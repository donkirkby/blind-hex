from turtle import TNavigator, TPen

class CairoTurtle(TNavigator, TPen):
    def __init__(self, canvas, frame):
        TNavigator.__init__(self)
        TPen.__init__(self)
        self.canvas = canvas
        self.frame = frame
        self.__xoff = self.window_width()/2
        self.__yoff = self.window_height()/2
    
    def _goto(self, end):
        start = self._position
        if self._drawing:
            self.canvas.line(start[0] + self.__xoff, 
                             start[1] - self.__yoff, 
                             end[0] + self.__xoff, 
                             end[1] - self.__yoff)
        self._position = end
    
    def window_width(self):
        return self.frame._width

    def window_height(self):
        return self.frame._height
