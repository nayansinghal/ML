from gridworld import *
from qlearningAgents import *
import graphicsGridworldDisplay

if __name__ == '__main__':
	width = 10
	height = 2

	grid = Gridworld(width, height, "dynamic_obstacle")
	grid.makeGrid()
	agent = QLearningAgent(grid)

	NumOfEpisode = 200

	display = graphicsGridworldDisplay.GraphicsGridworldDisplay(grid, 120, 1)

	for episode in range(0, NumOfEpisode):
		grid.runEpisode(agent, episode, display)

	dynamic_state = ['W', 'D','']
	actions = ['north','east','south']
	for action in actions:
		for i in range(0,3):
			for j in range(0,3):
				state = dynamic_state[i], dynamic_state[j]
				print((dynamic_state[i], dynamic_state[j], action) ,agent.getQvalueUsingDynObstacle(state, action))
	#agent.setEpsilon(0.0)
	#for episode in range(0, NumOfEpisode):
	#	grid.runEpisode(agent, episode, display)