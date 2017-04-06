from gridworld import *
from qlearningAgents import *
import graphicsGridworldDisplay

if __name__ == '__main__':
	width = 10
	height = 2

	grid = Gridworld(width, height)
	grid.makeGrid()
	agent = QLearningAgent(grid)

	NumOfEpisode = 20

	display = graphicsGridworldDisplay.GraphicsGridworldDisplay(grid, 120, 1)

	for episode in range(0, NumOfEpisode):
		grid.runEpisode(agent, episode, display)