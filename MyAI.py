# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		self.rows = rowDimension
		self.cols = colDimension
		self.mines = totalMines
		self.moves = {}
		self.safe_moves = set()
		self.safe_moves.add((startX, startY))
		self.flags = set()
		self.uncovered = set()
		self.frontier = set()
		#print(startX, startY)
		self.board = [[-1] * self.cols for i in range(self.rows)]
		#self.neighbors = set()
		self.currX = startX
		self.currY = startY
	
	def getNeighbors(self, x, y):
		neighbors = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				temp_x, temp_y = x + i, y + j
				if (0 <= temp_x < self.rows and 0 <= temp_y < self.cols 
						and (temp_x != x or temp_y != y)):
					#print(f"Adding neighbor {(temp_x + 1, temp_y + 1)}")
					neighbors.append((temp_x, temp_y))
		return neighbors

	def getFlags(self, neighbors):
		return sum(1 for n in neighbors if n in self.flags)

	def updateFrontier(self):
		for (x,y), num in self.moves.items():
			neighbors = self.getNeighbors(x,y)
			covered = [n for n in neighbors if n not in self.uncovered and n not in self.flags]
			numFlags = self.getFlags(neighbors)

			if num == numFlags:
				for c in covered:
					if c not in self.safe_moves:
						self.safe_moves.add(c)
			elif num - numFlags == len(covered):
				for c in covered:
					if c not in self.flags:
						self.flags.add(c)
		
	def getAction(self, number: int) -> "Action Object":

		self.moves[(self.currX, self.currY)] = number
		self.board[self.currX][self.currY] = number
		self.uncovered.add((self.currX, self.currY))
		self.updateFrontier()

		if len(self.moves) == self.rows * self.cols - self.mines:
			return Action(AI.Action.LEAVE, 1, 1)
		
		# Layer 1:
		# Adding neighbors if not risky
		if number == 0:
			for n in self.getNeighbors(self.currX, self.currY):
				if n not in self.uncovered and n not in self.safe_moves:
					self.safe_moves.add(n)

		# Popping neighbor if safe
		if len(self.safe_moves) != 0:
			nextMove = self.safe_moves.pop()
			self.currX, self.currY = nextMove
			return Action(AI.Action.UNCOVER, self.currX, self.currY)

		# Layer 2: If no more 0s to pop, get danger list and pop the least dangerous thing
		danger = {}
		for (x, y), num in self.moves.items():
			neighbors = self.getNeighbors(x,y)
			covered = [n for n in neighbors if n not in self.uncovered 
						and n not in self.flags]
			numFlags = self.getFlags(neighbors)
			remaining = num - numFlags
			if remaining > 0 and covered:
				for c in covered:
					if c not in danger:
						danger[c] = 0
					danger[c] += remaining/len(covered)
		if len(danger) > 0:
			MIN = min(danger.values())
			safest = [pos for pos, d in danger.items() if d == MIN]
			if safest != []:
				nextMove = safest.pop()
				self.currX, self.currY = nextMove
				return Action(AI.Action.UNCOVER, self.currX, self.currY)

		# Layer 3: Random
		nextMove = random.choice([(i, j) for i in range(self.rows)
										 for j in range(self.cols)
										 if (i, j) not in self.uncovered
										 and (i, j) not in self.flags])
		self.currX, self.currY = nextMove
		return Action(AI.Action.UNCOVER, self.currX, self.currY)
