#Author:  Gonca Ezgi Cakır
#Date:  25.04.2021
#Class:  Graduation Project II
#Project:  Kampus Ici Otonom Araclarla Ulasim Simulasyonu

#File:  passenger.py - passenger class


#import carla library
import glob
import os
import sys
import random

try:
    sys.path.append(glob.glob('../carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


#Passenger class to represent passengers in simulation
class Passenger(object):

  #id: passenger id
  #startS: start stop id
  #spawnTime: spawning time of the passenger
  #finalS: final stop id
  #waitTime: waited amount of time
  #waitLimit: limit for wait time
  #trans: transform object(carla)
  #walker_bp: type of the blueprint object(carla)
  #carlaObj: passenger object(carla)
  def __init__(self, id, startS, spawnTime, finalS, waitTime, waitLimit):
    
    self.id = id
    self.startS = startS
    self.spawnTime = spawnTime
    self.finalS = finalS
    self.waitTime = waitTime
    self.waitLimit = waitLimit
    self.walker = None
    self.trans = None
    self.carlaObj = None


  #creating passenger
  def spawn_passenger(self, world, locX, locY, rotYaw):

      #creating pedestrian 
      walker_bp = world.get_blueprint_library().filter("walker.pedestrian.*")
      self.trans = carla.Transform(carla.Location(x=locX, y=locY, z=1.85), carla.Rotation(yaw=rotYaw))

      #spawn pedestrian actor
      self.walker = random.choice(walker_bp) #get a random pedestrian character
      self.carlaObj = world.spawn_actor(self.walker, self.trans)
      world.wait_for_tick()
