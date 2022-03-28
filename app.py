from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
import random
import time
from turtle import width

from nim  import Nim , train

root = Tk()
root.title('Nim - App')
# root.minsize()
# root.maxsize(400,400)


class App():
	def __init__(self, master, ai):
		
		self.ai = ai

		# frame
		self.myFrame = Frame(master, padx=50, pady=50, bg='#9c27b0')
		self.myFrame.grid()

		self.newFrame = Frame(master)
		self.newFrame.grid(column=0,row=2)


		# buttons  
		self.btn_identity = []
		self.btn_disabled = []


		for i in [1, 3, 5, 7]:
			for y in range(i):
				self.btn = Button(self.myFrame, text=f'{i-y}', font="50", bg="#ffeb3b",fg='#fff', pady=5, padx=10, command=partial(self._handle_action,(y+1 if i == 3 else y+4 if i == 5 else y+9 if i == 7 else 0,i,y)))
				self.btn.grid(column=y+2 if i == 3 else y+1 if i == 5 else y if i == 7 else 3, row=1 if i == 3 else 2 if i == 5 else 3 if i == 7 else 0)
				self.btn_identity.append(self.btn)

		self.status_bar = Label(self.newFrame, text="Loading...", font="50")
		self.status_bar.grid(column=0,row=0)

		# game
		self.human_player = random.randint(0, 1)

		# create a new game
		self.game = Nim()

		# Compute available actions
		self.available_actions = Nim.available_actions(self.game.piles)
		time.sleep(1)

		# check for play
		if self.game.player != self.human_player:
			print("AI's Turn")
			print(self.game.piles)
			self.status_bar.config(text="AI's Turn")

			# ai make a move
			pile, count = self.ai.choose_action(self.game.piles, epsilon=False)
			print((pile,count))

			# Make move
			self._hundle_play((pile,count))

			# update ui
			self._hundle_ui((pile+1, count))

			# your turn
			print("Your Turn")
			self.status_bar.config(text="Your Turn")

		else:
			print("Your Turn")
			self.status_bar.config(text="Your Turn")
			print(self.game.piles)

	def _hundle_play(self,action):
		pile , count = action
		if (pile, count) in self.available_actions:
			self.game.move((pile,count))
			self.available_actions = Nim.available_actions(self.game.piles)
			if self.game.winner is not None:
				winner = "Win" if self.game.winner == self.human_player else "Loose"
				print(f"You {winner}")
				self.status_bar.config(text=f"You {winner}")
			else:
				self.status_bar.config(text="Your Turn")



	def _hundle_ui(self, action):

		def _hundle_action(action):
			"""x : pile, y : count"""
			x,y = action
			
			config_btn_id = 1 if x == 2 else 4 if x == 3 else 9 if x == 4 else 0
			row = [x + config_btn_id for x in range(3 if x == 2 else 5 if x == 3 else 7 if x == 4 else 1)]
			row.reverse()

			done = 0
			for i in row:
				if done < y:
					button_name = (self.btn_identity[i])
					if self.btn_disabled.count(button_name) < 1:
						button_name.configure(bg='#e91e63' if self.game.player == 0 else '#3f51b5', state=DISABLED)
						self.btn_disabled.append(button_name)
						done+=1
			#
		_hundle_action(action)

	def _handle_action(self,n):

		def calculate_count(n):
			"""x : button id, y : pile, z : count"""
			x,y,z = n

			answer = 0
			if y == 1:
				answer = 1
			else:
				for i in range(x, 3+1 if y == 3 else 8+1 if y == 5 else 15+1):
					button_name = (self.btn_identity[i])
					if self.btn_disabled.count(button_name) < 1:
						answer+=1
			return answer

		"""x : button id, y : pile, z : count"""
		x,y,z = n

		pile1 = 1 if y == 3 else 2 if y == 5 else 3 if y == 7 else 0
		count1 = calculate_count(n)

		# make move
		self._hundle_play((pile1,count1))

		# update ui
		self._hundle_ui((pile1+1,count1))

		time.sleep(1)
		if self.game.winner is None:
			self.status_bar.config(text="AI's Turn")

			# ai make a move
			pile2, count2 = self.ai.choose_action(self.game.piles, epsilon=False)

			print((pile2,count2))

			# # make move
			self._hundle_play((pile2, count2))

			# # update ui
			self._hundle_ui((pile2+1, count2))


		
ai = train(0)
app = App(root,ai)
root.mainloop()
