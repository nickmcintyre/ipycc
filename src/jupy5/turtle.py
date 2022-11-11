import asyncio
from contextlib import contextmanager
import math
from .sketch import Sketch


class Turtle:
    def __init__(self, width, height):
        self._p5 = Sketch(width, height)
        self.home()
        self.end_poly()
    
    # ========================================
    #              Turtle Motion
    # ========================================

    def forward(self, d):
        x = self._x + d * math.cos(self._angle)
        y = self._y + d * math.sin(self._angle)
        if self._pen_is_down:
            self._p5.line(self._x, self._y, x, y)
        self._x = x
        self._y = y
        if self._is_drawing_poly:
            self._p5.vertex(x, y)

    def backward(self, d):
        self.forward(-d)
    
    def right(self, angle):
        self._angle += math.radians(angle)
    
    def left(self, angle):
        self._angle -= math.radians(angle)
    
    def setposition(self, x, y):
        self._x = x
        self._y = y
    
    def setx(self, x):
        self._x = x
    
    def sety(self, y):
        self._y = y
    
    def setheading(self, angle):
        self._angle = math.radians(angle)
    
    def home(self):
        self._x = self._p5.width * 0.5
        self._y = self._p5.height * 0.5
        self._angle = 0
        self._pen_is_down = False
        self._pen_color = 'limegreen'
        self._pen_size = 1
        self._speed = 1
        self._p5.stroke(self._pen_color)
        self._p5.stroke_weight(self._pen_size)
        self._fill_color = '#00000000'
        self._p5.no_fill()
    
    def speed(self, speed):
        self._speed = speed
    
    def position(self):
        return (self._x, self._y)

    def xcor(self):
        return self._x

    def ycor(self):
        return self._y

    def heading(self):
        return math.degrees(self._angle)

    # ========================================
    #               Pen Control
    # ========================================

    def pendown(self):
        self._pen_is_down = True

    def penup(self):
        self._pen_is_down = False

    def pensize(self, width):
        self._pen_size = width
        self._p5.stroke_weight(self._pen_size)
    
    def isdown(self):
        return self._pen_is_down
    
    def pencolor(self, color):
        self._pen_color = color
        self._p5.stroke(self._pen_color)

    def fillcolor(self, color):
        self._fill_color = color
    
    def reset(self):
        self.clear()
        self.home()
    
    def clear(self):
        self._p5.clear()
    
    def begin_poly(self):
        if self._pen_is_down:
            self._p5.begin_shape()
            self._is_drawing_poly = True
    
    def end_poly(self):
        self._p5.end_shape()
        self._is_drawing_poly = False
    
    def begin_fill(self):
        self._is_filling = True
        self._p5.fill(self._fill_color)
    
    def end_fill(self):
        self._is_filling = False
        self._p5.no_fill()
    
    def filling(self):
        return self._is_filling
    
    # ========================================
    #                Screen
    # ========================================
    
    def bgcolor(self, color):
        self._p5.background(color)

    async def delay(self, secs):
        await asyncio.sleep(secs)
    
    def _display(self):
        self._p5._display()
    
    def remove(self):
        self.clear()
        self._p5.remove()


@contextmanager
def turtle(width, height):
    t = Turtle(width, height)
    t._display()
    yield t
    t.remove()
