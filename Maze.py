''' Maze
                    '''

import pygame, sys, time, random,math
from pygame.locals import *

pygame.init()
''' Maze ver 0.1 - have the rat look for the cheeses using the arrow keys. After all cheeses have been collected
    return to the home room to stop the timer and save your best time. By - Loqoman and IslandSparky
    ver 1.0 Corrected maze logic so maze complexity can be changed.
    ver 1.1 Revised game instructions above

 
Programmer Changelog

7/13/2016 9:11PM  - Commit version 1.0 to github
7/13/2016 9:18PM  - Commit version 1.1 to github'''


BLACK = (0,0,0)
WHITE =  (255,255,255)
YELLOW = (255,255,0)
LIGHTYELLOW = (128,128,0)
RED = (255, 0 ,0)
LIGHTRED = (128,0,0)
BLUE = (0, 0, 255)
SKYBLUE = (135,206,250)
GREEN = (0,255,0)
LIGHTGREEN = (152,251,152)
AQUAMARINE = (123,255,212)
LIGHTBROWN = (210,180,140)
LIGHTGREY = (211,211,211)
DIMGREY = (105,105,105)
VIOLET = (238,130,238)
SALMON = (250,128,114)
GOLD = (255,165,0)
BACKGROUND = LIGHTGREY
WINDOWWIDTH = 1250
WINDOWHEIGHT = 750
MAZE_TOPLEFT = (50,150)   # Top left corner of the maze area
MAZE_WIDTH = 1000
MAZE_HEIGHT = 600

# The following two dictionaries define the room and cheese complexity for various
# game levels
ROOMS_V = {'E':15,'M':25,'H':45,'H+':60}  # number of rooms in the vertical direction
GAME_CHEESE = {'E':1,'M':5,'H':10,'H+':15} # number of cheeses to store 

LAST_CHEESE_ROOM = 0

windowSurface = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption('Maze')
#--------------------Maze Class -----------------------------------------
# Class for the maze
class Maze(object):
#
    rooms_V = 0  # Number of rooms in vertical direction
    rooms_H = 0  # Number of rooms in horizontal
    room_size = 0# Size of each room in pixels
    starting_col = 0  # Starting column
    starting_row = 0  # Starting row
    difficulty = 'M'  # difficulty of maze, default to medium
    cheeses = []  # rooms containing the cheeses


    def __init__(self):
    # Maze initialization method called when maze is created
        Maze.difficulty = 'M'   # default difficulty to medium
            
        return  # return from Maze.__init__

    def build(self):
        Room.rooms = []   # empty the list of rooms before building them
        Path.clear_paths()  # empty all the path lists

        
    # Maze.build function called at the Maze object level to build a maze.
        Maze.rooms_V = ROOMS_V[Maze.difficulty]

        '''if Maze.difficulty == 'E':
            Maze.rooms_V = int(ROOMS_V[0])
        elif Maze.difficulty == 'M':
            Maze.rooms_V = int(ROOMS_V[1])
        elif Maze.difficulty == 'H':
            Maze.rooms_V = int(ROOMS_V[2])
        elif Maze.difficulty == 'H+':
            Maze.rooms_V = int(ROOMS_V[3])'''
        Maze.rooms_H = int(Maze.rooms_V * (float(MAZE_WIDTH)/float(MAZE_HEIGHT)))
        Maze.room_size = int(float(MAZE_HEIGHT)/float(Maze.rooms_V))
              
        Maze.starting_col = 0
        Maze.starting_row = int(Maze.rooms_V/2)
            
        # Fill in the rooms array with the room objects
        for h in range (0,Maze.rooms_H):
            Room.rooms.append([])  # this creates the second dimension
            for v in range(0,Maze.rooms_V):
                room = Room(size=Maze.room_size,row=v,col=h)
                Room.rooms[h].append(room)
                Room.unused_rooms.append(room)
        
        # generator doesn't mark the starting room because it is used for branches
        # so mark the starting room as solid white

        while True:
            room = Room.rooms[Maze.starting_col][Maze.starting_row]
            room.room_color = WHITE
            room.state = 'P'
            Room.draw(room)

            # Do a random walk for primary path
            p_path = Path() # create an object for the primary path
            east_exit = p_path.random_walk(col=Maze.starting_col,row=Maze.starting_row,
                                    color=RED,room_state='P',seek_east=True)
            if east_exit:

                break
            else:
                Maze.reset(maze) # reset the array and try again

        room = Room.rooms[Maze.starting_col][Maze.starting_row]
        Room.unused_rooms.remove(room) # show starting room is used
        p_path.rooms.insert(0,room)  # add starting room to head of rooms list

        Path.primary_path.append(p_path) # append the path object, only one

        # Now build some secondary paths
        for i in range(0,int(len(p_path.rooms)/5)):
            room_index = random.randrange(0,len(p_path.rooms))
            room = p_path.rooms[room_index]
            col = room.col
            row = room.row
            s_path = Path()  # create a new secondary path object
            unused = s_path.random_walk(col,row,color=YELLOW,
                                         room_state='S')
            if len(s_path.rooms) > 0: # don't store empty path
                Path.level2_paths.append(s_path)
            
        # Also build some Tertiary paths]
        if len(Path.level2_paths) >0:  # make sure there are paths at level 2
            for i in range(0,len(Path.level2_paths)): # for all paths in level2
                
                if len(Path.level2_paths[i].rooms) > 0: # insure some rooms
                    for j in range(0,int(len(Path.level2_paths[i].rooms))):
                        room_index = random.randrange(0,
                                            len(Path.level2_paths[i].rooms))
                        room = Path.level2_paths[i].rooms[room_index]
                        col =room.col
                        row =room.row
                        t_path = Path()   # ceate a new path object
                        unused= t_path.random_walk(col,row,color=GREEN,
                                                 room_state='T')
                        if len(t_path.rooms) > 0: # don't store empty path
                            Path.level3_paths.append(t_path)
        # And finally some level4 paths
        if len(Path.level3_paths) >0:  # make sure there are paths at level 3
            for i in range(0,len(Path.level3_paths)): # for all paths in level 3
                if len(Path.level3_paths[i].rooms) > 0: # ensure some rooms
                    for j in range(0,int(len(Path.level3_paths[i].rooms))):
                        room_index = random.randrange(0,
                                            len(Path.level3_paths[i].rooms))
                        room = Path.level3_paths[i].rooms[room_index]
                        col =room.col
                        row =room.row
                        f_path = Path()  # create a new path object
                        unused= f_path.random_walk(col,row,
                                                color=AQUAMARINE,
                                                 room_state='F')
                        if len(f_path.rooms) > 0: # don't store empty path
                            Path.level4_paths.append(f_path) 
           
        # For debug, turn all the unused rooms to a light color

        for i in range(0,len(Room.unused_rooms)):
            room = Room.unused_rooms[i]
            room.room_color = LIGHTGREY
            Room.draw(room)

        # clean up the unused cells

        while len(Room.unused_rooms) > 0:
            # select an unused room to start a dead end path
            room = random.choice(Room.unused_rooms)
        #    print('calling dead_end',room.col,room.row)
        #    print('length of unused rooms is',len(Room.unused_rooms))
