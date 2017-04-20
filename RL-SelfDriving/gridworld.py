import random
import util
from qlearningAgents import *
import graphicsGridworldDisplay

class Gridworld():
  """
    Gridworld
  """
  def __init__(self, width, height, qtype):
    self.width = width
    self.height = height
    # 10 X 4 , where (0,0) x++ will takes you to (1,0)
    self.data = [['' for y in range(height)] for x in range(width)]
    self.terminalState = 'TERMINAL_STATE'
    self.noise = 0.2
    self.state = (0,0)
    self.startState = (0,0)
    self.qtype = qtype
    self.dynamicCars = []
    self.trafficLights = []
    self.trafficColors = {'R':0, 'Y':1, 'G':2, '2':'G', '1':'Y', '0':'R'}

  def getStartState(self):
    return self.startState

  def isTerminal(self, state):
    return state == self.terminalState

  def getCurrentState(self):
    return self.state

  def reset(self):
    self.state = self.getStartState()

  def makeGrid(self):
      #self.data[self.width - 1][0] = 'e'

      if self.qtype == "obstacle":
        self.data[2][0] = 'O'
        self.data[4][1] = 'O'
        self.data[6][0] = 'O'

      if self.qtype == "dynamic_obstacle":
        self.dynamicCars.append([0,1])
        self.dynamicCars.append([5, 1])
        for cars in self.dynamicCars:
          self.data[cars[0]][cars[1]] = 'D'

      if self.qtype == "trafficLight":
        self.trafficLights.append([5,0])
        for trafficLight in self.trafficLights:
          self.data[trafficLight[0]][trafficLight[1]] = 'R'

  def getTrafficEnv(self, state):
    trafLightSts = ''

    x,y = state
    if (x == self.width - 1):
      trafLightSts = ''
    elif (self.data[x+1][1] == 'R' or self.data[x + 1][0] == 'R'):
      trafLightSts = 'R'
    elif (self.data[x+1][1] == 'Y' or self.data[x+1][0] == 'Y'):
      trafLightSts = 'Y'
    elif (self.data[x + 1][1] == 'G' or self.data[x + 1][0] == 'G'):
      trafLightSts = 'G'
    else:
      trafLightSts = ''

    return trafLightSts

  def updateTrafficEnv(self):
    for trafficLight in self.trafficLights:
      x,y = trafficLight[0], trafficLight[1]
      self.data[x][y] = self.trafficColors[str((int(self.trafficColors[self.data[x][y]]) + 1)%3)]

  def getObstacleEnv(self, state):
      north = ' '
      south = ' '
      east = ' '
      west = ' '

      x,y = state
      if (y == self.height - 1):
        north = 'w'
      else:
        north = self.data[x][y + 1]

      if (y == 0):
        south = 'w'
      else:
        south = self.data[x][y-1]

      if (x == self.width - 1):
        east = 'w'
      else:
        east = self.data[x+1][y]

      if (x == 0):
        west = 'w'
      else:
        west = self.data[x-1][y]

      static_env = (north, east, south, west)
      return static_env

  def getDynObsEnv(self, state):
    backward = ''
    same = ''

    x, y = state
    if (y == self.height - 1):
      backward = 'W'
      same = 'W'
    elif (x == 0):
      backward = 'W'
      same = self.data[x][1] if self.data[x][1] is '' or self.data[x][1] is 'D' else ''
    else:
      backward = self.data[x-1][1] if self.data[x-1][1] is '' or self.data[x-1][1] is 'D' else ''
      same = self.data[x][1] if self.data[x][1] is '' or self.data[x][1] is 'D' else ''

    dynamice_env = (backward, same)
    return dynamice_env

  def getEnvironment(self, state):
    if state == self.terminalState:
      return None
    elif self.qtype == "walk":
      return state
    elif self.qtype == "obstacle":
      return self.getObstacleEnv(state)
    elif self.qtype == "dynamic_obstacle":
      return self.getDynObsEnv(state)
    elif self.qtype == "trafficLight":
      return self.getTrafficEnv(state)

  def updateEnvironment(self):

    dynamicCars =[]
    for cars in self.dynamicCars:
      self.data[cars[0]][cars[1]] = ''
      x = cars[0] + 1 if cars[0] + 1 < self.width else 0
      self.data[x][cars[1]] = 'D'
      dynamicCars.append([x,cars[1]])
    self.dynamicCars = dynamicCars

  def getPossibleActions(self, state):
    if state == self.terminalState:
      return ()
    x,y = state

    if x==(self.width-1) and y ==(0):
      return ('exit',)
    return ('north','east','south', 'stop')
    
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
        
  def getReward(self, state, action, nextState):
    
    if state == self.terminalState:
        return 0.0

    if self.qtype == "obstacle":
      if nextState != self.terminalState:
        x,y = nextState
        if self.data[x][y] == 'O':
          return -5.0
        elif x==(self.width-1) and y ==(0):
          return 10

    elif self.qtype == "dynamic_obstacle":
      if nextState != self.terminalState:
        x,y = nextState
        for cars in self.dynamicCars:
          dynCarX, dynCarY = cars[0], cars[1]
          dynCarX = cars[0] + 1 if cars[0] + 1 < self.width else 0
          if x == dynCarX and y == dynCarY:
            return -5.0
        if x==(self.width-1) and y ==(0):
          return 10

    elif self.qtype == "trafficLight":
      if nextState != self.terminalState:
        x, y = nextState
        for trafficLight in self.trafficLights:
          trafficX, trafficY = trafficLight[0], trafficLight[1]
          if x == trafficX and y == trafficY and (self.data[trafficX][trafficY] == 'R' or self.data[trafficX][trafficY] == 'Y'):
            return -5.0
          else:
            return 10.0
        if x == (self.width - 1) and y == (0):
          return 10

    if action=='east':
      return 0.5
    else:
      return -0.5

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
    elif(y1==y2 and x2==x1):
      action = 'stop'
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
        reward = self.getReward(state, action, nextState)
        self.state = nextState
        return (nextState, reward, action)
    raise 'Total transition probability less than one; sample failure.'

  def runEpisode(self, agent, episode, display):

    returns = 0
    totalDiscount = 1.0
    self.reset()
    display.start()
    iter = 0

    print ("BEGINNING EPISODE: "+str(episode)+"\n")
    while True:

      # DISPLAY CURRENT STATE
      print ("ITERATION: " + str(iter) + "\n")
      iter += 1

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
      self.updateEnvironment()
      self.updateTrafficEnv()
      agent.updateEpsilon()
      print 'color:', self.data[5][0]

  def getTransitionStatesAndProbs(self, state, action):
    if action not in self.getPossibleActions(state):
      raise "Illegal action!"

    if self.isTerminal(state):
      return []

    x, y = state

    if x == (self.width - 1) and y == (0):
      termState = self.terminalState
      return [(termState, 1.0)]

    successors = []

    northState = (self.__isAllowed(y + 1, x) and (x, y + 1)) or state
    # westState = (self.__isAllowed(y,x-1) and (x-1,y)) or state
    southState = (self.__isAllowed(y - 1, x) and (x, y - 1)) or state
    eastState = (self.__isAllowed(y, x + 1) and (x + 1, y)) or state

    if action == 'north' or action == 'south':
      if action == 'north':
        successors.append((northState, 1 - self.noise))
      else:
        successors.append((southState, 1 - self.noise))

      massLeft = self.noise
      # successors.append((westState,massLeft/2.0))
      successors.append((eastState, massLeft / 1.0))

    if action == 'west' or action == 'east':
      if action == 'east':
        successors.append((eastState, 1 - self.noise))
      # else:
      #  successors.append((eastState,1-self.noise))

      massLeft = self.noise
      successors.append((northState, massLeft / 2.0))
      successors.append((southState, massLeft / 2.0))

    if action == 'stop':
      successors.append(((x,y), 1.0))

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