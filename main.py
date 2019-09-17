import random

# implement networking
# implement graphics
# improve grid efficiency
# improve readability
# change how direction is handled
# change how the objects interact

class Snake:
    directions = {"up":[0,1],
                  "down":[0,-1],
                  "left":[-1,0],
                  "right":[1,0],
                  "u":[0,1],
                  "d":[0,-1],
                  "l":[-1,0],
                  "r":[1,0]}
    
    def __init__(self, x, y, length=5):
        self.snake_nodes = [[x, y]]
        self.direction = [0,1] # positive y movement "up"
        self.dead = False
        self.length = length
        for i in range(self.length-1):
            self.add_segment()
        
    def move(self):
        # prepend the new head position
        self.snake_nodes[0:0] = [[self.snake_nodes[0][0]+self.direction[0],self.snake_nodes[0][1]+self.direction[1]]]
        # delete last segment of snake
        self.snake_nodes.pop()

    def change_direction(self, direction):
        if direction in self.directions: # check it is a valid key for a direction
            if [-self.direction[0],-self.direction[1]] != Snake.directions[direction]: # you can't do a 180
                self.direction = Snake.directions[direction]

    def add_segment(self): # should be position of last segment in previous move, but this will do for now
        self.snake_nodes.append([self.snake_nodes[-1][0]-self.direction[0],self.snake_nodes[-1][1]-self.direction[1]])

    def get_nodes(self):
        return self.snake_nodes

    def is_self_intersecting(self):
        return any([self.snake_nodes.count(node) > 1 for node in self.snake_nodes])

    def die(self):
        self.dead = True

class Food:

    def __init__(self, x, y):
        self.position = [x, y]

    def get_position(self):
        return self.position

class Grid:
    grid_w = 20
    grid_h = 20

    def __init__(self, w=0, h=0, snake=Snake(5,5)):
        self.grid_w = w if w > 0 else Grid.grid_w
        self.grid_h = h if h > 0 else Grid.grid_h
        self.snakes = [snake]
        self.food = []
        
    def add_snake(self, snake):
        self.snakes.append(snake)

    def add_food(self, food):
        self.food.append(food)

    def remove_food(self, food):
        if food in self.food:
            self.food.remove(food)

    def check_collisions(self):
        for snake in self.snakes:
            if snake.is_self_intersecting():
                snake.die()
            elif snake.get_nodes()[0][0] >= self.grid_w or snake.get_nodes()[0][1] >= self.grid_h: # check for intersecting walls and then kill snake
                snake.die()
            elif snake.get_nodes()[0][0] < 0 or snake.get_nodes()[0][1] < 0: # check for intersecting walls and then kill snake
                snake.die()
            else:
                for food in self.food:
                    if food.get_position() == snake.get_nodes()[0]:
                        snake.add_segment()
                        self.food.remove(food)

    def get_grid(self):
        grid = [[0 for x in range(self.grid_w)] for y in range(self.grid_h)]
        for snake_id,snake in enumerate(self.snakes):
            for segment in snake.get_nodes():
                try:
                    grid[segment[0]][segment[1]] = snake_id + 1
                except:
                    pass
        for food in self.food:
            pos = food.get_position()
            grid[pos[0]][pos[1]] = -1
        return grid
    
    def print(self):
        grid = [[0 for x in range(self.grid_w)] for y in range(self.grid_h)]
        old_grid = self.get_grid()
        for x,row in enumerate(old_grid): # make it visually make sense
            for y,value in enumerate(row):
                y = self.grid_h - (y+1)
                grid[y][x] = value
        print(grid)
        return grid

    def remove_dead_snakes(self):
        for snake in self.snakes:
            if snake.dead:
                self.snakes.remove(snake) # don't do this in a for loop
                print("Snake died")

    def add_constant_food(self, amount):
        if len(self.food) < amount:
            for i in range(amount-len(self.food)): #-1
                position = self.random_empty_position()
                if position:
                    self.add_food(Food(position[0], position[1]))
                else:
                    print("You win")

    def get_cell_type(self, position):
        return get_grid()[position[0]][position[1]]
        
    def random_empty_position(self):
        grid = self.get_grid()
        empty_positions = []
        for x,row in enumerate(grid): # make it visually make sense
            for y,value in enumerate(row):
                if value == 0:
                    empty_positions.append([x,y])
        if empty_positions:
            position = random.choice(empty_positions)
        else:
            position = None
        return position
    
    def draw(self):
        # draw the snake(s) and then draw the food using pygame
        pass
        

snake = Snake(5, 5, 5)
food = Food(10, 10)
grid = Grid(snake=snake)
grid.add_food(food)

running = True

while running:
    grid.print()
    direction = input("Direction: ")
    snake.change_direction(direction)
    snake.move()
    grid.check_collisions()
    grid.add_constant_food(1)
    grid.remove_dead_snakes()
    if len(grid.snakes) < 1 or len(grid.food) < 1:
        print("Game Finished")
        running = False
    
