from subprocess import call
import re

from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from board import Board
from pdf_turtle import PdfTurtle


class GameBoard(PdfTurtle):
    def draw(self):
        board = Board(self)
        board.draw()


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    page_width, page_height = doc.pagesize
    canvas.drawCentredString(page_width//2,
                             0.75 * inch, 
                             "donkirkby.github.com/blind-hex")
    canvas.restoreState()


def go():
    doc = SimpleDocTemplate("blind-hex.pdf",
                            pagesize=pagesizes.letter,
                            topMargin=0.25 * inch,
                            bottomMargin=0.25 * inch,
                            leftMargin=0.75 * inch,
                            rightMargin=0.75 * inch)
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
            story.append(Spacer(1, 0.055*inch))
            text = ''
        else:
            match = re.match(r'^\s*\[(.+)]:\s*(.*)$', line)
            if match:
                links[match.group(1)] = match.group(2)
            elif re.search(r'PDF', line):
                text = ''  # skip this paragraph
            else:
                if text:
                    text += ' '
                text += line
    if text:
        raise RuntimeError('No blank line found at end of file.')
    for i in range(len(story)//2):
        p = story[i*2+1]
        replacement = ''
        index = 0
        for match in re.finditer(r'\[([^]]+)]\[([^]]+)]', p.text):
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
    scale = 0.9825
    board = GameBoard.create(doc.width * scale, doc.height * scale)
    board.draw()
    story.append(board.to_reportlab())
    doc.build(story, onFirstPage=first_page)


go()

call(["evince", "blind-hex.pdf"])
