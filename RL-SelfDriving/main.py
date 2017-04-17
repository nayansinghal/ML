from gridworld import *
from qlearningAgents import *
import graphicsGridworldDisplay

if __name__ == '__main__':
	width = 10
	height = 2

	grid = Gridworld(width, height, "obstacle")
	grid.makeGrid()
	agent = QLearningAgent(grid)

	NumOfEpisode = 200

	display = graphicsGridworldDisplay.GraphicsGridworldDisplay(grid, 120, 1)

	for episode in range(0, NumOfEpisode):
		grid.runEpisode(agent, episode, display)

	agent.setEpsilon(0.0)
	for episode in range(0, NumOfEpisode):
		grid.runEpisode(agent, episode, display)