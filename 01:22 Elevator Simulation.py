import random as rd
import numpy as np
import itertools

rd.seed(1)


class Passenger():
    """
    Passengers are initiated with a starting and ending floor and
    the waittime attribute is used to evaluate elevator performance.
    It represents total waiting and travel time.
    """
    def __init__(self, desired_floor, starting_floor):
        self.desired_floor = desired_floor
        self.starting_floor = starting_floor 
        self.waittime = 0 

        
        
class Elevator():
    """
    Elevators are initiated with a maximum capacity. Current and 
    next floor are used to track elevator movement and the moving 
    attribute determines when the elevator is stopping.
    The elevator keeps track of the passengers inside it, but not the
    global waiting list.
    """
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.current_capacity = 0
        
        self.current_floor = 0 
        self.next_floor = 0
        
        self.moving = False # True == moving
        self.passenger_list = []
        

  
    def get_next_floor(self, passenger_list):
        """
        Assigns as the next floor the first passenger's 
        desired floor.
        """
        self.next_floor = passenger_list[0].desired_floor
        
    def get_next_passenger(self, waiting_list):
        """
        Sets elevators next floor to a waiting passenger's
        starting floor when passenger list is empty.
        """
        self.next_floor = waiting_list[0].starting_floor
  
    def move(self):
        """
        Moves the elevator closer to the desired floor of the
        first passenger. Once it reaches that floor, self.moving
        is set to False. This is for time tracking and unloading. 
        """
        if self.next_floor > self.current_floor:
            self.current_floor += 1
        elif self.next_floor < self.current_floor:
            self.current_floor -= 1
        else: 
            self.moving = False           
            
    
class Building():
    """
    Buildings are initiated with a number of floors. They keep track
    of the global waitlist and the total runtime, passed from passengers
    who have finished their journey (self.finished_passengers).
    """
    def __init__(self, floors):
        self.floors = floors 
        self.waiting_list = []
        self.finished_passengers = []
        self.total_runtime = 0
        
    
    def spawn_passengers(self, num_of_passengers):
        """
        Creates passengers with random starting and desired floors, 
        ensuring that those are not the same. Appends them to the
        global waiting list and finishes by sorting the waiting list.
        """
        for _ in range(num_of_passengers):
            starting = rd.randint(0, self.floors)
            desired = rd.choice([x for x in range(self.floors) if x != starting])
            
            self.waiting_list.append(Passenger(starting, desired))
        self.waiting_list = sorted(self.waiting_list, key=lambda x: x.starting_floor)
        
        
    def unload_elevator(self, elevator, waiting_list_on_current_floor):
        """
        Drops of passengers on their desired floor by adding them to the
        finished_passenger list and picks up new, waiting passengers.
        Sets moving back to True.
        Ensures that the maximum capacity is not surpassed.
        """
          #p is used to represent passengers in all code
        for i, p in enumerate(elevator.passenger_list):
            if p.desired_floor == elevator.current_floor:
                self.finished_passengers.append(elevator.passenger_list.pop(i))
                elevator.current_capacity -= 1
        
        entered_elevator = []
        for p in waiting_list_on_current_floor:
            if elevator.current_capacity < elevator.max_capacity:
                elevator.passenger_list.append(p)
                entered_elevator.append(p)
                elevator.current_capacity += 1
        
        self.waiting_list = [p for p in self.waiting_list if p not in entered_elevator]
        self.moving = True
                
    
    def update_time(self, elevator, time):
        """
        Updates each unfinished person's time counter by a set time.
        """
        for p in itertools.chain(self.waiting_list, elevator.passenger_list):
          p.waittime += time
                               

        
    def run_elevator_simulation(self, sim_size, capacity, walking = False):
        """
        META FUNCTION
        This function performs the full elevator run. If walking
        is set to True, passengers with less than or equal to 4 floors to go will
        take the stairs instead of the elevator.
        
        It spawns passengers and performs elevator movements. Moving 1 floor is
        the base unit of time and takes 1. Stopping takes 3 and walking 
        stairs also takes 3 units of time.
        """
        elevator = Elevator(capacity)
        self.spawn_passengers(sim_size)
                             
        if walking == True:
            # people take 3x as long to walk, as the elevator takes
            # to move a single floor.
            for i, p in enumerate(self.waiting_list):
                distance = abs(p.desired_floor - p.starting_floor)
                if distance <= 4:
                    p.waittime = distance * 3 
                    self.finished_passengers.append(self.waiting_list.pop(i))
                    
                                                                                   
        while len(self.waiting_list) != 0 or len(elevator.passenger_list) != 0:
          #uncomment print statements below to track elevator movement
#             print("# of waiting: ", len(self.waiting_list))
#             print("# of passengers: ", len(elevator.passenger_list))
#             print("# of finished: ", len(self.finished_passengers))
#             print("I'm on floor %d." %elevator.current_floor)
#             print("-------------------")
#             for p in self.waiting_list:
#                 print (p.starting_floor, p.desired_floor)

                
            if elevator.moving == False:
                  # time steps are added whenever the elevator stops to unload
                  # big elevators take longer
                if elevator.max_capacity >= 15:
                    self.update_time(elevator, 5)
                else:
                    self.update_time(elevator, 3)
                  # determines who's waiting on the current floor & adds them
                  # to the elevator/drops off current passengers
                waiting_list_on_current_floor = [p for p in self.waiting_list 
                                                 if p.starting_floor == elevator.current_floor]
                self.unload_elevator(elevator, waiting_list_on_current_floor)
#                 print("Currently holding %d passengers." %elevator.current_capacity)
            
            
            if len(elevator.passenger_list) == 0 and len(self.waiting_list) != 0:
                  # if there's no more passengers in the elevator, pick up new ones
                  # move elevator 1 floor
                elevator.get_next_passenger(self.waiting_list)
                elevator.move()
                self.update_time(elevator, 1) 
                    
            if len(elevator.passenger_list) != 0:
                elevator.get_next_floor(elevator.passenger_list)
                elevator.move()
                self.update_time(elevator, 1)
                       
        
#         print ("I have moved all passengers!")
        for p in self.finished_passengers:
            self.total_runtime += p.waittime
        
#         print ("Average runtime is %d units." %(self.total_runtime/sim_size))
        return (self.total_runtime/sim_size)
     
    
    def reset_simulation(self):
        """
        Clear runtime variables.
        """
        self.finished_passengers = []
        self.total_runtime = 0
                                          

Judy_the_House = Building(20) 
Judy_the_House.run_elevator_simulation(180, 7) 
Judy_the_House.reset_simulation()