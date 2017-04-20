import random,util,math
from gridworld import *;
          
class QLearningAgent():
  def __init__(self, grid):
    self.QValuesWalk = util.Counter()
    self.grid = grid
    self.epsilon = 0.05
    self.alpha = 1
    self.gamma = 0.8

  def updateEpsilon(self):
    self.epsilon = self.epsilon * 0.99

  def setEpsilon(self, value):
    self.epsilon = 0.0

  def getQvalueUsingDynObstacle(self, env, action):
    return self.QValuesWalk[(env, action)]

  def getQValue(self, state, action):
    if self.grid.qtype == "walk":
      return self.QValuesWalk[(state,action)]
    elif self.grid.qtype == "obstacle":
      env = self.grid.getEnvironment(state)
      return self.QValuesWalk[(env,action)]
    elif self.grid.qtype == "dynamic_obstacle":
      env = self.grid.getEnvironment(state)
      return self.QValuesWalk[(env, action)]
  
  def getValue(self, state):
    actions = self.grid.getPossibleActions(state)
    if len(actions) < 1:
      return 0.0

    return max([self.QValuesWalk[(state, action)] for action in actions])
    
  def getPolicy(self, state):
    maxqval=float("-inf")
    bestAction=[]
    actions = self.grid.getPossibleActions(state)
    if len(actions)==0:
      return None
    env = self.grid.getEnvironment(state)
    for action in actions:
      qValue = self.QValuesWalk[(env,action)]
      if qValue > maxqval:
        maxqval=qValue
        bestAction=[action]
      elif qValue==maxqval:
        bestAction.append(action)
    return random.choice(bestAction)
    
  def getAction(self, state):
    # Pick Action
    legalActions = self.grid.getPossibleActions(state)
    action = None
    
    if len(legalActions)==0:
      return action
    if util.flipCoin(self.epsilon):
      return random.choice(legalActions)
    else:
      return self.getPolicy(state)
  
  def update(self, state, action, nextState, reward):

    if state=="TERMINAL_STATE":
      return
    env = self.grid.getEnvironment(state)
    nextenv = self.grid.getEnvironment(nextState)
    oldQsa = self.QValuesWalk[(env, action)]
    nextActions = self.grid.getPossibleActions(nextState)
    if len(nextActions)==0:
      maxFutureValue=self.QValuesWalk[(nextenv, action)]
    else:
      maxFutureValue=max([self.QValuesWalk[(nextenv, nextAction)] for nextAction in nextActions])
    self.QValuesWalk[(env, action)] = oldQsa + self.alpha * ( reward + self.gamma * (maxFutureValue) - oldQsa )