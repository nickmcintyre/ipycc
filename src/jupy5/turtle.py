import asyncio
import math
from ipycanvas import hold_canvas
from .sketch import Sketch


class Turtle:

    def __init__(self, *args):
        if len(args) == 0:
            self.width = 200
            self.height = 200
        elif len(args) == 1:
            self.width = args[0]
            self.height = args[0]
        elif len(args) >= 2:
            self.width = args[0]
            self.height = args[1]
        self._bg = Sketch(self.width, self.height)
        self._bgcolor = 'white'
        self._p5 = Sketch(self.width, self.height)
        self.reset()
        self.end_poly()

    def _render(self):
        with hold_canvas():
            self._bg.background(self._bgcolor)
            # TODO: implement push() and pop()
            self._bg.scale(1, -1)
            self._bg.translate(0, -self.height)
            self._bg.image(self._p5.canvas, 0, 0)
            self._bg.reset_matrix()

    def draw(self):
        self._render()
        self._bg.draw()

    def remove(self):
        self._p5.remove()

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
        self._render()
    
    def fd(self, d):
        self.forward(d)

    def backward(self, d):
        self.forward(-d)
    
    def bk(self, d):
        self.forward(-d)
    
    def back(self, d):
        self.forward(-d)

    def right(self, angle):
        self._angle -= math.radians(angle)
    
    def rt(self, angle):
        self._angle -= math.radians(angle)

    def left(self, angle):
        self._angle += math.radians(angle)
    
    def lt(self, angle):
        self._angle += math.radians(angle)

    def goto(self, x, y):
        self._x = x
        self._y = y
    
    def setpos(self, x, y):
        self._x = x
        self._y = y
    
    def setposition(self, x, y):
        self._x = x
        self._y = y

    def setx(self, x):
        self._x = x

    def sety(self, y):
        self._y = y

    def setheading(self, angle):
        self._angle = math.radians(angle)
    
    def seth(self, angle):
        self._angle = math.radians(angle)

    def home(self):
        self._x = self._p5.width * 0.5
        self._y = self._p5.height * 0.5
        self._angle = 0

    def speed(self, speed):
        self._speed = speed

    def position(self):
        return (self._x, self._y)

    def xcor(self):
        return self._x

    def ycor(self):
        return self._y

    def heading(self):
        return math.degrees(self._angle) % 360

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

    def clear(self):
        self._p5.clear()

    def reset(self):
        self.clear()
        self.home()
        self._pen_is_down = True
        self._pen_color = 'black'
        self._pen_size = 1
        self._speed = 1
        self._p5.stroke(self._pen_color)
        self._p5.stroke_weight(self._pen_size)
        self._is_filling = False
        self._fill_color = '#00000000'
        self._p5.no_fill()
        self._is_drawing_poly = False
        self._render()

    def begin_poly(self):
        if self._pen_is_down:
            self._p5.begin_shape()
            self._is_drawing_poly = True

    def end_poly(self):
        self._p5.end_shape()
        if self._is_drawing_poly:
            self._render()
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
        self._bgcolor = color
        self._render()

    async def delay(self, secs):
        await asyncio.sleep(secs)