#            d_path = Path()
            d_path = Path()    # build a new path object
            status = d_path.build_dead_end(room.col,room.row,
                                            color=SALMON,room_state='D')
            if status:
                Path.dead_end_paths.append(d_path)
            
        time.sleep(1)

        # Show maze in light color
        for col in range(0,Maze.rooms_H):
            for row in range(0,Maze.rooms_V):
                room = Room.rooms[col][row]
                room.room_color = LIGHTGREY
                room.draw()

        # Redraw the starting room in white
        room = Room.rooms[Maze.starting_col][Maze.starting_row]
        room.room_color = WHITE
        room.draw()


        # Redraw the ending room in green
        last_room = p_path.rooms[len(p_path.rooms)-1]
        print(last_room.col,last_room.row)
        last_room.room_color = GREEN
        last_room.draw()
        pygame.display.update()
        
        # return from Maze.build
        return  

    def reset(self):
    # Maze method to reset the room array to initial condition
        Room.unused_rooms = []  # empty the unused rooms list
        for col in range (0,Maze.rooms_H):
            for row in range(0,Maze.rooms_V):
                room = Room.rooms[col][row]
                Room.unused_rooms.append(room)
                room.room_color = BACKGROUND
                room.state = None;
                room.contents = []  # reset to no contents
                #initialize the state of the walls
                room.walls = ['N','S','E','W']
                room.draw()

        return # return from Maze.reset

    def store_cheese(self):
    # store cheese in the longest paths of level 4 paths
        num_cheeses = GAME_CHEESE[Maze.difficulty]
        num_stored = 0    
            # find the longest path not already used
        path_used = []
        while num_stored < num_cheeses:
            longest_path = 0
            most_rooms = 0
            for path_index in range(0,len(Path.level4_paths)):
                if ( (len(Path.level4_paths[path_index].rooms) > most_rooms) and
                     (path_index not in path_used) ):
                     longest_path = path_index
                     most_rooms = len(Path.level4_paths[path_index].rooms)

            path_used.append(longest_path) # use longest path not yet used           
            path =Path.level4_paths[longest_path]
            room = path.rooms[len(path.rooms)-1]
            room.room_color = GOLD
            room.contents.append('cheese')
            Maze.cheeses.append(room)  # add room to list containing cheese
            room.draw()
            num_stored += 1
            pygame.display.update()
        
        return  # return from store cheeese

#------------------- Path Class ----------------------------------------
# Class for paths through the maze
class Path(object):
    primary_path = [] # the primary path object in list same as others
    level2_paths = [] # the list of paths that are secondary
    level3_paths = [] # list of the third level paths
    level4_paths = [] # list of fourth level paths
    dead_end_paths = [] # list dead end paths randomly connected to others
    '''
     N
     |
 W---|---E
     |
     S
    '''
    def __init__(self):
    # Path class initializer, called when a path is created to build path object                        
        self.rooms = [] # set the rooms list empty

        return  # return from Path.__init__

    def random_walk(self,col=0,row=0,color=BACKGROUND,room_state='P',
                    seek_east=False):
    # Function to do a random walk
