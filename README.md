# Gravity-simulation
This is a gravity simulation for the n-body problem. I have used pygame for the animation and classes to make
planet objects. In order to calculate changes of position of the planets I have assumed constant acceleration 
for a given time frame, indicated by dt  in the code. I have also used a constant velocity in this time interval to create the
changes in displacement. The smaller we make dt the more accurate ths simulation becomes but also the slower it is
. I have added a gravity softening factor which although unrealistic, creates a visually appealing 
simulation, making it more likely for planets to spiral each other. Note that when the planets become too close,
controlled by r_min, then the smaller plane coalesces into the greater planet, conservation of momentum is then 
used to find the subsequent velocity of the coalesced planets. The velocities of the planets is initialised randomly.


Here is an example of the the output:


![image](https://user-images.githubusercontent.com/91262171/135104417-1999a3bc-33af-432a-9eab-238ee99dd831.png)

