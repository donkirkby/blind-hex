from turtle import TNavigator, TPen
from argparse import ArgumentError

class CairoTurtle(TNavigator, TPen):
    class _Screen(object):
        def __init__(self, canvas):
            self.cv = canvas
            
    def __init__(self, canvas, frame):
        TNavigator.__init__(self)
        TPen.__init__(self)
        self.screen = CairoTurtle._Screen(canvas)
        self.frame = frame
        self.__xoff = self.window_width()/2
        self.__yoff = self.window_height()/2
    
    def _goto(self, end):
        start = self._position
        if self._drawing:
            self.screen.cv.line(start[0] + self.__xoff, 
                                start[1] - self.__yoff, 
                                end[0] + self.__xoff, 
                                end[1] - self.__yoff)
        self._position = end
    
    def window_width(self):
        return self.frame._width

    def window_height(self):
        return self.frame._height

    def write(self, arg, move=False, align="left", font=("Helvetica", 8, "normal")):
        if move:
            raise ArgumentError('move', 'Parameter is not supported.')
        fontName = font[0]
        is_style_added = False
        for style in font[2].split():
            if style != 'normal':
                if not is_style_added:
                    fontName += '-'
                    is_style_added = True
                fontName += style.capitalize()
        
        x = self.xcor() + self.__xoff
        y = self.ycor() - self.__yoff
        y += font[1] * 0.45
        self.screen.cv.setFont(fontName, font[1])
        if align == 'left':
            self.screen.cv.drawString(x, 
                                      y,
                                      str(arg))
        elif align == 'center':
            self.screen.cv.drawCentredString(x, 
                                             y,
                                             str(arg))
        elif align == 'right':
            self.screen.cv.drawRightString(x, 
                                           y,
                                           str(arg))
