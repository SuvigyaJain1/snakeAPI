import turtle
import time
import random 


class body(turtle.Turtle):

	def __init__(self, color, dir):
		turtle.Turtle.__init__(self)
		self.color(color)
		self.penup()
		self.shape('square')
		self.dir = dir # in order of [x, y]
		self.width = 20
		self.foodPos = (1000, 1000)

class snake():

	def __init__(self, x, y):
		self.head = body('white', [1,0])
		self.head.goto(x, y)
		self.tail = [self.head]
		self.n = 0
		turtle.update()

	def eat(self):
		self.food.clear()
		self.food.ht()
		self.randomFood()
		if len(self.tail) < 50:
			part = body('red', [0,0])
			self.tail.append(part)
			self.n += 1
			self.tail[self.n].goto(self.tail[self.n-1].xcor(), self.tail[self.n-1].ycor())
			return 1
		else:
			return -1

	def move(self):

		for i in range(self.n, -1, -1):
			newPos = [self.tail[i].pos()[0]+self.tail[i].width*self.tail[i].dir[0], self.tail[i].pos()[1]+self.tail[i].width*self.tail[i].dir[1]]
			self.tail[i].goto(newPos)

		for i in range(self.n, 0, -1):
			self.tail[i].dir = self.tail[i-1].dir

	def turn(self, directionNew):
		self.head.dir = directionNew
		self.tail[0].dir = directionNew

	def getPos(self):
		return self.head.pos()

	def atFood(self):
		if self.getPos() == self.foodPos:
			return 1
		return 0

	def randomFood(self):
		newFood = body('blue', [0,0])
		snakePos = list(map(lambda x: x.pos(), self.tail))
		newX, newY = snakePos[0]
		while (newX, newY) in snakePos:
			newX = random.randrange(-300, 300, 20)
			newY = random.randrange(-160, 160, 20)
		newFood.goto(newX, newY)
		self.foodPos = (newX, newY)
		self.food = newFood 	

	def left(self):
		self.turn([-1,0])

	def right(self):
		self.turn([1,0])

	def up(self):
		self.turn([0,1])

	def down(self):
		self.turn([0,-1])

	def checkBoundary(self):
		x, y = self.getPos()
		if x not in range(-300, 301):
			return 0
		if y not in range(-160, 161):
			return 0
		return 1

	def ateSelf(self):
		if self.n <= 2:
			return 0
		for part in self.tail[1:]:
			if part.pos() == self.tail[0].pos():
				return 1


class Game():

	def __init__(self ):
		self.snake = snake(0, 0)

	def startScreen(self, render):
		self.reward = 0
		if render:
			self.win = turtle.Screen()
			self.win.setup(620, 360)		
		else:
			self.win = turtle.Screen()
			self.win.setup(0, 0)
		self.win.bgcolor('black')
		self.win.tracer(0,0)
		self.snake.randomFood()
		# self.win.mainloop()

	# Call when playing a real-time game with an actual player and physical keyboard
	def gameLoop(self): 
		
		while(self.snake.n < 50):
			self.win.listen()
			self.win.onkey(self.snake.up, 'w');
			self.win.onkey(self.snake.down, 's');
			self.win.onkey(self.snake.left, 'a');
			self.win.onkey(self.snake.right, 'd');
			self.snake.move()

			if self.snake.atFood():
				self.snake.eat()

			if not self.snake.checkBoundary() or self.snake.ateSelf():
				break;
			time.sleep(0.1)

	# call for a simulated game that works with input in the form of an array or string
	# returns -1 for game end
	# returns score for game in progress
	# returns 0 for invalid input
	def nextFrame(self, keyPressed, render=False):
        
		self.snake.move()

		key_dict = {0:'up', 1:'down', 2:'left', 3:'right'}
		if keyPressed in ['up', 'down', 'left', 'right']:
			eval("self.snake."+keyPressed+"()")
		elif keyPressed in [0,1,2,3]:
			keyPressed = key_dict[keyPressed]
			eval("self.snake."+keyPressed+"()")
		else:
			print("Value Error: Unrecognized key input")
			return 0

		if not self.snake.checkBoundary() or self.snake.ateSelf():
			self.reward = -2
			return -1

		if self.snake.atFood():
				self.snake.eat()
				self.reward = 1
		else:
			headX = self.snake.getPos()[0]
			headY = self.snake.getPos()[1]
			foodX = self.snake.foodPos[0]
			foodY = self.snake.foodPos[1]
			self.reward = (700 - (abs(headX-foodX) + abs(headY-foodY)**2)**0.5) / 700


		if render:
			self.win.update()
			time.sleep(0.1)

		return self.snake.n
	
	def render(self):
		self.win.update()

	def clearScreen(self):
		self.win.clear()

	def snakeInfo(self):
		info = []
		info.append(self.snake.getPos()[0])
		info.append(self.snake.getPos()[1])
		info.append(self.snake.foodPos[0])
		info.append(self.snake.foodPos[1])
		info.append(list(map(lambda x: x.pos(), self.snake.tail)))
# 		reward = (700 - ((info[0]-info[2])**2 + (info[1]-info[3])**2)**0.5) / 700
		return info, float("%.2f"%self.reward)
