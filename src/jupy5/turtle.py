import asyncio
from contextlib import contextmanager
import math
import time
from .sketch import Sketch


class Turtle:
    def __init__(self, p5):
        self._x = p5.width / 2
        self._y = p5.height / 2
        self._p5 = p5
        self._angle = 0
        self._pen_is_down = False
        self._pen_color = 'black'
        self._pen_size = 1
        self._speed = 1

    def xcor(self):
        return self._x

    def ycor(self):
        return self._y

    def position(self):
        return (self._x, self._y)

    def heading(self):
        return math.degrees(self._angle)

    def setheading(self, angle):
        self._angle = math.radians(angle)

    def left(self, angle):
        self._angle -= math.radians(angle)

    def right(self, angle):
        self._angle += math.radians(angle)

    def setposition(self, x, y):
        self._x = x
        self._y = y

    def home(self):
        self._x = self._p5.width / 2
        self._y = self._p5.height / 2
        self._angle = 0
        self._pen_is_down = False
        self._pen_color = 'black'
        self._pen_size = 1
        self._speed = 1
        self._p5.stroke(self._pen_color)
        self._p5.stroke_weight(self._pen_size)

    def forward(self, d):
        dt = 0.5 / self._speed
        time.sleep(dt)
        x = self._x + d * math.cos(self._angle)
        y = self._y + d * math.sin(self._angle)
        if self._pen_is_down:
            self._p5.line(self._x, self._y, x, y)
        self._x = x
        self._y = y
        time.sleep(dt)

    def backward(self, d):
        self.forward(-d)

    def setspeed(self, speed):
        self._speed = speed

    def background(self, color):
        self._p5.background(color)

    def clear(self):
        self._p5.clear()

    def reset(self):
        self.clear()
        self.home()

    def pencolor(self, color):
        self._pen_color = color
        self._p5.stroke(self._pen_color)

    def pendown(self):
        self._pen_is_down = True

    def penup(self):
        self._pen_is_down = False

    def pensize(self, width):
        self._pen_size = width
        self._p5.stroke_weight(self._pen_size)

    async def pause(self, secs):
        await asyncio.sleep(secs)


@contextmanager
def turtle(width, height):
    p5 = Sketch(width, height)
    t = Turtle(p5)
    t.background('gainsboro')
    t._p5.display()
    yield t
    t._p5.clear()
    t._p5.remove()
