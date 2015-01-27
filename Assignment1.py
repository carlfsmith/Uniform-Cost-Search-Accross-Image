'''
Created on Jan 19, 2015

@author: Carl
'''
import heapq
from functools import total_ordering
from PIL import Image
from _heapq import heappush, heappop

@total_ordering
class MyState:
    def __init__(self, cost, par, x, y):
        self.cost = cost     #double
        self.parent = par    #MyState
        self.x = x           #int
        self.y = y           #int
    
    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
    
    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.cost < other.cost
    
    def __hash__(self):
        return hash((self.x, self.y))
    
def options(state, width, height):
    directions = [(state.x-1, state.y), (state.x, state.y-1), 
                  (state.x, state.y+1), (state.x+1, state.y)]
    actions = []
    for i in range(len(directions)):
        x, y = directions[i][0], directions[i][1]
        if x >= 0 and x < width:   
            if y >= 0 and y < height:    
                if state.parent == None or ((x, y) != (state.parent.x, state.parent.y)):
                    actions.append((x, y))
    return actions
    
def transition(state, action, pixels):
    x, y = action[0], action[1]
    child = MyState(None, state, x, y)
    return child

def action_cost(state, action, pixels):      # the G from RGB value
    x, y = action[0], action[1]
    color = pixels[x, y]
    cost = color[1]         # the G from RGB value
    return cost

def drawpath(goal, image):
    prev = goal
    pixels = image.load()
    while prev != None:
        pixels[prev.x, prev.y] = (255, 0, 0)
        prev = prev.parent

def uniform_cost_search(startState, goalState, image):
    frontier = []  # lowest cost comes out first
    startState.cost = 0.0
    startState.parent = None
    heappush(frontier, startState)
    beenthere = {startState : 0}  
       
    width, height = image.size
    pixels = image.load()
      
    it = 0  
    while len(frontier) > 0:
        s = heappop(frontier)    #Mystate
        if s == goalState:    #return state which reached goal
            return s
        actions = options(s, width, height)
        if ((it % 5000) < 1000):
            pixels[s.x, s.y] = (0, 255, 0)
        it+=1 
        for a in actions:
            child = transition(s, a, pixels)       # compute the next state
            acost = action_cost(s, a, pixels)      # compute the cost of the action
            
            c_cost = beenthere.get(child)
            if c_cost != None:               #if child is inside of beenthere
                if s.cost + acost < c_cost:
                    child.cost = s.cost + acost
                    child.parent = s;
                    beenthere[child] = child.cost
            else:
                child.cost = s.cost + acost;
                child.parent = s;
                heappush(frontier, child)  
                beenthere[child] = child.cost  
    raise Exception("No path to traverse")
 
startState = MyState(0, None, 100, 100)
goalState = MyState(0, None, 400, 400)
image = Image.open('terrain.png')
if image.mode != 'RGB':
    image = image.convert('RGB')
goal = uniform_cost_search(startState, goalState, image)
drawpath(goal, image)
image.save('path.png')
  

