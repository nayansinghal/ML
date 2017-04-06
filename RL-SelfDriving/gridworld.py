import random
import util
from qlearningAgents import *
import graphicsGridworldDisplay

class Gridworld():
  """
    Gridworld
  """
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.data = [[0 for y in range(height)] for x in range(width)]
    self.terminalState = 'TERMINAL_STATE'
    self.noise = 0.2
    self.state = (0,0)
    self.startState = (0,0)
    #self.data[width-1][height-1]=10

  def makeGrid(self):
    for h in range(self.height):
        self.data[self.width - 1][h] = 10

  def getPossibleActions(self, state):
    if state == self.terminalState:
      return ()
    x,y = state

    if x==(self.width-1):
      return ('exit',)
    return ('north','east','south','west')
    
  def getStates(self):
    """
    Return list of all states.
    """
    # The true terminal state.
    states = [self.terminalState]
    for x in range(self.width):
      for y in range(self.height):
          state = (x,y)
          states.append(state)
    return states
        
  def getReward(self, state, action):
    
    if state == self.terminalState:
        return 0.0

    if action=='east':
      return 0.5
    else:
      return -0.5

  def getStartState(self):
      return self.startState
    
  def isTerminal(self, state):
    return state == self.terminalState

  def getTransitionStatesAndProbs(self, state, action):   
        
    if action not in self.getPossibleActions(state):
      raise "Illegal action!"
      
    if self.isTerminal(state):
      return []
    
    x, y = state
    
    if x==(self.width-1):
      termState = self.terminalState
      return [(termState, 1.0)]
      
    successors = []                
                
    northState = (self.__isAllowed(y+1,x) and (x,y+1)) or state
    westState = (self.__isAllowed(y,x-1) and (x-1,y)) or state
    southState = (self.__isAllowed(y-1,x) and (x,y-1)) or state
    eastState = (self.__isAllowed(y,x+1) and (x+1,y)) or state
                        
    if action == 'north' or action == 'south':
      if action == 'north': 
        successors.append((northState,1-self.noise))
      else:
        successors.append((southState,1-self.noise))
                                
      massLeft = self.noise
      successors.append((westState,massLeft/2.0))
      successors.append((eastState,massLeft/2.0))
                                
    if action == 'west' or action == 'east':
      if action == 'west':
        successors.append((westState,1-self.noise))
      else:
        successors.append((eastState,1-self.noise))
                
      massLeft = self.noise
      successors.append((northState,massLeft/2.0))
      successors.append((southState,massLeft/2.0))
      
    successors = self.__aggregate(successors)
                                                                           
    return successors                                
  
  def __aggregate(self, statesAndProbs):
    counter = util.Counter()
    for state, prob in statesAndProbs:
      counter[state] += prob
    newStatesAndProbs = []
    for state, prob in counter.items():
      newStatesAndProbs.append((state, prob))
    return newStatesAndProbs
        
  def __isAllowed(self, y, x):
    if y < 0 or y >= self.height: return False
    if x < 0 or x >= self.width: return False
    return True;
            
  def getCurrentState(self):
    return self.state
               
  def inferAction(self, state, nextState):
    if nextState=="TERMINAL_STATE": #state=="TERMINAL_STATE" or 
      return None
    x1, y1 = state
    x2, y2 = nextState
    action=None
    if(x1==x2 and y2==y1+1):
      action='north'
    elif(x1==x2 and y2==y1-1):
      action='south'
    elif(y1==y2 and x2==x1+1):
      action='east'
    elif(y1==y2 and x2==x1-1):
      action='west'
    return action

  def doAction(self, action):
    successors = self.getTransitionStatesAndProbs(self.state, action) 
    sum = 0.0
    rand = random.random()
    state = self.getCurrentState()
    for nextState, prob in successors:
      sum += prob
      if sum > 1.0:
        raise 'Total transition probability more than one; sample failure.' 
      if rand < sum:
        tookAction = self.inferAction(state, nextState)
        if tookAction!=None:
          action=tookAction
        reward = self.getReward(state, action)
        self.state = nextState
        return (nextState, reward, action)
    raise 'Total transition probability less than one; sample failure.'    
        
  def reset(self):
    self.state = self.getStartState()

  def runEpisode(self, agent, episode, display):

    returns = 0
    totalDiscount = 1.0
    self.reset()
    display.start()

    print ("BEGINNING EPISODE: "+str(episode)+"\n")
    while True:

      # DISPLAY CURRENT STATE
      state = self.getCurrentState()
      display.displayQValues(agent, state)

      # END IF IN A TERMINAL STATE
      actions = self.getPossibleActions(state)
      if len(actions) == 0:
        print ("EPISODE "+str(episode)+" COMPLETE: RETURN WAS "+str(returns)+"\n")
        return returns

      # GET ACTION (USUALLY FROM AGENT)
      action = agent.getAction(state)
      if action == None:
        raise 'Error: Agent returned None action'

      # EXECUTE ACTION
      nextState, reward, action2 = self.doAction(action)
      print("Started in state: "+str(state)+
              "\nSpecified action: "+str(action)+
              "\nTook action: "+str(action2)+
              "\nEnded in state: "+str(nextState)+
              "\nGot reward: "+str(reward)+"\n")
      # UPDATE LEARNER
      agent.update(state, action2, nextState, reward)
 