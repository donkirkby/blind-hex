from subprocess import call

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Flowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class GameBoard(Flowable):
    def wrap(self, *args):
        #HACK: This will appear on the last page, so I don't care about flow.
        return (0, 0)
        
    def skipped_lines(self, i, j, size):
        skipped_lines = []
        if i == 0:
            skipped_lines.append(3)
            if j == 0:
                skipped_lines.append(4)
        elif i == size - 1:
            skipped_lines.append(0)
            if j == size - 1:
                skipped_lines.append(1)
        if j == 0:
            skipped_lines.append(5)
        elif j == size - 1:
            skipped_lines.append(2)
        return skipped_lines
    
    def writeText(self, c, text, x, y, r, theta):
        xscale = 1/4.0
        yscale = 1.0
        c.setFont("Courier-Bold", r/.75)
        c.translate(x, y)
        c.rotate(theta)
        c.translate(r, 0)
        c.line(0, 0.4*r, 0, 0.6*r)
        c.line(0, -0.4*r, 0, -0.6*r)
        c.scale(xscale, yscale)
        xoffset = -.305
        if text == "4":
            xoffset = -.38
        c.drawString(xoffset*r/.75, -.3*r/.75, text)
        c.scale(1/xscale, 1/yscale)
        c.translate(-r, 0)
        c.rotate(-theta)
        c.translate(-x, -y)
    
    def writeEdge(self, c, ticks, x, y, r, theta):
        xscale = 1/4.0
        yscale = 1.0
        c.translate(x, y)
        c.rotate(theta)
        c.translate(r, 0)
        c.line(0, 0.6*r, 0, -0.6*r)
        crosses = min(ticks, 4)
        for i in range(crosses):
            sign = 1 - 2*(i%2)
            centering = ((crosses+1)%2)*0.1*r
            height = sign*((i+1)/2)*0.2*r + centering
            c.line(-.1*r, height, .1*r, height)
        if ticks == 5:
            c.line(-.1*r, -0.4*r, .1*r, 0.4*r)
        c.scale(xscale, yscale)
        c.scale(1/xscale, 1/yscale)
        c.translate(-r, 0)
        c.rotate(-theta)
        c.translate(-x, -y)
    
    def writeLine(self, c, x, y, r, theta):
        c.translate(x, y)
        c.rotate(theta)
        c.translate(r, 0)
        c.line(0, 0, r, 0)
        c.translate(-r, 0)
        c.rotate(-theta)
        c.translate(-x, -y)
        
    def writeHexagon(self, c, j, x, y, r, skipped_lines):
        for side in range(6):
            theta = side * 60
    #        writeText(c, str(j), x, y, r, theta + 30)
            self.writeEdge(c, j, x, y, r, theta + 30)
            if side not in skipped_lines:
                self.writeLine(c, x, y, r*1.16, theta)
        
    def draw(self):
        c = self.canv
        c.translate(-2.1*inch, -11.4*inch)
        c.scale(.925, .925)
        labels = [5, 1, 3, 4, 2, 5]
        size = 6
        for i in range(size):
            c.rotate(30)
            c.translate(1.5*inch, 0)
            c.rotate(-30)
            for j in range(size):
                self.writeHexagon(c, 
                             labels[(j-i+10)%5], 
                             inch, 
                             (2*j+1)*.75*inch, 
                             .375*inch,
                             self.skipped_lines(i, j, size))
    
        c.setFont("Courier", .375*inch/0.75)
        xoffset = -2.3*inch
        yoffset = 2.6*inch
        c.translate(xoffset, yoffset)
        for player in 'ox':
            c.rotate(180)
            for i in range(5):
                c.drawString((i*0.75-2)*inch-xoffset, -3*inch-yoffset, str(i+1))
                c.drawString((i*0.75-2)*inch-xoffset, -2.5*inch-yoffset, player)
        c.translate(-xoffset, -yoffset)
        
        for i in range(size*2-1):
            if i < size*2-2:
                c.drawString(1.4*inch, (1.03+0.75*i)*inch, "x")
            if i > 0:
                c.rotate(30)
                c.translate(-.75*2*size*inch, 0)
                c.rotate(-30)
                c.drawString(1.6*inch, (1.03+0.75*i)*inch, "x")
                c.rotate(30)
                c.translate(.75*2*size*inch, 0)
                c.rotate(-30)
        
        xoffset = 0.8*inch
        c.translate(xoffset, 0)
        for i in range(size*2-1):
            if i < size*2-2:
                c.drawString(0, 0, "o")
            if i > 0:
                c.drawString(0.09*inch, (2*size*0.75 - .2)*inch, "o")
            c.rotate(30)
            c.translate(-.75*inch, 0)
            c.rotate(-30)
        c.translate(-xoffset, 0)

def go():
    doc = SimpleDocTemplate("blind-hex.pdf")
    styles = getSampleStyleSheet()
    story = [Paragraph('Blind Hex', styles['Title'])]
    f = open('README.md')
    text = ''
    for line in f.readlines():
        line = line.strip()
        if line.startswith('==='):
            style_name = 'Heading1'
        elif line.startswith('---'):
            style_name = 'Heading2'
        elif not line:
            style_name = 'Normal'
        else:
            style_name = None
        if style_name:
            story.append(Paragraph(text, styles[style_name]))
            text = ''
        else:
            if text:
                text += ' '
            text += line
    story.append(PageBreak())
    story.append(GameBoard())
    doc.build(story)

go()

call(["evince", "blind-hex.pdf"])