#        self.rooms.append(Room.rooms[col][row])
        rewind_depth = 0 # initialize the depth of rewind
        while True:
            old_col = col
            old_row = row
            bail_out = False
            # try a random direction out and see if we can move there
            possible_directions=['N','S','E','W']
            if seek_east:
               possible_directions=['N','N','S','S','E','E','W']            
            if seek_east:
                if (row == 0) |(row >= Maze.rooms_V-1): # don't loop back if N or S
                    possible_directions.remove('W')
            while len(possible_directions) > 0:
                room = Room.rooms[col][row]

                try_index = random.randrange(0,len(possible_directions))

    #           print(try_index,col,row,possible_directions)       
                direction = possible_directions[try_index]
                del possible_directions[try_index]
               
                status,col,row = Room.walk(room,
                                           direction=direction,wall_check=False)
    #           print('Room state is ',Room.rooms[col][row].state)
                if ((not status) |
                    (not (Room.rooms[col][row].state == None)) ):
                    col = old_col  # room was busy, back out
                    row = old_row
                    if len(possible_directions) <= 0: # we are stuck
                        if (room_state == 'P'): # stuck, if primary, rewind and try again
                            #print('Stuck on primary path')
                            #  back out several rooms and try again
                            rewind_depth += 1 # rewind farther each time stuck
                            rewind = rewind_depth  # set the maximum number of rewind rooms
                            while ( (rewind > 0) and (len(self.rooms) > 1) ):
                                #print('rewind =', rewind)
                                last_room = self.rooms[len(self.rooms)-1]
                                entry_direction = last_room.entry_direction # remember before wiping out
                                last_room.entry_direction = []
                                last_room.room_color = BACKGROUND # mark old room at end of path as unusued
                                last_room.state = None
                                last_room.walls = ['N','S','E','W'] # restore its walls
                                self.rooms.remove(last_room) # take it out of the path
                                Room.unused_rooms.append(last_room) # put it back unused
                               # restore the wall entered from in the previous room
                                room = self.rooms[len(self.rooms)-1]
                                room.walls.append(entry_direction)
                                col =room.col
                                row = room.row
                                last_room.draw()
                                pygame.display.update()
                                time.sleep(.1)
                                                               
                                rewind = rewind - 1 # count down rewinding room
                                bail_out = True
                            
                            pygame.display.update()
                            if (bail_out):
                                break
                        else: # stuck not on primary path
                            return False

                    
                else:  # room seems OK to add to the walk

                   # get the object for this room and change its color as indicated

                    if (len(self.rooms) > 0 ): # remember old room to knock down walls
                        old_room = self.rooms[len(self.rooms)-1]
                    else:
                        old_room = Room.rooms[old_col][old_row] # special case for first room
                    room = Room.rooms[col][row]
                    self.rooms.append(room)
                    room.entry_direction = direction
                    room.room_color = color
                    room.state = room_state  # indicate room is used
                    Room.unused_rooms.remove(room)  # delete from unusued rooms
                    # knock down the wall in old and new room.
                    Room.knock_out_walls(direction,room,old_room)
                    room.draw()
                    pygame.display.update()
                    
                    if seek_east and (col == Maze.rooms_H-1):

                        return True # we found an east exit
                    else:
                        break
                if (bail_out):
                    break
    #        time.sleep(.1)
                 

        return False  # shouldn't ever get here.

    def build_dead_end(self,col=0,row=0,color=LIGHTGREEN,room_state='D'):
    # Function to do clear out unused rooms by building dead end paths.  They
    # break into any exiting path that is not isolated from another path.
    # call with a row and column on the unused room list.
    # returns with status (False if stuck) and new deadend path.
    # note deadend paths start at the end room.

        search = [] # this will hold tuples for rooms and directions entered
        # pick out an unused room and start there
        room = Room.rooms[col][row]  # start with the indicated room
        search.append((room,None))  # remember room and entry direction
        room.state = 'X'   # indicate we are in search mode
        room.room_color= LIGHTGREEN # show in search path
        room.draw()
        while True:
            old_col = col
            old_row = row
            # try a random direction out and see if we can move there
            possible_directions=['N','S','E','W']

            while (len(possible_directions) > 0) :
                room = Room.rooms[col][row]

                try_index = random.randrange(0,len(possible_directions))

#                print(try_index,col,row,possible_directions)       
                direction = possible_directions[try_index]
                del possible_directions[try_index]
                status,col,row = Room.walk(room,
                                           direction=direction,wall_check=False)
#                print('Trial room is ',col,row,Room.rooms[col][row].state)
                if ((status) and
                    (Room.rooms[col][row].state != 'X') ): # don't loop on itself

#                    print('room seems ok')                
                    # Room seems OK
                    # get the object for this room 
                    old_room = Room.rooms[old_col][old_row]  # remember old room
                    room = Room.rooms[col][row]


                    if room.state != None:
                        # knock out the wall into this room
                        Room.knock_out_walls(direction,room,old_room)
#                        print('found a way out',room.col,room.row,room.state)
                        # Found another path, this is out way out
                        # walk search path, fixing status,color and clearing walls

#                        print ('len(search),first entry=',len(search),search)
                        while len(search) > 0:
                            entry = search[0] # get from head of list
                            room = entry[0]
                            self.rooms.append(room)
                            direction = entry[1]
#                            print ('from search',room.col,room.row,room.state,direction)
                            room.state = room_state # indicate on dead end path
                            room.room_color = color # set to argument color
                            room.draw()
                            pygame.display.update()
                            if direction != None: # bypass first room
                                Room.knock_out_walls(direction,room,old_room)
                                old_room.draw()
                                room.draw()
                                old_room = room
                            else:  # it is the first room
                                old_room.room_color = color
                                old_room.draw()
                                old_room = room

                            Room.unused_rooms.remove(room)
                            search.remove(entry) # trim down the temp list

#                        print('connected to another path exiting with true status')
                        return True  # return Ok


                                    
                    else:  # room OK,but still searching
    #                    print('room ok but still searching')
                        room.room_color = LIGHTBROWN
                        room.state = 'X'  # indicate room is used in search
                        search.append((room,direction)) # room and way we came in
                        Room.draw(room)
                        break
               
                else:  # Can't go this way or use this room
    #                print('cant go this way or use this room')
                    room.room_color = LIGHTGREEN # for debug set to lightgreen
                    col = old_col  # room was busy, back out
                    row = old_row
                    if len(possible_directions) <= 0: # we are stuck
                        # we are stuck, walk the path and reset status to unused.
                        while len(search) > 0:
                            for entry in search:
    #                            print('we are stuck,len search=',len(search))
                                room = entry[0]  # get the room
                                room.state = None # set back to unused
                                room.room_color = BACKGROUND # for debugging visuals
                                Room.draw(room)
                                search.remove(entry)
    #                    print('exiting with false status')
                        return False
                    

