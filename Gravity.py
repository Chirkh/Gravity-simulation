# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 19:30:44 2021

@author: chi20
"""

'''This is a gravity simulation for the n-body problem. I have used pygame for the animation and classes to make
planet objects. In order to calculate changes of position of the planets I have assumed constant acceleration 
for a given time frame, indicated by dt. I have also used a constant velocity in this time interval to create the
changes in displacement. The smaller we make dt the more accurate ths simulation becomes but also becomes
considerably slower. I have added a gravity softening factor which creates a visually apealing 
simulation, making it more likely for planets to spiral each other. Note that when the planets become too close,
controlled by r_min, then the smaller plane coalesces into the greater planet, conservation of momentum is then 
used to find the subsequent velocity of the coalesced planets.'''
import pygame
import random
#constants
G=6.674e-11
grid=(1200, 600)
TotPlanets=10
Mass=100
Max_initv=1e-5
dt=2000
radius=5
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
diction={0:red, 1:green, 2:blue}
gen_per_frame=5
frame_per_sec=60
soften=0.4
Min_mass=80
Max_mass=400
r_min=0.2
class planet():
    def __init__(self, mass, x, y, v_x, v_y):
        self.mass=mass
        self.x=x
        self.y=y
        self.v_x=v_x
        self.v_y=v_y
        self.a_x=0
        self.a_y=0
        self.colour=(random.randint(0,250), random.randint(0,250), random.randint(0,250))
        self.hist=[(x,y)]
        
def Make_Planets(TotPlanets): #Makes a list of the planet objects with random initial coordinates
    planets=[]
    for i in range(TotPlanets):
        Mass=random.randint(Min_mass, Max_mass)
        X=random.randint(int(0.1*grid[0]), int(0.9*grid[0]))
        Y=random.randint(int(0.1*grid[1]), int(0.9*grid[1]))
        V_x=random.uniform(-Max_initv, Max_initv)
        V_y=random.uniform(-Max_initv, Max_initv)
        planets.append(planet(Mass, X, Y, V_x, V_y))
    return planets

def acceleration(particle, planets):
    
   # Acceleration reset to 0 after every timeframe of length dt
    a_x=0
    a_y=0
    for i in planets:
        if i!=particle:
            delta_x=particle.x-i.x
            delta_y=particle.y-i.y
            r=(delta_x**2+delta_y**2)**0.5 #Radius
            a_x-=G*i.mass*delta_x/(r+soften)**3
            a_y-=G*i.mass*delta_y/(r+soften)**3
    return a_x, a_y

def generation(planets):
    for i in planets:
        a_x, a_y=acceleration(i, planets)
        i.v_x+=a_x*dt
        i.v_y+=a_y*dt
        i.x+=i.v_x*dt
        i.y+=i.v_y*dt
        i.hist.append((i.x, i.y))
        
def display_screen():
    pygame.init()
    screen=pygame.display.set_mode(grid)
    screen.fill(pygame.Color('black'))
    clock=pygame.time.Clock()
    
    return screen, clock
        
        
def draw(planets, screen, gen):
    for i in planets:
        
        pygame.draw.circle(screen, i.colour, (i.x, i.y), radius*(i.mass/((Min_mass+Max_mass)*0.3)) )
        pygame.draw.line(screen, i.colour, (i.x-i.v_x*dt, i.y-i.v_y*dt), (i.x, i.y), 1)
    years=str((gen*dt)/31536000)[0:5] #31536000 seconds in a year
    pygame.display.set_caption('Time elapsed:{0} years'.format(years ))  
        
def trails(planets, screen): #Makes a trail for the planets dependent on size of planet
    for i in planets:
        width=min(4, i.mass/((Min_mass+Max_mass)*0.3)) #Make 1 width correspond to 0.6 between min and max
        pygame.draw.lines(screen, i.colour ,False,  i.hist, int(width)) 
        

def collide(i, j):
    dx=i.x-j.x
    dy=i.y-j.y
    r=(dx**2+dy**2)**0.5
    if r<r_min:
        return True
    
    

def momentum(a, b): #Simple 2d conservation of momentum, the planets coalsce and collide if they get close enough
    vx=(a.v_x*a.mass+b.v_x*b.mass)/(a.mass+b.mass)
    vy=(a.v_y*a.mass+b.v_y*b.mass)/(a.mass+b.mass)
    a.v_x=vx
    a.v_y=vy
    a.mass+=b.mass
    
    
def collision(planets):#Small planet gets removed and added onto new planet
    removals=[]
    for i in range(len(planets)-1):
        for j in range(i+1, len(planets)):
            if collide(planets[i], planets[j]):
                if planets[i].mass>=planets[j].mass:
                    momentum(planets[i], planets[j])
                    removals.append(planets[j])
                else:
                    momentum(planets[j], planets[i])
                    removals.append(planets[i])
    planets=[i for i in planets if i not in removals]
    return planets
        
def main():
    gen=0
    screen, clock=display_screen()
    planets=Make_Planets(TotPlanets)
    draw(planets, screen, gen)
    run=True
    while run:
        for i in range(gen_per_frame):
            gen+=1
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    pygame.quit()
            
            generation(planets)
            planets=collision(planets)
            screen.fill(pygame.Color('black'))
            draw(planets, screen, gen)
            trails(planets, screen)
        pygame.display.update()
        clock.tick(frame_per_sec)
main()      
            
            
        
    