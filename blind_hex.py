from subprocess import call

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def skipped_lines(i, j, size):
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

def writeText(c, text, x, y, r, theta):
    xscale = 1/4.0
    yscale = 1.0
    c.setFont("Courier", r/.75)
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

def writeLine(c, x, y, r, theta):
    c.translate(x, y)
    c.rotate(theta)
    c.translate(r, 0)
    c.line(0, 0, r, 0)
    c.translate(-r, 0)
    c.rotate(-theta)
    c.translate(-x, -y)
    
def writeHexagon(c, j, x, y, r, skipped_lines):
    for side in range(6):
        theta = side * 60
        writeText(c, str(j), x, y, r, theta + 30)
        if side not in skipped_lines:
            writeLine(c, x, y, r*1.16, theta)
    

c = canvas.Canvas("blind-hex.pdf")
c.translate(-1*inch, -.75*inch)
c.scale(.925, .925)
labels = [5, 1, 3, 4, 2, 5]
size = 6
for i in range(size):
    c.rotate(30)
    c.translate(1.5*inch, 0)
    c.rotate(-30)
    for j in range(size):
        writeHexagon(c, 
                     labels[(j-i+10)%5], 
                     inch, 
                     (2*j+1)*.75*inch, 
                     .375*inch,
                     skipped_lines(i, j, size))

xoffset = -2.3*inch
yoffset = 2.6*inch
c.translate(xoffset, yoffset)
for j in range(2):
    c.rotate(180)
    for i in range(5):
        c.drawString((i*0.75-2)*inch-xoffset, -3*inch-yoffset, str(i+1))
    
c.showPage()
c.save()

call(["evince", "blind-hex.pdf"])
