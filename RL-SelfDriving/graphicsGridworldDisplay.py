import util
from graphicsUtils import *

class GraphicsGridworldDisplay:
  
  def __init__(self, gridworld, size=120, speed=1.0):
    self.gridworld = gridworld
    self.size = 120
    self.speed = 0.1
    
  def start(self):
    setup(self.gridworld, size=self.size)
  
  def pause(self):
    wait_for_keys()

  def displayQValues(self, agent, currentState = None, message = 'Agent Q-Values'):
    qValues = util.Counter()
    states = self.gridworld.getStates()
    for state in states:
      for action in self.gridworld.getPossibleActions(state):
        qValues[(state, action)] = agent.getQValue(state, action)
    drawQValues(self.gridworld, qValues, currentState, message)
    sleep(0.05 / self.speed)

BACKGROUND_COLOR = formatColor(0,0,0)    
EDGE_COLOR = formatColor(1,1,1)
OBSTACLE_COLOR = formatColor(0.5,0.5,0.5)
TEXT_COLOR = formatColor(1,1,1)
MUTED_TEXT_COLOR = formatColor(0.7,0.7,0.7)
LOCATION_COLOR = formatColor(0,1,1)
DYNAMIC_CAR_COLOR = formatColor(1,0.4, 0.7)
RED = formatColor(1,0,0)
YELLOW = formatColor(1,1,0)
GREEN = formatColor(0.5, 1.0, 0)

WINDOW_SIZE = -1
GRID_SIZE = -1
GRID_HEIGHT = -1
MARGIN = -1

def setup(gridworld, title = "Gridworld Display", size = 120):
  global GRID_SIZE, MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT
  grid = gridworld
  WINDOW_SIZE = size
  GRID_SIZE = size
  GRID_HEIGHT = grid.height
  MARGIN = GRID_SIZE * 0.75
  screen_width = (grid.width - 1) * GRID_SIZE + MARGIN * 2
  screen_height = (grid.height - 0.5) * GRID_SIZE + MARGIN * 2

  begin_graphics(screen_width,
                 screen_height,
                 BACKGROUND_COLOR, title=title)

def drawQValues(gridworld, qValues, currentState = None, message = 'State-Action Q-Values'):
  grid = gridworld
  blank()
  stateCrossActions = [[(state, action) for action in gridworld.getPossibleActions(state)] for state in gridworld.getStates()]
  qStates = reduce(lambda x,y: x+y, stateCrossActions, [])
  qValueList = [qValues[(state, action)] for state, action in qStates] + [0.0]
  minValue = min(qValueList)
  maxValue = max(qValueList)
  for x in range(grid.width):
    for y in range(grid.height):
      state = (x, y)
      gridType = grid.data[x][y]
      isExit = (str(gridType) == 'e') or (x == grid.width - 1 and y == 0)
      isCurrent = (currentState == state)
      actions = gridworld.getPossibleActions(state)
      if actions == None or len(actions) == 0:
        actions = [None]
      bestQ = max([qValues[(state, action)] for action in actions])
      bestActions = [action for action in actions if qValues[(state, action)] == bestQ]

      q = util.Counter()
      valStrings = {}
      for action in actions:
        v = qValues[(state, action)]
        if v is None:
          v = 0
        q[action] += v
        valStrings[action] = '%.2f' % v
      if gridType == 'O':
        drawSquare(x, y, 0, 0, 0, None, None, True, False, isCurrent, False)
      elif gridType == 'D':
        drawSquare(x, y, 0, 0, 0, None, None, False, False, isCurrent, True)
      elif gridType == 'R':
        drawSquare(x, y, 0, 0, 0, None, None, False, False, isCurrent, False, (RED, OBSTACLE_COLOR, OBSTACLE_COLOR))
      elif gridType == 'Y':
        drawSquare(x, y, 0, 0, 0, None, None, False, False, isCurrent, False, (OBSTACLE_COLOR, YELLOW, OBSTACLE_COLOR))
      elif gridType == 'G':
        drawSquare(x, y, 0, 0, 0, None, None, False, False, isCurrent, False, (OBSTACLE_COLOR, OBSTACLE_COLOR, GREEN))
      elif isExit:
        action = 'exit'
        value = q[action]
        valString = '%.2f' % value
        drawSquare(x, y, value, minValue, maxValue, "end", action, False, isExit, isCurrent, False)
      else:
        drawSquareQ(x, y, q, minValue, maxValue, valStrings, actions, isCurrent)
  pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
  text( pos, TEXT_COLOR, message, "Courier", -28, "bold", "c")