#            time.sleep(.1)
                 
        print('build dead end - tilt, shouldnot get here')
        return False  # shouldn't ever get here.

# method to clear out all paths for maze reset
    def clear_paths():
        Path.primary_path = [] # the primary path object in list same as others
        Path.level2_paths = [] # the list of paths that are secondary
        Path.level3_paths = [] # list of the third level paths
        Path.level4_paths = [] # list of fourth level paths
        Path.dead_end_paths = [] # list dead end paths randomly connected to others


        

#------------------- Room Class  ----------------------------------------
#Class for the rooms in the maze
class Room(object):
    
    rooms = []  # holds the doubly indexed list of room objects
    unused_rooms = [] # single indexed list of the unused rooms
    
    def __init__(self,size=Maze.room_size,row=0,col=0):
    #Room initialization method called when room is created.  Column and row
    # give the position in the array
        self.room_color = BACKGROUND  # chose the paint colors
        self.wall_color = BLACK
        self.size = size  # size of the room in pixels
        self.col = col    # column coordinate
        self.row = row   # row coordinate
        self.state = None   # usage state of the room
        self.contents = [] # contents list to empty

        #initialize the state of the walls. If they are in the list they are up.
        self.walls = ['N','S','E','W']
        # remember the direction you were going when you entered the room
        self.entry_direction = []
        #Remember the way you came in, opposite from the direction from the last room
        self.way_out = []
        #Remember all the directions you have explored
        self.explored = []
        
        #define a rectangle for this room and save it
        left = int(float((WINDOWWIDTH-MAZE_WIDTH)/2.)
                   +int(self.col*float(size)))
        top =  int(float((WINDOWHEIGHT-MAZE_HEIGHT)/2)
                   +int(self.row*float(size)))
        self.rect = pygame.Rect(left,top,size,size)

        self.draw()  # draw the room

        return  # return from Room.__init__

    def draw(self):
    # Room method to draw and room and it's walls acording to current wall state

        pygame.draw.rect(windowSurface,self.room_color,self.rect,0) # draw the floor

        #draw the walls based on their state
        if self.walls.count('N') > 0:
            pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.left,self.rect.top),
                             (self.rect.left+self.size,self.rect.top),1)
        if self.walls.count('S') > 0:
           pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.left,self.rect.bottom),
                             (self.rect.left+self.size,self.rect.bottom),1)
        if self.walls.count('W') > 0:
           pygame.draw.line(windowSurface,self.wall_color,
                 (self.rect.left,self.rect.top),
                 (self.rect.left,self.rect.top+self.size),1)
        if self.walls.count('E') > 0:
           pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.right,self.rect.top),
                             (self.rect.right,self.rect.top+self.size),1)
        

        pygame.display.update()

        return  # return from Maze.draw

    def walk(self,direction='N',wall_check=True):
    #Maze method to walk out of a room
    # if walk_check is False, you can walk through walls (used for initial
    # maze setup). Returns false if we can't go that way, also returns updated
    # room object.
    
        moved = False  # establish default
        col = self.col # initial col
        row = self.row
        if ( (direction == 'N') &
             (self.row >0) ):
            if( (self.walls.count('N') == 0) |  (not wall_check)):
                 row -=1
                 moved = True
        if ( (direction == 'S') &
             (self.row < (Maze.rooms_V-1) ) ):
            if( (self.walls.count('S') == 0) |  (not wall_check)):
                 row +=1
                 moved = True
        if ( (direction == 'W') &
             (self.col >0) ):
            if( (self.walls.count('W') == 0) |  (not wall_check)):
                 col -=1
                 moved = True
        if ( (direction == 'E') &
             (self.col < (Maze.rooms_H-1) ) ):
            if( (self.walls.count('E') == 0) |  (not wall_check)):
                 col +=1
                 moved = True
#        print('dir,N,S,E,W= ',direction,self.walls)

        return moved,col,row  # returned with indication of success or failure

    def knock_out_walls(direction,room,old_room):
    # General purpose function to clear the walls from which we entered a room.
    # direction is the direction we were going when we entered.
    # room is current room object. old_room is the room we entered from.
 

        if direction == 'N':
            old_room.walls.remove('N')
            room.walls.remove('S')
        elif direction == 'S':
            old_room.walls.remove('S')
            room.walls.remove('N')
        elif direction == 'E':
            old_room.walls.remove('E')
            room.walls.remove('W')                              
        elif direction == 'W':
            old_room.walls.remove('W')
            room.walls.remove('E')
        Room.draw(old_room) # redraw both rooms
        Room.draw(room)

        return # return from knock_out_walls


