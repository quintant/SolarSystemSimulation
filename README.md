# Solar System Simulator?

## The system
- Starts with 300 objects.
  - Can be changed by giving SpaceManager higher or lower input value.
- All objects start with random velocity (range can be changed) and location (size of the spawn box can be chaged).
- New objects can be placed by clicking the mouse.
  - New objects will spawn and the location of the click with a random velocity.
  
## Optimizations
- Objects that are very far away from each other will not calculate the gravitational force between them
  - This is done so after most of the objects have been merged the simulation runs faster
- Objects that go very far away from the sun are destroyed.
  - They wont have much effect on other objects and wont be seen
  - Gets rid of most out of view objects -> faster simulation
- Simulation runs on a separate thread.
- Garbage collection of planets happens in the backround.
- Smooth exit from simulation when exiting.
  
\
\
\
This is a small project done in one day. (+ some changes later on)
