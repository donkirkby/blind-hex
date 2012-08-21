from math import sin, pi

#echo on
#echo width 40
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
        d1 = height*.97 / (count * 1.5)
        d2 = width / count
        d = min(d1, d2)
        t.penup()
        t.right(90)
        t.fd(d * (count-1)/2)
        t.right(60)
        t.fd(d * (count-1)/2)
        t.left(150)
        t.pendown()
        for i in range(count/2 + 1):
            for j in range(count/2 + 1):
                skip_headings = []
                if i == 0:
                    skip_headings.append(180)
                elif i == count/2:
                    skip_headings.append(0)
                if j == 0:
                    skip_headings.append(300)
                elif j == count/2:
                    skip_headings.append(120)
                if len(skip_headings) == 2:
                    skip_headings.append(sum(skip_headings)/2)
                self.hexagon(d, skip_headings)
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


    def tick(self, t, ticksize):
        t.left(90)
        t.penup()
        t.fd(ticksize / 2)
        t.pendown()
        t.back(ticksize)
        t.penup()
        t.fd(ticksize / 2)
        t.pendown()
        t.right(90)

    def edge(self, t, d):
        ticksize = d/8
        stepcount = 12
        tickcount = 4
        for i in range(stepcount):
            parity_match = i % 2 != tickcount % 2
            distance_from_centre = abs(stepcount/2 - i)
            close_enough = distance_from_centre < tickcount 
            if parity_match and close_enough:
                self.tick(t, ticksize)
            t.fd(d / stepcount)

    def hexagon(self, height, skip_headings):
        """ Draw a hexagon of the given height, centred at the current 
        position. 
        """
        d = height / (2*sin(60*pi/180))
        t = self.t
        t.penup()
        t.fd(d)
        t.left(120)
        t.pendown()
        for _ in range(6):
            self.edge(t, d)
            t.right(60)
            if t.heading() not in skip_headings:
                t.fd(d)
                t.penup()
                t.back(d)
                t.pendown()
            t.left(120)
        t.penup()
        t.right(120)
        t.back(d)
        t.pendown()

if __name__ == '__live_coding__':
    global __live_turtle__
    GameBoard(__live_turtle__).draw()
    
elif __name__ == '__main__':
    from Tkinter import mainloop
    from turtle import Turtle
    
    t = Turtle()
    t.tracer(1000000) # disable animation
    GameBoard(t).draw()
    t.tracer(1)
    mainloop()