#---------------------- Rat Class ----------------------------------------
# Rat class for the rat that is going to run the maze
class Rat(object):  # create Rat object

    def __init__(self,direction = 'E',color=DIMGREY ):

        self.direction = direction
        self.color = color
        self.room = Room.rooms[Maze.starting_col][Maze.starting_row]
        self.cheeses = []  # empty list of cheeses we carrys

        self.draw()  # draw him in the starting room
        
        return # return from Rat.__init__

    def draw(self):
    # draw the rat in his room

        pygame.draw.circle(windowSurface,self.color,self.room.rect.center,
                           int(Maze.room_size/3),0)
        pygame.display.update()

        return  # return from Rat.__init__

    def erase(self):
    # erase the rat from this room

        pygame.draw.circle(windowSurface,self.room.room_color,
                           self.room.rect.center,int(Maze.room_size/3),0)
        pygame.display.update()

        return # return from Rat.erase

    def move(self,direction='E'):
    # move the rat in the indicated direction
        status,col,row = self.room.walk(direction)
        if status: # move was legal
            self.erase()   # erase from the current room
            self.room = Room.rooms[col][row] # get new room he is in
            self.check_for_cheese(self.room)
            self.draw()   # draw rat in new room

        return status   # return whether move occurred or not

    def check_for_cheese(self,room):
    # see if there is cheese in room, if so, pick up cheese, change room color
    # to background and return true
        if 'cheese' in room.contents:
            self.cheeses.append('cheese')  # add to the stuff we carry
            room.contents.remove('cheese')  # remove from the room
            Maze.cheeses.remove(room) # remove room from master list of cheeses
            room.room_color = BACKGROUND
            self.room.draw() # redraw room with no cheese
            return True
        else:
            return False
                
    def cheese_num(self):
        return len(self.cheeses)
    def reset_cheese(self):
        self.cheeses = []
    def change_color(self,color_n):
        self.color = color_n
        self.draw()

#------------------------------------------------------------------
# Robot_Rat class
# This dumb robot rat basically does a random walk with a bit of a
# refinement that causes him to prefer rooms that he hasn't been in
# before.
#------------------------------------------------------------------

class Robot_Rat(Rat):  # create Rat object

    def __init__(self,direction = 'E',color=DIMGREY ):

        Rat.__init__(self,direction,color) # use the parent class init for basics

        return

    def auto_move(self):

         possible_directions=['E','S','N','W']
         #print ('walls =', self.room.walls)
         for direction in self.room.walls:
             possible_directions.remove(direction)
         for direction in self.room.explored:
             possible_directions.remove(direction)
         #print('Way out =',self.room.way_out)
         if (len(self.room.way_out) != 0):        
             possible_directions.remove(self.room.way_out) # don't explore the way you came
         #print(possible_directions)


          

         while  len(possible_directions) > 0 :
            if (possible_directions.count('E') > 0): # Seek east if possible
                direction = 'E'
                possible_directions.remove('E')
            else:
                try_index = random.randrange(0,len(possible_directions))
                direction = possible_directions[try_index]
                del possible_directions[try_index]
            #print(try_index,self.room.col,self.room.row)
            old_room = self.room
            status = self.move(direction=direction)
            #print('status',status,self.room.col, self.room.row)
            if ( status): 
                old_room.explored.append(direction) #mark that we have gone this way
                self.room.room_color = DIMGREY # show we have visited this room

                # if this room doesn't already have a way out (indicating the first
                # entrance, mark the way out.
                if ( len(self.room.way_out) == 0):
                     self.room.way_out = self.opposite_direction(direction)
                     
                return 
                

         # couldn't find a fresh exit, go back the way you came

         self.move(direction = self.room.way_out)
         return
        

    def opposite_direction(self,direction):  # return the direction opposite to that specified

        directions = ['N','S','E','W']
        opposite = ['S','N','W','E']

        index = directions.index(direction)

        return opposite[index]
        
                     



        


#------------------------------------------------------------------
# Define the widget classes
#------------------------------------------------------------------

class Widget(object):
# Widget class for all widgets,  its  function is mainly to hold the
# dictionary of all widget objects by name as well as the application
# specific handler function. And support isclicked to
# see if cursor is clicked over widget.

    widgetlist = {} # dictionary of tubles of (button_object,app_handler)
    background_color = LIGHTGREY

    def __init__(self):
    # set up default dimensions in case they are not defined in
    # inherited class, this causes isclicked to default to False
        self.left = -1
        self.width = -1
        self.top = -1
        self.height = -1

    def find_widget(widget_name):
    # find the object handle for a widget by name        
        if widget_name in Widget.widgetlist:
            widget_object = Widget.widgetlist[widget_name][0]
            return  widget_object
        else:
            Print ('Error in find_widget, Widget not found ' + widget_name)
            return

    def isclicked (self, curpos):
    # button was clicked, is this the one? curpos is position tuple (x,y)
        

        covered = False

        if (curpos[0] >= self.left and
        curpos[0] <= self.left+self.width and
        curpos[1] >= self.top and
        curpos[1] <= self.top + self.height):
            covered = True

        return covered
    

    def handler(self):
    # prototype for a widget handler to be overridden if desired
        pass #do nothing    
            
