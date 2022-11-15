import math
from .sketch import Sketch


class Turtle(Sketch):
    def __init__(self, *args):
        if len(args) == 0:
            width = 200
            height = 200
        elif len(args) == 1:
            width = args[0]
            height = args[0]
        elif len(args) == 2:
            width = args[0]
            height = args[1]
        super().__init__(width, height)
        self.home()
        self.end_poly()

    # ========================================
    #              Turtle Motion
    # ========================================

    def forward(self, d):
        x = self._x + d * math.cos(self._angle)
        y = self._y + d * math.sin(self._angle)
        if self._pen_is_down:
            self.line(self._x, self._y, x, y)
        self._x = x
        self._y = y
        if self._is_drawing_poly:
            self.vertex(x, y)

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
        self._x = self.width * 0.5
        self._y = self.height * 0.5
        self._angle = 0
        self._pen_is_down = False
        self._pen_color = 'limegreen'
        self._pen_size = 1
        self._speed = 1
        self.stroke(self._pen_color)
        self.stroke_weight(self._pen_size)
        self._fill_color = '#00000000'
        self.no_fill()

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
        self.stroke_weight(self._pen_size)

    def isdown(self):
        return self._pen_is_down

    def pencolor(self, color):
        self._pen_color = color
        self.stroke(self._pen_color)

    def fillcolor(self, color):
        self._fill_color = color

    def reset(self):
        self.clear()
        self.home()

    def begin_poly(self):
        if self._pen_is_down:
            self.begin_shape()
            self._is_drawing_poly = True

    def end_poly(self):
        self.end_shape()
        self._is_drawing_poly = False

    def begin_fill(self):
        self._is_filling = True
        self.fill(self._fill_color)

    def end_fill(self):
        self._is_filling = False
        self.no_fill()

    def filling(self):
        return self._is_filling

    # ========================================
    #                Screen
    # ========================================

    def bgcolor(self, color):
        self.background(color)
