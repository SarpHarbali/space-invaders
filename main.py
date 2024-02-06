import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random


class Object:  #create parent class for objects
    def __init__(self, canvas, obj):
        self.canvas = canvas  #this will be used as a canvas
        self.obj = obj


    def get_position(self):
        return self.canvas.coords(self.obj)  #returns the coordinates of the object
    
    def move_object(self, x, y):  #move function
        self.canvas.move(self.obj, x, y)  #move by the x and y values (not move to)
        
    def destroy(self):
        self.canvas.delete(self.obj)  #deletes the object
        
class Character(Object): #child class
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.balls = []
        self.img = ImageTk.PhotoImage(Image.open("Media/cannon1.png"))  #create the cannon image
        self.obj = canvas.create_image(self.x, self.y, image=self.img)  #put image to the canvas
        self.cooldown = 1.00
        """self.obj = canvas.create_rectangle(self.x - self.width / 2,
                                       self.y - self.height / 2,
                                       self.x + self.width / 2,
                                       self.y + self.height / 2,
                                       fill='#FFB643')"""

        super().__init__(canvas, self.obj)  #use the canvas and obj attributes to use the functions of the parent class

    def move(self, x_move, y_move):
        self.move_object(x_move, y_move)

    def shoot(self,e):
        if self.cooldown >= 1.00:
            ball = Ball(self.canvas, self.get_position()[0],
                        self.get_position()[1])  #create instance of the ball
            self.balls.append(ball)  #list is used for the movement of the balls
            self.cooldown = 0.00

    def timer(self):
        self.cooldown += 0.5  #timer for the cooldown

    def move_balls(self):
        for ball in self.balls:
            ball.move()  #move every ball that's on the screen

        
class Ball(Object):
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 10
        self.img = ImageTk.PhotoImage(Image.open("Media/laser.png"))
        self.obj = canvas.create_image(self.x, self.y, image=self.img)
        super().__init__(canvas, self.obj)

    def move(self):
        self.move_object(0, -self.speed)


class Alien(Object):
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.points = 1000
        self.balls = []
        self.direction = 1
        self.img = ImageTk.PhotoImage(Image.open("Media/alien1.png"))
        self.obj = canvas.create_image(self.x, self.y, image=self.img)
        super().__init__(canvas, self.obj)

    def move(self):
        self.move_object(0, self.speed)

    def wiggle(self):
        self.move_object(random.randint(-5,5), random.randint(-5,5))  #move up and down and side to side randomly

    def score(self):
        self.points -= 2  #decrease the point value of the alien


class MainWindow(tk.Tk):  #child class of the tk.Tk class
    def __init__(self, name, dimensions):
        super().__init__()
        self.name = name
        self.dimensions = dimensions
        self.title(self.name)
        self.geometry(self.dimensions)