class Button(Widget):

    buttonlist = []
    grouplist = {}
    
    def __init__ (self, window = windowSurface,color = BLACK,
                  topleft = (200,200), size=20,name = '', label='',
                  value = '',app_handler=Widget.handler,
                  group = '',groupaction = 'RADIO'):   

        self.window = window
        self.color = color
        self.topleft = topleft
        self.left = topleft[0]  # required by isclicked method in Widget
        self.top = topleft[1]   # "
        self.width = size       # "
        self.height = size      # "
        self.right = self.left + size
        self.bottom = self.top + size
        self.size = size
        self.name = name
        self.label = label
        self.value = value
        self.app_handler = app_handler # object of applications specific handler
        self.group = group
        
        self.groupaction = groupaction
        # groupaction value of 'RADIO' allows only one in group to be on
        # 'RADIO_WITH_OFF' allows only one but all off also
        # '' means no group action required

        self.state = False    # Initialize button state to 'off'


        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        else:
            print ('Error - duplicate widget name of ' + name)

        Button.buttonlist += [self] # add to button list as a object

        # if button is in a group, add group to dictionary if the group is not
        # already there.  Then add the button to the group.

        if group in Button.grouplist:
            Button.grouplist[group] += (self,)
        else:
            Button.grouplist[group] = (self,)


        
        # get the rectangle for the object
        self.rect = pygame.draw.rect(window,color,
        (topleft[0],topleft[1],size,size),1)

        #write label if any
        if label != '':
           self._label()
            
        self.draw()

    def _label(self): # private method to generate label, does not do draw
       labelFont = pygame.font.SysFont(None, int(self.size*1.5) )
       text = labelFont.render(self.label,True,self.color,
       Widget.background_color)
       
       textRect= text.get_rect()
       textRect.left = self.rect.right + 5
       textRect.bottom = self.rect.bottom
       self.window.blit(text, textRect)
                                                   

    def identify(self):  # print my name
        print ("Button name is:" + self.name)

    def draw (self): # draw button with current state
        
        self.rect = pygame.draw.rect(self.window, self.color,
        self.rect,1)

        if self.state:

            pygame.draw.circle(self.window,self.color,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2))
            ,int(self.size/2)-2,0)
        else:
            pygame.draw.circle(self.window,WHITE,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2)),
            int(self.size/2)-2,0)
            
            pygame.draw.circle(self.window,self.color,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2)),
            int(self.size/2)-2,1)
                               
        pygame.display.update()   # refresh the screen

    def toggle (self):  # toggle the button state
        if self.state:
            self.state = False
        else:
            self.state = True
            
        self.draw()



    def group_handler(self):
    # if button in a group, button is now on and is a RADIO button  then
    # turn off all other buttons in the group

        #if groupaction is 'RADIO' or 'RADIO_WITH_OFF'and new state is on,
        # turn off all other buttons in the group. 
        if ( (self.groupaction == 'RADIO') |
             (self.groupaction == 'RADIO_WITH_OFF') ):

            # loop finding other buttons in group and turning them off
            for i in range(len((Button.buttonlist))):

                if (Button.buttonlist[i].group == self.group and
                Button.buttonlist[i] != self):
                    Button.buttonlist[i].state = False
                    Button.draw(Button.buttonlist[i])

        # Now, if 'RADIO' and if new state is off,
        # tun it back on because at least one must be on in the group.
        if self.groupaction == 'RADIO':
            if (self.state == False):
                self.toggle()
                return
#------------------------------------------------------------
# Button handler method,  overriding the Widget
# handler method prototype. Does some general work then calls the
# group handler and application specific handler if any
#------------------------------------------------------------

    def handler(self):


        # toggle the state of the button
        self.toggle()

        # see if button is in a group and if so, call  the group handler
        # in button class to enforce such things as 'RADIO' exclusivity
        if self.group != '': #if it does not have a group
            self.group_handler()

        # call the application specific handler (if none specified when
        # button is created it defaults to dummy prototype Widget.handler).
        self.app_handler(self)


        return
    def return_state(self):
        return self.state
             

class Text(Widget):

    def __init__(self,window=windowSurface,
                 color=BLACK,background_color=Widget.background_color,
                 topleft=(200,200),name= '',
                 font_size=20,max_chars=20,text='',
                 outline=True,outline_width=1,
                 justify = 'LEFT',
                 app_handler=Widget.handler):

        
        # initialize the properties
        self.window=window
        self.color= color
        self.background_color = background_color
        self.name = name
        self.font_size = font_size
        self.max_chars = max_chars
        self.text = text
        self.outline = outline
        self.outline_width = outline_width
        self.justify = justify
        self.app_handler = app_handler
        
        self.topleft=topleft
        self.left=topleft[0]    # reguired by isclicked method in Widget
        self.top=topleft[1]     # "
        
        # render a maximum size string to set size of text rectangle
        max_string = ''
        for i in range(0,max_chars):
            max_string += 'D'

        maxFont = pygame.font.SysFont(None,font_size)
        maxtext = maxFont.render(max_string,True,color)
        maxRect= maxtext.get_rect()
        maxRect.left = self.left
        maxRect.top = self.top
        self.maxRect = maxRect  # save for other references
        self.maxFont = maxFont

        # now set the rest required by isclicked method
        self.width = maxRect.right - maxRect.left
        self.height = maxRect.bottom -  maxRect.top


        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        elif (name != ''):
            print ('Error - duplicate widget name of ' + name)

        self.draw()  # invoke the method to do the draw

        return   # end of Text initializer

    # Text method to draw the text and any outline on to the screen
    def draw(self):
        # fill the maxRect to background color to wipe any prev text
        pygame.draw.rect(self.window,self.background_color,
                         (self.maxRect.left,self.maxRect.top,
                          self.width, self.height),0)

        # if outline is requested, draw the outline 4 pixels bigger than
        # max text.  Reference topleft stays as specified
        
        if self.outline:
            pygame.draw.rect(self.window,self.color,
                             (self.maxRect.left-self.outline_width-2,
                              self.maxRect.top-self.outline_width-2,
                              self.width+(2*self.outline_width)+2,
                              self.height+(2*self.outline_width)+2),
                              self.outline_width)


        # Now put the requested text within maximum rectangle
        plottext = self.maxFont.render(self.text,True,self.color)
        plotRect = plottext.get_rect()

        plotRect.top = self.top # top doesn't move with justify

        # justify the text
        if self.justify == 'CENTER':
            plotRect.left = self.left + int(plotRect.width/2) 
        elif self.justify == 'LEFT':
            plotRect.left = self.left
        elif self.justify == 'RIGHT':
            plotRect.right = self.maxRect.right
        else:
            print('Illegal justification in Text object')

        # blit the text and update screen
        self.window.blit(plottext,plotRect)

        pygame.display.update()

    # Text method to update text and redraw
    def update(self,text):
        self.text = text
        self.draw()

