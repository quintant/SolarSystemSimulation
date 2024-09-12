import numpy as np
import pygame
from numba import njit, prange
import math

@njit(parallel=True)
def compute_forces(obj_pos, obj_mass, obj_vel, numObjects, mid, cell_size, width, height, max_distance, active):
    # Initialize force array
    forces = np.zeros_like(obj_vel)

    # Precompute cell indices
    cell_indices = (obj_pos // cell_size).astype(np.int32)

    # Create a grid to store particle indices
    grid_shape = (int(np.ceil(width / cell_size)), int(np.ceil(height / cell_size)))
    MAX_PARTICLES_PER_CELL = 100  # Adjust based on expected maximum particles per cell

    grid_counts = np.zeros(grid_shape, dtype=np.int32)
    grid_particles = -np.ones((grid_shape[0], grid_shape[1], MAX_PARTICLES_PER_CELL), dtype=np.int32)

    # Assign particles to grid cells
    for i in prange(numObjects):
        if active[i]:
            x_idx, y_idx = cell_indices[i]
            if 0 <= x_idx < grid_shape[0] and 0 <= y_idx < grid_shape[1]:
                count = grid_counts[x_idx, y_idx]
                if count < MAX_PARTICLES_PER_CELL:
                    grid_particles[x_idx, y_idx, count] = i
                    grid_counts[x_idx, y_idx] += 1

    # Gravitational constant
    G = 1e-3

    # Calculate forces
    for i in prange(numObjects):
        if active[i]:
            xi, yi = obj_pos[i]
            mi = obj_mass[i]
            x_cell, y_cell = cell_indices[i]

            # Force due to the sun (central mass at obj_pos[0])
            if i != 0:
                x_sun, y_sun = obj_pos[0]
                m_sun = obj_mass[0]
                dx_sun = x_sun - xi
                dy_sun = y_sun - yi
                dist_sq_sun = dx_sun * dx_sun + dy_sun * dy_sun
                if dist_sq_sun > 0:
                    dist_sun = math.sqrt(dist_sq_sun)
                    force_mag_sun = G * mi * m_sun / dist_sq_sun
                    fx_sun = force_mag_sun * dx_sun / dist_sun
                    fy_sun = force_mag_sun * dy_sun / dist_sun
                    forces[i, 0] += fx_sun
                    forces[i, 1] += fy_sun

            # Inter-particle forces (with nearby particles)
            for dx_offset in range(-1, 2):
                for dy_offset in range(-1, 2):
                    nx_cell = x_cell + dx_offset
                    ny_cell = y_cell + dy_offset
                    if 0 <= nx_cell < grid_shape[0] and 0 <= ny_cell < grid_shape[1]:
                        cell_count = grid_counts[nx_cell, ny_cell]
                        for idx in range(cell_count):
                            j = grid_particles[nx_cell, ny_cell, idx]
                            if i != j and active[j] and j != 0:
                                xj, yj = obj_pos[j]
                                mj = obj_mass[j]
                                dx = xj - xi
                                dy = yj - yi
                                dist_sq = dx * dx + dy * dy
                                if 0 < dist_sq < max_distance * max_distance:
                                    dist = math.sqrt(dist_sq)
                                    force_mag = G * mi * mj / dist_sq
                                    fx = force_mag * dx / dist
                                    fy = force_mag * dy / dist
                                    forces[i, 0] += fx
                                    forces[i, 1] += fy

    return forces

@njit
def handle_collisions(obj_pos, obj_mass, obj_vel, numObjects, cell_size, width, height, collision_distance, active):
    # Precompute cell indices
    cell_indices = (obj_pos // cell_size).astype(np.int32)

    # Create a grid to store particle indices
    grid_shape = (int(np.ceil(width / cell_size)), int(np.ceil(height / cell_size)))
    MAX_PARTICLES_PER_CELL = 100

    grid_counts = np.zeros(grid_shape, dtype=np.int32)
    grid_particles = -np.ones((grid_shape[0], grid_shape[1], MAX_PARTICLES_PER_CELL), dtype=np.int32)

    # Assign particles to grid cells
    for i in range(numObjects):
        if active[i]:
            x_idx, y_idx = cell_indices[i]
            if 0 <= x_idx < grid_shape[0] and 0 <= y_idx < grid_shape[1]:
                count = grid_counts[x_idx, y_idx]
                if count < MAX_PARTICLES_PER_CELL:
                    grid_particles[x_idx, y_idx, count] = i
                    grid_counts[x_idx, y_idx] += 1

    # Collision detection and handling
    for i in range(numObjects):
        if active[i]:
            xi, yi = obj_pos[i]
            mi = obj_mass[i]
            vi_x, vi_y = obj_vel[i]
            x_cell, y_cell = cell_indices[i]

            for dx_offset in range(-1, 2):
                for dy_offset in range(-1, 2):
                    nx_cell = x_cell + dx_offset
                    ny_cell = y_cell + dy_offset
                    if 0 <= nx_cell < grid_shape[0] and 0 <= ny_cell < grid_shape[1]:
                        cell_count = grid_counts[nx_cell, ny_cell]
                        for idx in range(cell_count):
                            j = grid_particles[nx_cell, ny_cell, idx]
                            if i != j and active[j]:
                                xj, yj = obj_pos[j]
                                mj = obj_mass[j]
                                vj_x, vj_y = obj_vel[j]
                                dx = xj - xi
                                dy = yj - yi
                                dist_sq = dx * dx + dy * dy
                                if dist_sq < collision_distance * collision_distance:
                                    # Collision detected
                                    total_mass = mi + mj
                                    # Update velocity to conserve momentum
                                    vi_x = (mi * vi_x + mj * vj_x) / total_mass
                                    vi_y = (mi * vi_y + mj * vj_y) / total_mass
                                    mi = total_mass
                                    # Mark particle j as inactive
                                    active[j] = 0
                                    obj_mass[j] = 0
                                    obj_vel[j, 0] = 0
                                    obj_vel[j, 1] = 0
                                    obj_pos[j, 0] = -1
                                    obj_pos[j, 1] = -1
                                    # Update particle i's mass and velocity
                                    obj_mass[i] = mi
                                    obj_vel[i, 0] = vi_x
                                    obj_vel[i, 1] = vi_y

    return

class SpaceManager:

    def __init__(self, numObjects, sun=False, width:int=800, height:int=600, velocity_scale:float=1.5) -> None:
        self.numObjects = numObjects
        self.width = width
        self.height = height
        self.sun = sun

        # Initialize object positions
        self.obj_pos = np.random.uniform(0, 1, (self.numObjects, 2)) * np.array([self.width, self.height])

        # Set the central object mass and position (the sun)
        self.obj_mass = np.abs(np.random.randn(self.numObjects) * 10)
        self.obj_mass[0] = 1000  # Mass of the sun
        self.obj_pos[0] = np.array([self.width / 2, self.height / 2])  # Position of the sun at center
        self.mid = self.obj_pos[0]

        # Initialize velocities
        self.obj_vel = np.zeros((self.numObjects, 2))

        # Gravitational constant
        G = 1e-3

        # Velocity scaling factor to increase initial velocities
        self.velocity_scale = velocity_scale

        # Initialize velocities to give particles a tangential velocity around the sun
        for i in range(1, self.numObjects):
            # Radial vector from sun to particle
            r_vec = self.obj_pos[i] - self.obj_pos[0]
            r = np.linalg.norm(r_vec)
            if r > 0:
                # Unit radial vector
                r_hat = r_vec / r
                # Unit tangential vector (perpendicular to radial vector)
                t_hat = np.array([-r_hat[1], r_hat[0]])
                # Orbital velocity magnitude
                v = math.sqrt(G * self.obj_mass[0] / r)
                # Increase the velocity by the scaling factor
                v *= self.velocity_scale
                # Assign velocity
                self.obj_vel[i] = v * t_hat
            else:
                # If particle is at the same position as the sun, set velocity to zero
                self.obj_vel[i] = np.zeros(2)

        # Grid parameters
        self.cell_size = 50
        self.max_distance = 100

        # Collision parameters
        self.collision_distance = 5  # Adjust as needed

        # Active particles
        self.active = np.ones(self.numObjects, dtype=np.int32)

    def iterate(self, screen):
        # Store previous active status
        prev_active = self.active.copy()

        # Compute forces
        forces = compute_forces(self.obj_pos, self.obj_mass, self.obj_vel, self.numObjects, self.mid,
                                self.cell_size, self.width, self.height, self.max_distance, self.active)

        # Update velocities and positions for active particles
        for i in range(self.numObjects):
            if self.active[i]:
                self.obj_vel[i] += forces[i] / self.obj_mass[i]
                self.obj_pos[i] += self.obj_vel[i]

        # Handle collisions
        handle_collisions(self.obj_pos, self.obj_mass, self.obj_vel, self.numObjects,
                          self.cell_size, self.width, self.height, self.collision_distance, self.active)

        # Keep the central mass stationary
        self.obj_pos[0] = self.mid
        self.obj_vel[0] = 0

        # Handle boundary conditions (optional)
        # self.obj_pos = np.mod(self.obj_pos, [self.width, self.height])

        # Clear old positions for particles that were active
        old_pos = np.rint(self.obj_pos - self.obj_vel).astype(int)
        valid_old = (old_pos[:, 0] >= 0) & (old_pos[:, 0] < self.width) & \
                    (old_pos[:, 1] >= 0) & (old_pos[:, 1] < self.height) & \
                    (prev_active == 1)
        # Optionally, you can clear these positions on the surface if needed

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw particles with size proportional to mass
        for i in range(self.numObjects):
            if self.active[i]:
                x, y = int(self.obj_pos[i, 0]), int(self.obj_pos[i, 1])
                if 0 <= x < self.width and 0 <= y < self.height:
                    mass = self.obj_mass[i]
                    # Compute radius proportional to the cube root of mass
                    radius = max(1, int(mass ** (1/3)))
                    if i == 0:
                        # Draw the sun with a distinctive color
                        color = (255, 255, 0)  # Yellow color for the sun
                        radius = max(radius, 8)  # Ensure the sun is prominent
                    else:
                        color = (255, 255, 255)  # White color for other particles
                    pygame.draw.circle(screen, color, (x, y), radius)
