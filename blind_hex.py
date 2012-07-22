from subprocess import call

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def writeText(c, text, x, y, r, theta):
    c.setFont("Helvetica", r/.75)
    c.translate(x, y)
    c.rotate(theta)
    c.translate(r, 0)
    c.scale(1.0/4, 1.24)
    c.drawString(-.305*r/.75, -.355*r/.75, text)
    c.scale(4, 1/1.24)
    c.translate(-r, 0)
    c.rotate(-theta)
    c.translate(-x, -y)

def writeLine(c, x, y, r, theta):
    c.translate(x, y)
    c.rotate(theta)
    c.translate(r, 0)
    c.line(0, 0, r, 0)
    c.translate(-r, 0)
    c.rotate(-theta)
    c.translate(-x, -y)
    
def writeHexagon(c, j, x, y, r):
    for side in range(6):
        theta = side * 60
        writeText(c, str(j), x, y, r, theta + 30)
        writeLine(c, x, y, r*1.16, theta)
    

c = canvas.Canvas("blind-hex.pdf")
# define a large font
# choose some colors
c.setStrokeColorRGB(0,0,0)
# move the origin up and to the left
#c.translate(4.25*inch,9*inch)
# change color
c.setFillColorRGB(0,0,0)

#c.circle(1*inch, 0, 0.1*inch)
#c.rect(-1*inch, -1*inch, 2*inch, 2*inch)
c.translate(-1*inch, -.75*inch)
c.scale(.925, .925)
labels = [5, 1, 3, 4, 2, 5]
for i in range(6):
    c.rotate(30)
    c.translate(1.5*inch, 0)
    c.rotate(-30)
    for j in range(6):
        writeHexagon(c, labels[(j-i+10)%5], inch, (2*j+1)*.75*inch, .375*inch)
#c.rotate(30)
#c.translate(0.5*inch, 0)
#c.rect(-1*inch, -1*inch, 2*inch, 2*inch)
#c.scale(.5, 1)
#c.rect(-1*inch, -1*inch, 2*inch, 2*inch)
#for j in range(6):
#    c.drawString(1*inch, -.325*inch, "3")
#    c.rotate(60)
c.showPage()
c.save()

call(["evince", "blind-hex.pdf"])