class Rectangle(Widget):
# class to wrap the pygame rectangle class to standardize with Widgets 

    def __init__(self, window=windowSurface,color=BLACK,
                 topleft = (200,200), width = 30, height = 20,
                 name = '',outline_width = 1, # width of outline, 0 = fill
                 app_handler=Widget.handler):

        self.window = window
        self.color = color
        self.topleft = topleft
        self.left = topleft[0]      # required by isclicked method in Widget
        self.top = topleft[1]       # "
        self.width = width          # "
        self.height = height        # "
        self.right = self.left + width
        self.bottom = self.top + height
        self.name = name
        self.outline_width = outline_width
        self.app_handler = app_handler

        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        elif (name != ''):
            print ('Error - duplicate widget name of ' + name)

        self.draw()  # invoke the draw method to draw it

        return

    def draw(self):     # Rectangle method to do the draw
        
        # get a rectangle object and draw it
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)
        pygame.draw.rect(self.window,self.color,self.rect,
                         self.outline_width)
        pygame.display.update(self.rect)

        return
    
    def handler(self):  # Rectangle handler
        self.app_handler(self)  # nothing special to do, call app_handler
        return
#Timer class
class Timer(object):

    timers = []  # create an empty list of all timers

    def process():
    # Timer processor, called from the main loop at the class
    # level to process timers
        for timer_object in Timer.timers:
            if timer_object.delay > 0.0: # timer is active
                if (time.time() - timer_object.start_time) > timer_object.delay:
                    # timer has timed out
                    timer_object.state = True
                    #timer_object.start_time = time.time()
                    if not (timer_object.handler == ''): # see if handler exists
                        timer_object.handler() # call the handler
                    if not timer_object.repeat:
                        timer_object.delay = 0.0
                    # else leave the delay in place so it will repeat

    def __init__(self,name='',handler='',repeat=False):
    # constructor for timer, must set with .set() method
        self.name = name
        self.start_time = time.time()
        self.delay = 0.0
        self.handler = ''
        self.repeat = repeat
        self.state = False  # show time not timed out
        Timer.timers += [self] # add timer object to the list of timers
        

    def set(self,delay,handler='',repeat=False):
    # set a timer, optionally associate a handler with it
        self.delay = delay    # time period in seconds
        self.handler = handler
        self.repeat = repeat
        self.start_time = time.time()

    def check_state(self):
    # check the state of the timer, return true if timed out
        return self.state

    def reset_state(self):
    # reset the state of the counter to false
        self.state = False
        
    def cancel(self):
    # cancel a timer
        self.delay = 0.0
        self.state = False
    def return_eta(self):
        #Returns the Time sence start of a timer, in secounds
        temp_eta = int(time.time() - self.start_time)
        return str(temp_eta)



        
#------------------ End of Timer Class -------------------------------------        
    


#---------------- General purpose functions not part of a class ver 0.1 ---------



def check_wall(rect):
# General purpose function to test if an  hit a wall.
# Call with a rectangle object
# Returns None if no wall struck, otherwise 'TOP','BOTTOM','RIGHT','LEFT'
    if (rect.right >= WINDOWWIDTH):
        return 'RIGHT'
    elif (rect.left <= 0):
        return 'LEFT'
    elif (rect.top <= 0):
        return 'TOP'
    elif (rect.bottom >= WINDOWHEIGHT):
        return 'BOTTOM'
    else:
        return None




def write_text(text='TEXT TEST',topleft=(200,200),font_size=50,color=YELLOW):
# General purpose function to write text on the screen
    myfont = pygame.font.SysFont(0,font_size)#setting for the font size
    label = myfont.render(text, 1,color)#("text",alias flag, color
    textrec = label.get_rect()  # get a rectangle to put it in
    textrec.left = topleft[0]  # set the position
    textrec.top = topleft[1]

    windowSurface.blit(label,textrec)#put the text rec onto the surface
    pygame.display.update()

    return  # end of write text

    return # return from update scores

#-------------Application specific setup functions not part of a class ------



def init_controls():
# Initialize the game controls and scoreboard widgets
# This is mainley a function for Loqoman, his editor makes these things easy to see
    global go
    go = Button(name='Go',color = RED,topleft=(10,10),size = 35, #Big GO button at the top
                label='Go',app_handler=go_application_handler)
    global player1
    player1 = Button(name='Player1',color=RED,
                     topleft =(WINDOWWIDTH-int(WINDOWWIDTH/3),10),size = 20,
                     label='Player 1',group='Player')
    
    player1.toggle() # set default to player 1 to True
    global player1_score
    player1_score=Text(color=RED,topleft=(player1.right+100,player1.top),
                       name='player1_score',font_size=30,max_chars=20,
                       text='Best time',justify='LEFT',outline=False)
                                          
    global player2
    player2 = Button(name='Player2',color=BLUE,
                     topleft =(player1.left,player1.bottom+10),size = 20,
                     label='Player 2',group='Player')
    global player2_score
    player2_score=Text(color=BLUE,topleft=(player2.right+100,player2.top),
                       name='player2_score',font_size=30,max_chars=20,
                       text='Best time',justify='LEFT',outline=False)
    #Clock area at the top
    global clock
    clock = Text(color=BLACK,topleft=(int(WINDOWWIDTH/2-300),10),
                  name='clock',font_size=40,max_chars=20,text='Hit go button to begin!',  
                  justify='LEFT',outline=True)
    global cheese_score
    #cheese score text
    cheese_score = Text(color=BLACK,topleft=((clock.topleft[0] - 60),700),name='score',font_size=40,
                        max_chars=20,text='Current cheese gathered:',justify='LEFT',outline=True)
    #Following are the difficulty buttons
    dif_easy = Button(name ='Easy',color = RED,
                      topleft=(10,75),size = 15,
                      label='Easy',app_handler=easy_button_handler, group='Difficulty')

    dif_normal = Button(name ='Normal',color = RED,
                      topleft=(10,dif_easy.bottom+10),size = 15,
                      label='Normal',app_handler=med_button_handler, group='Difficulty')

    dif_normal.toggle() # set default difficulty to 'Normal'

    tough = Button(name ='Tough',color = RED,
                      topleft=(10,dif_normal.bottom+10),size = 15,
                      label='Tough',app_handler=hrd_button_handler,group='Difficulty')

    dig_worst = Button(name='Horrible',color=RED,
                       topleft=(10,tough.bottom+10),size = 15,
                       label='Horrible',app_handler= hrdr_button_handler,group='Difficulty')
    global new
    new = Button(name ='New',color=RED,
                 topleft=(10,dig_worst.bottom+20),size=15,
                 label='New maze',app_handler=new_maze_handler)
                
    global current_time
    current_time = Timer(name = 'Elapsed Time: ',handler = '', repeat = False)
    
    return


