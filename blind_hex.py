from subprocess import call
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Flowable, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]

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

def firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(PAGE_WIDTH/2, 
                             0.75 * inch, 
                             "donkirkby.github.com/blind-hex")
    canvas.restoreState()

def go():
    doc = SimpleDocTemplate("blind-hex.pdf")
    styles = getSampleStyleSheet()
    story = [Paragraph('Blind Hex', styles['Title'])]
    f = open('README.md')
    links = {}
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
        if style_name and text:
                story.append(Paragraph(text, styles[style_name]))
                story.append(Spacer(1,0.055*inch))
                text = ''
        else:
            match = re.match(r'^\s*\[(.+)\]:\s*(.*)$', line)
            if match:
                links[match.group(1)] = match.group(2)
            elif re.search(r'PDF', line):
                text = '' # skip this paragraph
            else:
                if text:
                    text += ' '
                text += line
    if text:
        raise RuntimeError('No blank line found at end of file.')
    for i in range(len(story)/2):
        p = story[i*2+1]
        replacement = ''
        index = 0
        for match in re.finditer(r'\[([^\]]+)\]\[([^\]]+)\]', p.text):
            block = p.text[index:match.start()]
            replacement += block
            link = links[match.group(2)]
            replacement += '<a href="%s">%s</a>' % (link, match.group(1))
            index = match.end()
        if replacement:
            block = p.text[index:]
            if block.startswith(' '):
                block = '&nbsp;' + block[1:]
            replacement += block
            story[i*2+1] = Paragraph(replacement, p.style)
    story.append(PageBreak())
    story.append(GameBoard())
    doc.build(story, onFirstPage=firstPage)

go()

call(["evince", "blind-hex.pdf"])
