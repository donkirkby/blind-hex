#echo on
#echo width 80
#echo canvas
def draw(canvas):
    x = 10
    canvas.create_line(0, 0, 100, 200)

if __name__ == '__live_coding__':
    global __live_canvas__
    draw(__live_canvas__)
elif __name__ == '__main__':
    from Tkinter import mainloop, Button, Canvas, Frame, Tk
    master = Tk()
    frame = Frame(master)
    canvas = Canvas(frame, width=800, height=600)
    canvas.pack()
    quitButton = Button(frame, text="Quit", command=master.quit)
    quitButton.pack()
    frame.grid()
    quitButton.focus()
    
    draw(canvas)
    mainloop()