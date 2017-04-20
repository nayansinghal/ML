from gridworld import *
from qlearningAgents import *
import graphicsGridworldDisplay

def printDynObstaclesQValues(grid, agent):
	dynamic_state = ['W', 'D', '']
	actions = ['north', 'east', 'south', 'stop']
	for action in actions:
		for i in range(0, 3):
			for j in range(0, 3):
				state = dynamic_state[i], dynamic_state[j]
				print((dynamic_state[i], dynamic_state[j], action), agent.getQvalueUsingDynObstacle(state, action))

def printTrafficLightsQValues(grid, agent):
	traffic_states = ['R', 'Y', 'G', '','W']
	actions = ['north', 'east', 'south', 'stop']
	for action in actions:
		for trafficSignal in traffic_states:
				print((trafficSignal, action), agent.getQvalueUsingDynObstacle(trafficSignal, action))

if __name__ == '__main__':
	width = 10
	height = 2

	grid = Gridworld(width, height, "trafficLight")
	grid.makeGrid()
	agent = QLearningAgent(grid)

	NumOfEpisode = 100

	display = graphicsGridworldDisplay.GraphicsGridworldDisplay(grid, 120, 1)

	for episode in range(0, NumOfEpisode):
		grid.runEpisode(agent, episode, display)

	printTrafficLightsQValues(grid, agent)

	#agent.setEpsilon(0.0)
	#for episode in range(0, NumOfEpisode):
	#	grid.runEpisode(agent, episode, display)