import contextlib
import time
from IPython.display import display, clear_output
from ipycanvas import Canvas


class Sketch:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = Canvas(width=width, height=height)
        self.canvas.fill_style = 'white'
        self.canvas.stroke_style = 'black'

    def display(self):
        display(self.canvas)

    def clear(self):
        self.canvas.clear()

    def remove(self):
        clear_output()

    def fill(self, color):
        self.canvas.fill_style = color

    def stroke(self, color):
        self.canvas.stroke_style = color

    def background(self, color):
        old_fill = self.canvas.fill_style
        old_stroke = self.canvas.stroke_style
        self.canvas.fill_style = color
        self.canvas.stroke_style = color
        self.canvas.fill_rect(0, 0, self.width, self.height)
        self.canvas.stroke_rect(0, 0, self.width, self.height)
        self.canvas.fill_style = old_fill
        self.canvas.stroke_style = old_stroke

    def circle(self, x, y, d):
        self.canvas.fill_circle(x, y, d)
        self.canvas.stroke_circle(x, y, d)

    def pause(self, secs):
        time.sleep(secs)


@contextlib.contextmanager
def sketch(width, height):
    p5 = Sketch(width, height)
    p5.display()
    yield p5
    p5.clear()
    p5.remove()