class Game(MainWindow):  #child of window
    def __init__(self, name, dimensions):
        super().__init__(name, dimensions)
        self.init_ui()  #class is instentiated with a function for implementing the playing again function
    def init_ui(self):
        self.width = int(self.dimensions[:4])
        self.height = int(self.dimensions[5:])
        self.home = tk.Canvas(self, width=self.width, height=self.height, bg="black")  #create canvas
        self.home.delete("all")
        self.home.pack()
        self.file = open("scoreboard.txt")
        self.text = self.file.read()
        self.users = self.text.split() #split by space
        self.users = [user.split(",") for user in self.users]  #split by comma
        for user in self.users:
            user[1] = int(user[1])
        self.users = sorted(self.users, key=lambda user: user[1], reverse=True) #sort values
        self.file.close()
        self.home.create_text(370,70, fill="white", font="Verdana 30", text="Welcome to Space Invaders!")

        self.start_button = tk.Button(self, text="Start New Game", bg="green", font="Verdana 20",command=self.start) #create button
        self.start_window = self.home.create_window(370,400,window=self.start_button) #place button to the canvas

        self.load_button = tk.Button(self, text="Load Game", bg="green", font="Verdana 20",
                                      command=self.load)  # create button
        self.load_window = self.home.create_window(370, 500, window=self.load_button)  # place button to the canvas

        self.home.create_text(370,200, fill="white", font="Verdana 30", text="Choose key bindings:")

        self.arrow_button = tk.Button(self, text="Arrow Keys", font="Verdana 15",command=lambda: self.binding("Arrow"))
        self.arrow_window = self.home.create_window(270,300,window=self.arrow_button)

        self.wasd_button = tk.Button(self, text="WASD Keys", font="Verdana 15", command=lambda: self.binding("WASD"))
        self.wasd_window = self.home.create_window(470, 300, window=self.wasd_button)

        self.home.create_text(950,100, fill="white", font="Verdana 30", text="HIGH SCORES")

        self.home.create_text(950,150, fill="white", font="Verdana 20", text = "RANK     NAME     SCORE")

        for i in range(len(self.users)): #display all the users to the leaderboard
            self.home.create_text(815,195+i*50, fill="white", font="Verdana 20", text=str(i+1))
            self.home.create_text(940,195+i*50, fill="white", font="Verdana 20", text =str(self.users[i][0]))
            self.home.create_text(1075,195+i*50, fill="white", font="Verdana 20", text =str(self.users[i][1]))
            if i == 9:
                break

        self.level = 1

        self.header = tk.Canvas(self, width=self.width,
                                height=80)
        self.header.pack()
        self.score_text = self.header.create_text(150, 40, fill="darkblue", font="Verdana 30",
                                text="Score: 0" )

        self.canvas = tk.Canvas(self, bg='black',
                                     width=self.width,
                                    height=self.height-80)
        self.canvas.pack()

        self.character = Character(self.canvas, 640, 600)

        self.canvas.focus_set()

        self.canvas.bind('<KeyPress>', self.press)
        self.canvas.bind('<KeyRelease>', self.release)

        self.canvas.bind('<space>', self.character.shoot)

        self.canvas.bind('<p>', self.pause)

        self.canvas.bind('<Shift-Up>', self.cheat)

        self.canvas.bind('b', self.boss)

        self.aliens = []

        self.wave = 1

        self.leftPressed = 0

        self.rightPressed = 0

        self.score = 0

        self.level_score = 0

        self.gameOver = False

        self.paused = False

        self.cheating = False

        self.run1 = None

        self.run2 = None

        self.run3 = None

        self.keys = "Arrow"

        self.hey_boss = False

        self.save_button = None
        self.save_window = None

    def binding(self, key):
        self.keys = key #assign wasd or arrows

    def press(self, event):
        if self.keys == "Arrow":
            if event.keysym == "Left":
                self.leftPressed = 1
            if event.keysym == "Right":
                self.rightPressed = 1
        else:
            if event.keysym == "a":
                self.leftPressed = 1
            if event.keysym == "d":
                self.rightPressed = 1

    def release(self, event):
        if self.keys == "Arrow":
            if event.keysym == "Left":
                self.leftPressed = 0
            if event.keysym == "Right":
                self.rightPressed = 0
        else:
            if event.keysym == "a":
                self.leftPressed = 0
            if event.keysym == "d":
                self.rightPressed = 0

    def collision(self, item1, item2):
        coord1 = item1.get_position()
        coord2 = item2.get_position()
        if coord1 and coord2:
            coord1 = [coord1[0]-item1.img.width(), #get the corners
                      coord1[1]-item1.img.height(),
                      coord1[0] + item1.img.width(),
                      coord1[1] + item1.img.height()]

            coord2 = [coord2[0]-item1.img.width(),
                      coord2[1]-item1.img.height(),
                      coord2[0] + item1.img.width(),
                      coord2[1] + item1.img.height()]

            return coord1[0] < coord2[2] and coord1[2] > coord2[0] and coord1[1] < coord2[3] and coord1[3] > coord2[1] #checks whether they are overlapping

    def collision_check(self):
        for ball in self.character.balls:
            for alien in self.aliens:
                if self.collision(ball, alien): #if any ball collides with any alien
                    self.score += alien.points
                    self.aliens.remove(alien)
                    self.character.balls.remove(ball)
                    self.canvas.delete(alien.obj)
                    self.canvas.delete(ball.obj)

    def ship_move(self):
        if self.leftPressed == 1:
            self.character.move(-self.character.speed, 0)
        if self.rightPressed == 1:
            self.character.move(self.character.speed, 0)


    def load(self):
        self.home.destroy()
        self.file = open("level.txt")
        self.text = self.file.read()
        self.text = self.text.split()
        self.level = int(self.text[0])
        self.score = int(self.text[1])
        self.loop()
        self.file.close()

    def start(self):
        self.home.destroy()
        self.loop()

    def pause(self,e):
        self.paused = not self.paused #true if false, false if true
        if not self.paused: #if paused is false
            if self.level == 1:
                self.run1 = self.after(50, self.level1)
            if self.level == 2:
                self.run1 = self.after(F50, self.level2)
            if self.level == 3:
                self.run1 = self.after(50, self.level3)

    def cheat(self,e):
        self.cheating = not self.cheating
        if self.cheating:
            self.character.speed = 30
        else:
            self.character.speed = 10

    def boss(self,e):
        self.hey_boss = not self.hey_boss
        if self.hey_boss:
            self.gameOver = True
            self.game_over()
            self.canvas.delete(ALL)
            self.blackboard = ImageTk.PhotoImage(Image.open("Media/boss.png"))  # create the cannon image
            self.bb_obj = self.canvas.create_image(640, 360, image=self.blackboard)  # put image to the canvas



    def save_game(self):
        self.file = open("level.txt", "w")
        self.file.write(f"{self.level} {self.level_score}")
        self.file.close()
        self.quit()

    def save_user(self):
        self.name = self.entry.get()
        self.file = open("scoreboard.txt", "a") #appending to the file
        self.file.write(f" {self.name},{self.score}")
        self.file.close()
        self.button.destroy()
        self.entry.destroy()
        self.yes = tk.Button(self, text="Play Again", bg="green", font="Verdana 20",command=self.play_again)
        self.yes_window = self.canvas.create_window(500, 500, window=self.yes)
        self.no = tk.Button(self, text="Quit", bg="red",command=self.quit, font="Verdana 20")
        self.no_window = self.canvas.create_window(700, 500, window=self.no)


    def play_again(self):
        self.canvas.destroy()
        self.header.destroy()
        self.init_ui() #initialize again


    def game_over(self):
        for key in self.canvas.bind():
            self.canvas.unbind(key) #unbind all keys
        self.gameOver = True
        self.character.balls.clear()
        self.aliens.clear()
        self.character.destroy()

        self.file = open("level.txt", "w")
        self.file.write("1 0")
        self.file.close()

        self.canvas.create_text(600, 150, fill="darkblue", font="Verdana 50",
                                text="Game Over!")
        self.canvas.create_text(600, 300, fill="darkblue", font="Verdana 50",
                                text=f"Your score: {self.score}")
        self.entry = tk.Entry(self, width=20, font="Verdana 20")
        self.entry_window = self.canvas.create_window(600, 450, window=self.entry)
        self.button = tk.Button(self, text="Save", command=self.save_user, font="Verdana 20")
        self.button_window = self.canvas.create_window(600, 500, window=self.button)

    def level1(self):
        if not self.hey_boss:
            if self.paused and self.run1 != None:
                self.after_cancel(self.run1) #cancel loop if p is pressed
                self.save_button = tk.Button(self, text="Save and Quit", command=self.save_game, font="Verdana 20")
                self.save_window = self.canvas.create_window(640, 360, window=self.save_button)
            else:
                if self.save_button != None:
                    self.save_button.destroy()
                if self.level == 1:
                    self.ship_move()
                    self.character.move_balls()
                    if self.wave > 0:
                        for i in range(5):
                            alien = Alien(self.canvas, random.randint(40, 1240), 40) #create 5 aliens whose locations are random
                            self.aliens.append(alien)
                        self.wave -= 1
                    for alien in self.aliens:
                        alien.move()
                        alien.wiggle()
                        alien.score()
                        if alien.get_position()[1]+alien.img.height()/2 >= 600: #if aliens touch the bottom
                            self.game_over()
                    self.collision_check()
                    self.character.timer()
                    if len(self.aliens) == 0: #if all aliens are killed
                        self.level += 1
                        self.level_score = self.score
                        self.loop()
                    self.header.itemconfigure(self.score_text, text=f"Score: {self.score}") #dynamic score text
                    self.run1 = self.after(50, self.level1) #creating a loop by running the function inside the function

    def level2(self):
        if not self.hey_boss:
            if self.paused and self.run2 != None:
                self.after_cancel(self.run2)
                self.save_button = tk.Button(self, text="Save and Quit", command=self.save_game, font="Verdana 20")
                self.save_window = self.canvas.create_window(640, 360, window=self.save_button)
            else:
                if self.save_button != None:
                    self.save_button.destroy()
                if self.level == 2:
                    self.ship_move()
                    self.character.move_balls()
                    if self.wave > 0:
                        for i in range(10):
                            alien = Alien(self.canvas, random.randint(40, 1240), 40)
                            self.aliens.append(alien)
                        self.wave -= 1
                    for alien in self.aliens:
                        alien.move()
                        alien.wiggle()
                        alien.score()
                        if alien.get_position()[1]+alien.img.height()/2 >= 600:
                            self.game_over()
                    self.collision_check()
                    self.character.timer()
                    if len(self.aliens) == 0:
                        self.level += 1
                        self.level_score = self.score
                        self.loop()
                    self.header.itemconfigure(self.score_text, text=f"Score: {self.score}")
                    self.run2 = self.after(50, self.level2)

    def level3(self):
        if not self.hey_boss:
            if self.paused and self.run3 != None:
                self.after_cancel(self.run3)
                self.save_button = tk.Button(self, text="Save and Quit", command=self.save_game, font="Verdana 20")
                self.save_window = self.canvas.create_window(640, 360, window=self.save_button)
            else:
                if self.save_button != None:
                    self.save_button.destroy()
                if self.level == 3:
                    self.ship_move()
                    self.character.move_balls()
                    if self.wave > 0:
                        for i in range(15):
                            alien = Alien(self.canvas, random.randint(40, 1240), 40)
                            self.aliens.append(alien)
                        self.wave -= 1
                    for alien in self.aliens:
                        alien.move()
                        alien.wiggle()
                        alien.score()
                        if alien.get_position()[1]+alien.img.height()/2 >= 600:
                            self.game_over()
                    self.collision_check()
                    self.character.timer()
                    if len(self.aliens) == 0:
                        self.level += 1
                        self.level_score = self.score
                        self.loop()
                    self.header.itemconfigure(self.score_text, text=f"Score: {self.score}")
                    self.run3 = self.after(50, self.level3)

    def loop(self):
        if self.level == 1 and not self.gameOver:
            self.character.balls.clear()
            self.wave = 1
            self.canvas.coords(self.character.obj, 640, 600)
            self.canvas.create_text(600, 360, fill="darkblue", font="Verdana 50",
                                    text="Level 1: Easy", tags="text")
            self.after(2000, lambda: self.canvas.delete("text")) #wait for 2 seconds and then start the level
            self.after(2000, self.level1)

        if self.level == 2 and not self.gameOver:
            self.character.balls.clear()
            self.wave = 1
            self.canvas.coords(self.character.obj, 640, 600)
            self.canvas.create_text(600, 360, fill="darkblue", font="Verdana 50",
                                    text="Level 2: Medium", tags="text")
            self.after(2000, lambda: self.canvas.delete("text"))
            self.after(2000, self.level2)

        if self.level == 3 and not self.gameOver:
            self.character.balls.clear()
            self.wave = 1
            self.canvas.coords(self.character.obj, 640, 600)
            self.canvas.create_text(600, 360, fill="darkblue", font="Verdana 50",
                                    text="Level 3: Hard", tags="text")
            self.after(2000, lambda: self.canvas.delete("text"))
            self.after(2000, self.level3)

        if self.level > 3:
            self.game_over()


if __name__ == '__main__':
    hop = Game("Home", "1280x720")
    hop.mainloop()