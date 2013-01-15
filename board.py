from math import atan, pi, sin, sqrt

class Board:
    def __init__(self, t):
        self.t = t
        self.scale = 1.0

    def draw(self):
        t = self.t
        count = 11
        height = t.window_height()
        width = t.window_width()
        d1 = height / (count * 1.5)
        d2 = width / count
        d = min(d1, d2) * self.scale
        t.penup()
        t.right(90)
        t.fd(d * (count-1)/2)
        t.right(60)
        t.fd(d * (count-1)/2)
        t.left(150)
        t.pendown()
        labels = [5, 1, 3, 4, 2, 5]
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
                self.hexagon(d, 
                             labels[(j-i+10)%5], 
                             skip_headings)
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
        self.write_letters(t, count, d)

    def write_letters(self, t, count, d):
        t.penup()
        t.goto(0, 0)
        t.setheading(0)
        text_font = "Courier", int(d / 2), "normal"
        t.right(30)
        t.fd((count / 2 + 1) * d)
        t.left(120)
        t.fd(d * 2 / 3)
        for _ in range(count - 1):
            t.write("x", font=text_font, align="center")
            t.fd(d)
        
        t.fd(d)
        t.left(120)
        t.fd(2 * d)
        for _ in range(count - 1):
            t.write("o", font=text_font, align="center")
            t.fd(d)
        
        t.left(60)
        t.fd(d)
        for _ in range(count - 1):
            t.write("x", font=text_font, align="center")
            t.fd(d)
        
        t.fd(d)
        t.left(120)
        t.fd(2 * d)
        for _ in range(count - 1):
            t.write("o", font=text_font, align="center")
            t.fd(d)
        
    def tick(self, t, tick_size, tick_angle):
        t.left(tick_angle)
        t.penup()
        t.fd(tick_size / 2)
        t.pendown()
        t.back(tick_size)
        t.penup()
        t.fd(tick_size / 2)
        t.pendown()
        t.right(tick_angle)
        
    def curved_tick(self, t, tick_size):
        t.left(90)
        t.penup()
        radius = -tick_size*2/3
        angle = 90.0
        t.circle(radius, -angle/2)
        t.pendown()
        t.circle(radius, angle)
        t.penup()
        t.circle(radius, -angle/2)
        t.pendown()
        t.right(90)


    def hash_mark(self, t, d, stepcount, tick_size):
        span = d / stepcount * 8
        hash_angle = atan(tick_size / span) * 180 / pi
        hash_length = sqrt(tick_size * tick_size + span * span)
        t.penup()
        t.left(90)
        t.fd(tick_size / 2)
        t.right(hash_angle + 90)
        t.pendown()
        t.fd(hash_length)
        t.penup()
        t.back(hash_length)
        t.left(hash_angle + 90)
        t.back(tick_size / 2)
        t.right(90)
        t.pendown()

    def edge(self, t, d, tickcount):
        slant_angle = 30
        curved_ticks = []
        slanted_ticks = [3]
        
        is_hashed = tickcount == 5
        tick_angle = 90
        if tickcount in slanted_ticks:
            tick_angle += slant_angle * (1 - 2*(tickcount % 2))
        tickcount = min(tickcount, 4)
        ticksize = d/5
        stepcount = 12
        for i in range(stepcount):
            if i == 2 and is_hashed:
                self.hash_mark(t, d, stepcount, ticksize)
            parity_match = i % 2 != tickcount % 2
            distance_from_centre = abs(stepcount/2 - i)
            close_enough = distance_from_centre < tickcount 
            if parity_match and close_enough:
                if tickcount in curved_ticks:
                    self.curved_tick(t, ticksize)
                else:
                    self.tick(t, ticksize, tick_angle)
            t.fd(d / stepcount)

    def hexagon(self, height, tickcount, skip_headings):
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
            self.edge(t, d, tickcount)
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
    Board(__live_turtle__).draw()
    
elif __name__ == '__main__':
    from Tkinter import mainloop
    from turtle import Turtle
    
    t = Turtle()
    t.tracer(1000000) # disable animation
    Board(t).draw()
    t.tracer(1)
    mainloop()