#---------------End of general purpose functions --------------------#           
#---------------Button Applications handlers-------------------------#
def go_application_handler(self):
    global start
    if start == False:
        current_time.set(delay = 10000000)
        go_app_time = True
    global timeC
    timeC = 'Elapsed Time: ' + current_time.return_eta()    
    start = True
    return

def new_maze_handler(self):

    maze.build()

    # put the rat in his home room and draw him there
    rat.room = Room.rooms[Maze.starting_col][Maze.starting_row]    
    rat.draw()
    self.toggle()
    maze.store_cheese()

    new.toggle()
def easy_button_handler(self): #Changing the global var, difficulty to E for easy, M for medium, H for hard, and H+ for really hard
    Maze.difficulty = 'E'
def med_button_handler(self):
    Maze.difficulty = 'M'
def hrd_button_handler(self):
    Maze.difficulty = 'H'
def hrdr_button_handler(self):
    Maze.difficulty = 'H+' 
    

#----------------Main portion of the program ver 0.2 ----------------#
# Initialize things before the loop
pygame.key.set_repeat(50,50)
init_controls()


maze = Maze()

maze.build()  # Build maze with medium difficulty default

maze.store_cheese()

rat = Robot_Rat(color=RED)
#Which player has gone
player1_loop = False
player2_loop = False
high_score1 = 10000000
high_score2 = 10000000
global start
start =     True
#Varible to tell when the user has clicked the go button
              #I would like to have put this inside the init function for the widgets, however that makes it a local var :(
#  Main game loop, runs until window x'd out or someone wins

while True:
    if start == True:
        currentTimer = current_time.return_eta() #The current time, in secounds
        timeC = 'Elapsed Time: ' +  currentTimer #TimeC is the var to hold the clock time. It means time[Clock]
        clock.update(timeC) #Updating the clock
        cheese_score.update('Current cheese gathered:' + str(rat.cheese_num())) #updating the cheese score
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if start == True:

            if event.type is KEYDOWN:

                key = pygame.key.name(event.key) 

                if(key == 'd'): #Large key tree to see what key we are pressing and what to do with that key
                    rat.move('E')
                elif(key == 's'): 
                    rat.move('S')
                elif(key == 'a'):
                    rat.move('W')
                elif(key == 'w'):  
                    rat.move('N')
                    #Next is all arrows
                elif(key == 'up'):
                    rat.move('N')
                elif(key == 'left'):
                    rat.move('W')
                elif(key == 'right'):
                    rat.move('E')
                elif(key == 'down'):
                    rat.move('S')
        if event.type == MOUSEBUTTONDOWN:                
                for widgetname in Widget.widgetlist: #For every widget we have ever created

                    widget_object = Widget.find_widget(widgetname) #Temp varible for the widget name 
                    pos = pygame.mouse.get_pos() # mouse clicked get (x, y)

                    if widget_object.isclicked(pos): #isclicked, to see if something is clicked.

                        widget_object.handler()#Well, its clicked, so do the self.handler()
    '''if player1_loop == False: #If player 1 is going
        if ( (rat.cheese_num() >= maze.number_cheeses) &
         (rat.room == Room.rooms[Maze.starting_col][Maze.starting_row]) ): #wait untill they have all the cheese and are at the begginiing
            start = False
            if int(currentTimer) < high_score1:
                high_score1 = int(currentTimer)
            player1_score.update('Best time: ' + str(high_score1))
            player1_loop = True #Meaning if they have gone or not, in this case, this is saying that player1 HAS gone 
            rat.change_color(BLUE)
            maze.store_cheese()
            rat.reset_cheese()
            go.toggle() #Re toggling the go button
            rat.change_color(BLUE)
            pygame.display.update()
            player2_loop = False
            player1.toggle()
            player2.toggle()
    elif player2_loop == False: #If player 2 is going
        if ( (rat.cheese_num() >= maze.number_cheeses) &
         (rat.room == Room.rooms[Maze.starting_col][Maze.starting_row]) ):
            start = False
            if int(currentTimer) < high_score2:
                high_score2 = int(currentTimer)
            player2_score.update('Best time: ' + str(high_score2))
            player1_loop = False
            rat.change_color(RED)
            rat.reset_cheese()
            maze.store_cheese()
            go.toggle()
            player1.toggle()
            player2.toggle()
            rat.change_color(RED)'''
    rat.auto_move()
    Timer.process()
    pygame.display.update()
    time.sleep(.1)
    


sys.exit() # shouldn't ever get here.  Exit is in main loop.
        