def blank():
  clear_screen()
      
def drawSquare(x, y, val, min, max, valStr, action, isObstacle, isTerminal, isCurrent, isDynamicObstacle, TrafficColor = None):

  square_color = getColor(val, min, max)
  
  if isObstacle:
    square_color = OBSTACLE_COLOR
    
  (screen_x, screen_y) = to_screen((x, y))

  square( (screen_x, screen_y), 
                 0.5* GRID_SIZE, 
                 color = square_color,
                 filled = 1,
                 width = 1)
  square( (screen_x, screen_y), 
                 0.5* GRID_SIZE, 
                 color = EDGE_COLOR,
                 filled = 0,
                 width = 3)

  if isTerminal and not isObstacle:
    square( (screen_x, screen_y), 
                 0.4* GRID_SIZE, 
                 color = EDGE_COLOR,
                 filled = 0,
                 width = 2)

  if action == 'north':
    polygon( [(screen_x, screen_y - 0.45*GRID_SIZE), (screen_x+0.05*GRID_SIZE, screen_y-0.40*GRID_SIZE), (screen_x-0.05*GRID_SIZE, screen_y-0.40*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
  if action == 'south':
    polygon( [(screen_x, screen_y + 0.45*GRID_SIZE), (screen_x+0.05*GRID_SIZE, screen_y+0.40*GRID_SIZE), (screen_x-0.05*GRID_SIZE, screen_y+0.40*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
  if action == 'west':
    polygon( [(screen_x-0.45*GRID_SIZE, screen_y), (screen_x-0.4*GRID_SIZE, screen_y+0.05*GRID_SIZE), (screen_x-0.4*GRID_SIZE, screen_y-0.05*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
  if action == 'east':
    polygon( [(screen_x+0.45*GRID_SIZE, screen_y), (screen_x+0.4*GRID_SIZE, screen_y+0.05*GRID_SIZE), (screen_x+0.4*GRID_SIZE, screen_y-0.05*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)

  
  text_color = TEXT_COLOR

  if not isObstacle and isCurrent:
    circle( (screen_x, screen_y), 0.1*GRID_SIZE, outlineColor=LOCATION_COLOR, fillColor=LOCATION_COLOR )

  if isDynamicObstacle:
    circle((screen_x, screen_y), 0.1 * GRID_SIZE, outlineColor=DYNAMIC_CAR_COLOR, fillColor=DYNAMIC_CAR_COLOR)

  if not isObstacle:
    text( (screen_x, screen_y), text_color, valStr, "Courier", -26, "bold", "c")

  if TrafficColor != None:
    circle((screen_x - 0.3*GRID_SIZE, screen_y +0.10*GRID_SIZE), 0.04 * GRID_SIZE, outlineColor=TrafficColor[0], fillColor=TrafficColor[0])
    circle((screen_x - 0.3 * GRID_SIZE, screen_y + 0.20 * GRID_SIZE), 0.04 * GRID_SIZE, outlineColor=TrafficColor[1], fillColor=TrafficColor[1])
    circle((screen_x - 0.3 * GRID_SIZE, screen_y + 0.30 * GRID_SIZE), 0.04 * GRID_SIZE, outlineColor=TrafficColor[2], fillColor=TrafficColor[2])
    square((screen_x - 0.3 * GRID_SIZE, screen_y + 0.20 * GRID_SIZE), 0.18 * GRID_SIZE, color=EDGE_COLOR, filled=0, width=2)
    square((screen_x - 0.3 * GRID_SIZE, screen_y + 0.45 * GRID_SIZE), 0.06 * GRID_SIZE, color=EDGE_COLOR, filled=0, width=2)

def drawSquareQ(x, y, qVals, minVal, maxVal, valStrs, bestActions, isCurrent):

  (screen_x, screen_y) = to_screen((x, y))
  
  center = (screen_x, screen_y)
  nw = (screen_x-0.5*GRID_SIZE, screen_y-0.5*GRID_SIZE)
  ne = (screen_x+0.5*GRID_SIZE, screen_y-0.5*GRID_SIZE)
  se = (screen_x+0.5*GRID_SIZE, screen_y+0.5*GRID_SIZE)
  sw = (screen_x-0.5*GRID_SIZE, screen_y+0.5*GRID_SIZE)
  n = (screen_x, screen_y-0.5*GRID_SIZE+5)
  s = (screen_x, screen_y+0.5*GRID_SIZE-5)
  w = (screen_x-0.5*GRID_SIZE+5, screen_y)
  e = (screen_x+0.5*GRID_SIZE-5, screen_y)

  '''
  actions = qVals.keys()
  for action in actions:

    wedge_color = getColor(qVals[action], minVal, maxVal)

    if action == 'north':
      polygon( (center, nw, ne), wedge_color, filled = 1, smoothed = False)
      #text(n, text_color, valStr, "Courier", 8, "bold", "n")
    if action == 'south':
      polygon( (center, sw, se), wedge_color, filled = 1, smoothed = False)
      #text(s, text_color, valStr, "Courier", 8, "bold", "s")
    if action == 'east':
      polygon( (center, ne, se), wedge_color, filled = 1, smoothed = False)
      #text(e, text_color, valStr, "Courier", 8, "bold", "e")
    if action == 'west':
      polygon( (center, nw, sw), wedge_color, filled = 1, smoothed = False)
      #text(w, text_color, valStr, "Courier", 8, "bold", "w")
    '''

  square( (screen_x, screen_y),
                 0.5* GRID_SIZE, 
                 color = EDGE_COLOR,
                 filled = 0,
                 width = 3)
  #line(ne, sw, color = EDGE_COLOR)
  #line(nw, se, color = EDGE_COLOR)

  if isCurrent:
    circle( (screen_x, screen_y), 0.1*GRID_SIZE, LOCATION_COLOR, fillColor=LOCATION_COLOR )

  '''
  for action in actions:
    text_color = TEXT_COLOR
    if qVals[action] < max(qVals.values()): text_color = MUTED_TEXT_COLOR
    valStr = ""
    if action in valStrs:
      valStr = valStrs[action]
    h = -16
    if action == 'north':
      #polygon( (center, nw, ne), wedge_color, filled = 1, smooth = 0)
      text(n, text_color, valStr, "Courier", h, "bold", "n")
    if action == 'south':
      #polygon( (center, sw, se), wedge_color, filled = 1, smooth = 0)
      text(s, text_color, valStr, "Courier", h, "bold", "s")
    if action == 'east':
      #polygon( (center, ne, se), wedge_color, filled = 1, smooth = 0)
      text(e, text_color, valStr, "Courier", h, "bold", "e")
    if action == 'west':
      #polygon( (center, nw, sw), wedge_color, filled = 1, smooth = 0)
      text(w, text_color, valStr, "Courier", h, "bold", "w")
    '''

def getColor(val, minVal, max):
  r, g = 0.0, 0.0
  if val < 0 and minVal < 0:
    r = val * 0.65 / minVal
  if val > 0 and max > 0:
    g = val * 0.65 / max
  return formatColor(r,g,0.0)


def square(pos, size, color, filled, width):
  x, y = pos
  dx, dy = size, size
  return polygon([(x - dx, y - dy), (x - dx, y + dy), (x + dx, y + dy), (x + dx, y - dy)], outlineColor=color, fillColor=color, filled=filled, width=width, smoothed=False)
  
  
def to_screen(point):
  ( gamex, gamey ) = point
  x = gamex*GRID_SIZE + MARGIN  
  y = (GRID_HEIGHT - gamey - 1)*GRID_SIZE + MARGIN  
  return ( x, y )