from math import sin, pi

#echo on
#echo width 60
#echo scroll 50
#echo turtle

class GameBoard:
    def __init__(self, t):
        self.t = t
    
    def draw(self):
        t = self.t
        count = 11
        height = t.window_height()
        width = t.window_width()
        d1 = height / (count * 1.5)
        d2 = width / count
        d = min(d1, d2)
        t.penup()
        t.right(90)
        t.fd(height/2 - d)
        t.left(90)
        t.back(width/2 - d)
        t.pendown()
        for _ in range(count/2 + 1):
            for __ in range(count/2 + 1):
                self.hexagon(d)
                t.penup()
                t.left(90)
                t.fd(2*d)
                t.right(90)
                t.pendown()
            t.right(90)
            t.penup()
            t.fd((count+1)*d)
            t.left(90)
            t.left(30)
            t.fd(2*d)
            t.right(30)
            t.pendown()

    def edge(self, t, d):
        ticksize = d/5
        t.fd(d / 2)
        t.left(90)
        t.penup()
        t.fd(ticksize/2)
        t.pendown()
        t.back(ticksize)
        t.penup()
        t.fd(ticksize/2)
        t.pendown()
        t.right(90)
        t.fd(d / 2)

    def hexagon(self, height):
        d = height / (2*sin(60*pi/180))
        t = self.t
        for _ in range(6):
            self.edge(t, d)
            t.left(60)
            t.fd(d)
            t.penup()
            t.back(d)
            t.pendown()
            t.right(120)

if __name__ == '__live_coding__':
    global __live_turtle__
    GameBoard(__live_turtle__).draw()
    
elif __name__ == '__main__':
    from Tkinter import mainloop
    from turtle import Turtle
    
    GameBoard(Turtle()).draw()
    mainloop()
