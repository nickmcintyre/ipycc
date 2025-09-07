import math
import time
from ipycanvas import hold_canvas
from .sketch import Sketch
from ._colors import named_colors


class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!

    Provides (for `a`, `b` vectors, `k` number):
    -  `a+b` vector addition
    - `a-b` vector subtraction
    - `a*b` inner product
    - `k*a` and `a*k` multiplication with scalar
    - `|a|` absolute value of `a`
    - `a.rotate(angle)` rotation
    """

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0] * other[0] + self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0] * other, self[1] * other)
        return NotImplemented

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return math.hypot(*self)

    def rotate(self, angle: int | float):
        """Returns a vector with the same magnitude that is rotated
        counterclockwise by a given angle.

        Argument: `angle` -- a number

        **Example**
        ```python
        from ipycc.turtle import Vec2D

        v1 = Vec2D(1, 0)
        v2 = v1.rotate(90)
        print(v1) # (1.00,0.00)
        print(v2) # (0.00,1.00)
        ```
        """
        perp = Vec2D(-self[1], self[0])
        angle = math.radians(angle)
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self):
        return "(%.2f,%.2f)" % self


class TurtleGraphicsError(Exception):
    """Some TurtleGraphics Error.
    """


# Shape vertices.
_turtle_shapes = {
    "arrow" : ((-10, 0), (10, 0), (0, 10)),
    "turtle" : ((0, 16), (-2, 14), (-1, 10), (-4, 7),
                (-7, 9), (-9, 8), (-6, 5), (-7, 1), (-5, -3), (-8, -6),
                (-6,-8), (-4, -5), (0, -7), (4, -5), (6, -8), (8, -6),
                (5, -3), (7, 1), (6, 5), (9, 8), (7, 9), (4, 7), (1, 10),
                (2, 14)),
    "circle" : ((10, 0), (9.51, 3.09), (8.09, 5.88),
                (5.88, 8.09), (3.09, 9.51), (0, 10), (-3.09, 9.51),
                (-5.88, 8.09), (-8.09, 5.88), (-9.51, 3.09), (-10, 0),
                (-9.51, -3.09), (-8.09, -5.88), (-5.88, -8.09),
                (-3.09, -9.51), (-0.00, -10.00), (3.09, -9.51),
                (5.88, -8.09), (8.09, -5.88), (9.51, -3.09)),
    "square" : ((10, -10), (10, 10), (-10, 10),
                (-10, -10)),
    "triangle" : ((10, -5.77), (0, 11.55),
                (-10, -5.77)),
    "classic": ((0, 0),(-5, -9),(0, -7),(5, -9)),
}


# Default screen configuration.
_screen_width = 400
_screen_height = 400


class _Screen:
    """Provide the basic graphics functionality.
    """
    def __init__(self,
                 width: int | float =_screen_width,
                 height: int | float =_screen_height):
        self.width = width
        self.height = height
        self._sketch = Sketch(self.width, self.height)
        self._bgcolor = "white"
        self._sketch.background(self._bgcolor)
        self._turtles = []
        self._delayvalue = 10
        self._tracing = 1
        self.xscale = self.yscale = 1.0

    def add_turtle(self, t):
        """Adds a turtle to be drawn."""
        if t not in self._turtles:
            self._turtles.append(t)

    def _update(self):
        """Redraws the screen."""
        if self._tracing == 1:
            with hold_canvas():
                self._sketch.background(self._bgcolor)
                for t in self._turtles:
                    self._sketch.canvas.save()
                    self._sketch.scale(1, -1)
                    self._sketch.translate(0, -self.height)
                    self._sketch.image(t._pen, 0, 0)
                    if t.isvisible():
                        x, y = t._to_screen_coords(t._position)
                        self._sketch.translate(x, y)
                        angle = math.radians(t.heading() + t.tiltangle()) - math.pi / 2
                        self._sketch.rotate(angle)
                        self._sketch.stroke(t._pencolor)
                        self._sketch.stroke_weight(t._outlinewidth)
                        self._sketch.fill(t._fillcolor)
                        self._sketch.begin_shape()
                        shape = _turtle_shapes[t._shape]
                        for v in shape:
                            sx, sy = t._stretchfactor
                            self._sketch.vertex(sx * v[0], sy * v[1])
                        self._sketch.end_shape()
                    self._sketch.reset_matrix()
                    self._sketch.canvas.restore()

    def _delay(self, ms: int | float):
        """Delays animation for a given number of milliseconds."""
        time.sleep(ms * 0.001)

    def show(self):
        """Display the screen's drawing canvas."""
        self._update()
        self._sketch.show()


# Screens dictionary.
_screens = {
    "default": _Screen()
}
_screens["current"] = _screens["default"]


def setup(width: int | float, height: int | float, name: str = "default"):
    """Sets the size of the screen.

    Arguments:
    - `width` -- a number
    - `height` -- a number
    - `name` -- a string (optional)

    The first two arguments, `width` and `height`, set the width of the
    drawing screen in pixels.

    The third argument, `name`, is optional. If `name` is provided, a new
    screen will be created if it doesn't already exist. If a screen with
    `name` does exist, it will be resized and all turtles will be reset.
    The screen will be set as the current drawing screen.

    **Example**
    ```python
    from ipycc.turtle import Turtle, setup

    # Set the default screen to half size.
    setup(200, 200)

    # Create a turtle and show it.
    t = Turtle()
    t.show()

    # Send the turtle home.
    t.home()

    # Set the new screen to quarter size.
    setup(100, 100, "quarter")

    # Create a turtle and show it.
    t = Turtle()
    t.show()

    # Send the turtle home.
    t.home()
    ```
    """
    if name in _screens:
        old_screen = _screens[name]
        _screens[name] = _Screen(width, height)
        _screens[name]._turtles = old_screen._turtles
        for t in _screens[name]._turtles:
            t._pen = _Screen(width, height)
            t.reset()
    else:
        _screens[name] = _Screen(width, height)
    _screens["current"] = _screens[name]


def showscreen(name: str = "default"):
    """Shows the screen to which turtles are drawing.

    Argument: `name` (optional)

    Calling `showscreen()` with no arguments displays the current drawing
    screen beneath the code cell in which it's called.

    The argument, `name`, is optional. If the name of a screen created with
    `setup()` is passed, then it will be set as the current screen and
    displayed. Any turtles created afterward will render their
    drawings to this screen.

    **Example**
    ```python
    from ipycc.turtle import Turtle, setup, showscreen

    # Show the default screen.
    showscreen()

    # Create a turtle and move it.
    t = Turtle()
    t.forward(100)
    
    # Create a new sceen and show it.
    setup(200, 200, "a")
    showscreen("a")

    # Create a turtle and move it.
    t2 = Turtle()
    for i in range(4):
        t2.forward(50)
        t2.left(90)
    ```
    """
    if not name in _screens:
        raise TurtleGraphicsError(f"The screen {name} doesn't exist.")
    _screens["current"] = _screens[name]
    _screens["current"].show()


def tracer(n: int):
    """Turns turtle animation on/off for updating drawings.

    The parameter, `n`, must be either 0 (off) or 1 (on).
    
    **Example**
    ```python
    from ipycc.turtle import Turtle, tracer

    t = Turtle()
    t.show()

    tracer(0)
    for i in range(100):
        length = i * 5
        t.forward(length)
        t.left(90)
    tracer(1)
    ```
    """
    _screens["current"]._tracing = n
    if n == 1:
        _screens["current"]._update()


def clearscreen(name: str = "current"):
    """Delete all drawings from the screen.
    
    Reset the now empty screen to its initial state with a white background.

    Argument: `name` (optional)

    Calling `clearscreen()` resets all turtles on the current screen.

    The argument, `name`, is optional. If the name of a screen created with
    `setup()` is passed, then its turtles will be reset.

    **Example**
    ```python
    from ipycc.turtle import Turtle, clearscreen

    # Create a turtle and show its screen.
    t = Turtle()
    t.show()

    # Move the turtle forward.
    t.forward(100)
    
    # Clear the current screen.
    clearscreen()
    ```
    """
    if name not in _screens:
        raise TurtleGraphicsError(f"The screen {name} doesn't exist.")
    for t in _screens[name]._turtles:
        t.clear()
    _screens[name]._sketch.background("white")


def resetscreen(name: str = "current"):
    """Reset all turtles on the screen to their initial state.

    Argument: `name` (optional)

    Calling `resetscreen()` resets all turtles on the current screen.

    The argument, `name`, is optional. If the name of a screen created with
    `setup()` is passed, then it will be reset.

    **Example**
    ```python
    from ipycc.turtle import Turtle, resetscreen

    # Create a turtle and show its screen.
    t = Turtle()
    t.show()

    # Move the turtle forward.
    t.forward(100)
    
    # Reset the current screen.
    resetscreen()
    ```
    """
    if name not in _screens:
        raise TurtleGraphicsError(f"The screen {name} doesn't exist.")
    for t in _screens[name]._turtles:
        t.reset()


class Turtle:
    """A class to describe a virtual turtle robot drawing on a screen."""

    def __init__(self):
        self._screen = _screens["current"]
        self._pen = Sketch(self._screen.width, self._screen.height)
        self.reset()
        self._screen.add_turtle(self)

    def _to_screen_coords(self, v: Vec2D) -> Vec2D:
        x = self._screen.width * 0.5 + v[0]
        y = self._screen.height * 0.5 + v[1]
        return Vec2D(x, y)

    def show(self):
        """Display the turtle's drawing sceen.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()
        ```
        """
        self._screen.show()

    # ========================================
    #              Turtle Motion
    # ========================================

    def _update(self):
        """Perform a Turtle-data update.
        """
        if self._screen._tracing == 0:
            return
        elif self._screen._tracing == 1:
            self._screen._update()
            self._screen._delay(self._screen._delayvalue)

    def _go(self, distance: int | float):
        """Move turtle forward by specified distance"""
        ende = self._position + self._orient * distance
        self._goto(ende)

    def _goto(self, end: Vec2D):
        """Move the pen to the point end, thereby drawing a line
        if pen is down. All other methods for turtle movement depend
        on this one.
        """
        start = self._position
        if self._speed and self._screen._tracing == 1:
            diff = end - start
            diffsq = (diff[0] * self._screen.xscale)**2 + (diff[1] * self._screen.yscale)**2
            nhops = 1 + int((diffsq**0.5) / (3 * (1.1**self._speed) * self._speed))
            delta = diff * (1.0 / nhops)
            for n in range(1, nhops + 1):
                self._position = start + delta * n
                if self._drawing:
                    x1, y1 = self._to_screen_coords(start)
                    x2, y2 = self._to_screen_coords(self._position)
                    self._pen.line(x1, y1, x2, y2)
                self._update()
        else:
            x1, y1 = self._to_screen_coords(start)
            x2, y2 = self._to_screen_coords(end)
            if self._drawing:
                self._pen.line(x1, y1, x2, y2)
        if isinstance(self._fillpath, list):
            self._fillpath.append(end)
        self._position = end
        self._update()

    def forward(self, distance: int | float):
        """Move the turtle forward by the specified distance.

        Aliases: `forward` | `fd`

        Argument:
        `distance` -- a number (integer or float)

        Move the turtle forward by the specified `distance`, in the direction
        the turtle is headed.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.position()) # (0.00, 0.00)
        t.forward(25)
        print(t.position()) # (25.00,0.00)
        t.forward(-75)
        print(t.position()) # (-50.00,0.00)
        ```
        """
        self._go(distance)

    fd = forward

    def backward(self, distance: int | float):
        """Move the turtle backward by distance.

        Aliases: `back` | `backward` | `bk`

        Argument:
        `distance` -- a number

        Move the turtle backward by `distance`, opposite to the direction the
        turtle is headed. Do not change the turtle's heading.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.position()) # (0.00, 0.00)
        t.backward(30)
        print(t.position()) # (-30.00, 0.00)
        ```
        """
        self._go(-distance)

    back = backward
    bk = backward

    def _rotate(self, angle: int | float):
        """Turn turtle counterclockwise by specified angle if angle > 0."""
        self._orient = self._orient.rotate(angle)
        self._update()

    def right(self, angle: int | float):
        """Turn turtle right by angle units.

        Aliases: `right` | `rt`

        Argument:
        `angle` -- a number (integer or float)

        Turn turtle right by `angle` units. (Units are by default degrees,
        but can be set via the `degrees()` and `radians()` methods.)
        Angle orientation depends on mode. (See this.)

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.heading()) # 22.0
        t.right(45)
        print(t.heading()) # 337.0
        ```
        """
        self._rotate(-angle)

    rt = right

    def left(self, angle: int | float):
        """Turn turtle left by angle units.

        Aliases: `left` | `lt`

        Argument:
        `angle` -- a number (integer or float)

        Turn turtle left by `angle` units. (Units are by default degrees,
        but can be set via the `degrees()` and `radians()` methods.)
        Angle orientation depends on mode.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.heading()) # 22.0
        t.left(45)
        print(t.heading()) # 67.0
        ```
        """
        self._rotate(angle)

    lt = left

    def goto(self, x: int | float | tuple | Vec2D, y: int | float = None):
        """Move turtle to an absolute position.

        Aliases: `setpos` | `setposition` | `goto`:

        Arguments:
        - `x` -- a number or vector
        - `y` -- a number (optional)

        call: `goto(x, y)`         # two coordinates

        Move turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        tp = t.pos()
        print(tp) # (0.00, 0.00)
        t.setpos(60,30)
        print(t.pos()) # (60.00, 30.00)
        ```
        """
        if y is None:
            self._goto(Vec2D(*x))
        else:
            self._goto(Vec2D(x, y))

    setpos = goto
    setposition = goto

    def setx(self, x: int | float):
        """Set the turtle's first coordinate to `x`.

        Argument:
        `x` -- a number (integer or float)

        Set the turtle's first coordinate to `x`, leave second coordinate
        unchanged.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.position()) # (0.00, 240.00)
        t.setx(10)
        print(t.position()) # (10.00, 240.00)
        ```
        """
        self._goto(Vec2D(x, self._position[1]))

    def sety(self, y: int | float):
        """Set the turtle's second coordinate to `y`.

        Argument:
        `y` -- a number (integer or float)

        Set the turtle's first coordinate to `x`, second coordinate remains
        unchanged.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.position()) # (0.00, 40.00)
        t.sety(-10)
        print(t.position()) # (0.00, -10.00)
        ```
        """
        self._goto(Vec2D(self._position[0], y))

    def setheading(self, to_angle: int | float):
        """Set the orientation of the turtle to `to_angle`.

        Aliases:  `setheading` | `seth`

        Argument:
        `to_angle` -- a number (integer or float)

        Set the orientation of the turtle to `to_angle`.
        Here are some common directions in degrees:
        - 0 - east
        - 90 - north
        - 180 - west
        - 270 - south

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.setheading(90)
        print(t.heading()) # 90
        ```
        """
        angle = (to_angle - self.heading()) * self._angleOrient
        full = self._fullcircle
        half = full / 2.0
        angle = (angle + half) % full - half
        self._rotate(angle)

    seth = setheading

    def home(self):
        """Move turtle to the origin - coordinates `(0,0)`.

        No arguments.

        Move turtle to the origin and reset its heading to 0.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.home()
        ```
        """
        self.goto(0, 0)
        self.setheading(0)

    def dot(self, size: int = None, *color: str | tuple[int | float]):
        """Draw a dot with diameter size, using color.

        Optional arguments:
        - `size` -- an integer >= 1 (if given)
        - `color` -- a colorstring or a numeric color tuple

        Draw a circular dot with diameter size, using `color`.
        If `size` is not given, the maximum of `pensize+4` and `2*pensize` is
        used.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.dot()
        t.fd(50)
        t.dot(20, "blue")
        t.fd(50)
        ```
        """
        if not color:
            if isinstance(size, (str, tuple)):
                color = self._colorstr(size)
                size = self._pensize + max(self._pensize, 4)
            else:
                color = self._pencolor
                if not size:
                    size = self._pensize + max(self._pensize, 4)
        else:
            if size is None:
                size = self._pensize + max(self._pensize, 4)
            color = self._colorstr(color)
        self._pen.canvas.save()
        self._pen.no_stroke()
        self._pen.fill(color)
        x, y = self._to_screen_coords(self._position)
        self._pen.circle(x, y, size)
        self._pen.canvas.restore()

    def stamp(self):
        """Stamp a copy of the turtleshape onto the canvas.

        No argument.

        Stamp a copy of the turtle shape onto the canvas at the current
        turtle position.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color("blue")
        t.stamp()
        t.fd(50)
        ```
        """
        self._pen.canvas.save()
        x, y = self._to_screen_coords(self._position)
        self._pen.translate(x, y)
        angle = math.radians(self.heading()) - math.pi / 2
        self._pen.rotate(angle)
        self._pen.stroke(self._pencolor)
        self._pen.stroke_weight(2)
        self._pen.fill(self._fillcolor)
        self._pen.begin_shape()
        shape = _turtle_shapes[self._shape]
        for v in shape:
            sx, sy = self._stretchfactor
            self._pen.vertex(sx * v[0], sy * v[1])
        self._pen.end_shape()
        self._pen.reset_matrix()
        self._pen.canvas.restore()

    def speed(self, speed: int | float | str = None) -> None | int:
        """Return or set the turtle's speed.

        Optional argument:
        `speed` -- an integer in the range `0..10` or a `speedstring`
        (see below)

        Set the turtle's speed to an integer value in the range `0..10`.
        If no argument is given: return current speed.

        If input is a number greater than 10 or smaller than 0.5,
        speed is set to 0.
        Speedstrings  are mapped to speedvalues in the following way:
        - `'fastest'` :  0
        - `'fast'`    :  10
        - `'normal'`  :  6
        - `'slow'`    :  3
        - `'slowest'` :  1
        speeds from 1 to 10 enforce increasingly faster animation of
        line drawing and turtle turning.

        Attention:
        `speed = 0` : *no* animation takes place. forward/back makes turtle jump
        and likewise left/right make the turtle turn instantly.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.speed(3)
        ```
        """
        speeds = {"fastest": 0, "fast": 10, "normal": 6, "slow": 3, "slowest": 1}
        if speed is None:
            return self._speed
        if speed in speeds:
            speed = speeds[speed]
        elif 0.5 < speed < 10.5:
            speed = int(round(speed))
        else:
            speed = 0
        self._speed = speed

    def position(self) -> Vec2D:
        """Return the turtle's current location `(x,y)`, as a `Vec2D`.

        Aliases: `pos` | `position`

        No arguments.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.pos()) # (0.00, 0.00)
        ```
        """
        return self._position

    pos = position

    def towards(self, x: int | float | tuple | Vec2D, y: int | float = None) -> float:
        """Return the angle of the line from the turtle's position to `(x,y)`.

        Arguments:
        - `x` -- a number   or  a pair/vector of numbers   or   a turtle instance
        - `y` -- a number (optional)

        Return the angle, between the line from turtle-position to position
        specified by `x`, `y` and the turtle's start orientation.

        **Example**
        ```python
        from ipycc.turtle import Turtle, Vec2D

        t = Turtle()
        t.show()

        print(t.pos()) # (10.00, 10.00)
        print(t.towards(0, 0)) # 225.0
        print(t.towards((0, 0))) # 225.0
        v = Vec2D(0, 0)
        print(t.towards(v)) # 225.0
        ```
        """
        if y is not None:
            pos = Vec2D(x, y)
        if isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, tuple):
            pos = Vec2D(*x)
        x, y = pos - self._position
        result = round(math.degrees(math.atan2(y, x)), 10) % 360.0
        result /= self._degreesPerAU
        return (self._angleOffset + self._angleOrient * result) % self._fullcircle

    def xcor(self) -> float:
        """Return the turtle's x coordinate.

        No arguments.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.left(60)
        t.forward(100)
        print(tutrtle.xcor()) # 50.0
        ```
        """
        return self._position[0]

    def ycor(self) -> float:
        """Return the turtle's y coordinate.

        No arguments.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.left(60)
        t.forward(100)
        print(t.ycor()) # 86.6025403784
        ```
        """
        return self._position[1]

    def heading(self) -> float:
        """Return the turtle's current heading.

        No arguments.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.left(67)
        print(t.heading()) # 67.0
        ```
        """
        x, y = self._orient
        result = round(math.degrees(math.atan2(y, x)), 10) % 360.0
        result /= self._degreesPerAU
        return (self._angleOffset + self._angleOrient*result) % self._fullcircle

    def distance(self, x: int | float | tuple | Vec2D, y: int | float = None) -> float:
        """Return the distance from the turtle to `(x,y)` in turtle step units.

        Arguments:
        - `x` -- a number   or  a pair/vector of numbers   or   a turtle instance
        - `y` -- a number   (optional)

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.pos()) # (0.00, 0.00)
        print(t.distance(30,40)) # 50.0
        t2 = Turtle()
        t2.forward(77)
        print(t.distance(t2)) # 77.0
        ```
        """
        if y is not None:
            pos = Vec2D(x, y)
        if isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, tuple):
            pos = Vec2D(*x)
        return abs(pos - self._position)

    def _setDegreesPerAU(self, fullcircle):
        """Helper function for degrees() and radians()"""
        self._fullcircle = fullcircle
        self._degreesPerAU = 360/fullcircle
        self._angleOffset = 0

    def degrees(self, fullcircle: int | float = 360.0):
        """Set angle measurement units to degrees.

        Optional argument:
        `fullcircle` -  a number

        Set angle measurement units, i. e. set number
        of 'degrees' for a full circle. Default value is
        360 degrees.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.left(90)
        print(t.heading()) # 90

        # Change angle measurement unit to grad (also known as gon,
        # grade, or gradian and equals 1/100-th of the right angle.)
        t.degrees(400.0)
        print(t.heading()) # 100
        ```
        """
        self._setDegreesPerAU(fullcircle)

    def radians(self):
        """Set the angle measurement units to radians.

        No arguments.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.heading()) # 90
        t.radians()
        print(t.heading()) # 1.5707963267948966
        ```
        """
        self._setDegreesPerAU(math.tau)

    # ========================================
    #               Pen Control
    # ========================================

    def pendown(self):
        """Pull the pen down -- drawing when moving.

        Aliases: `pendown` | `pd` | `down`

        No argument.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.pendown()
        t.forward(100)
        ```
        """
        self._drawing = True

    pd = pendown
    down = pendown

    def penup(self):
        """Pull the pen up -- no drawing when moving.

        Aliases: `penup` | `pu` | `up`

        No argument

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.penup()
        t.forward(100)
        ```
        """
        self._drawing = False

    pu = penup
    up = penup

    def pensize(self, width: int | float = None) -> None | float:
        """Set or return the line thickness.

        Aliases:  `pensize` | `width`

        Argument:
        `width` -- positive number

        Set the line thickness to `width` or return it. If no argument is
        given, current pensize is returned.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.pensize()) # 1
        t.pensize(10)   # from here on lines of width 10 are drawn
        ```
        """
        if width is None:
            return self._pensize
        self._pensize = width
        self._pen.stroke_weight(self._pensize)

    width = pensize

    def isdown(self) -> bool:
        """Return `True` if pen is down, `False` if it's up.

        No argument.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.penup()
        print(t.isdown()) # False
        t.pendown()
        print(t.isdown()) # True
        ```
        """
        return self._drawing

    def _iscolorstring(self, color) -> bool:
        """Check if the string color is a legal Tkinter color string.
        """
        return color in named_colors

    def _colorstr(self, color: str | tuple[int | float]) -> str:
        """Return color string corresponding to args.

        Argument may be a string or a tuple of three
        numbers corresponding to actual colormode,
        i.e. in the range 0<=n<=colormode.

        If the argument doesn't represent a color,
        an error is raised.
        """
        if len(color) == 1:
            color = color[0]
        if isinstance(color, str):
            if self._iscolorstring(color) or color == "":
                return named_colors[color]
            else:
                raise TurtleGraphicsError("bad color string: %s" % str(color))
        try:
            r, g, b = color
        except (TypeError, ValueError):
            raise TurtleGraphicsError("bad color arguments: %s" % str(color))
        if self._colormode == 1.0:
            r, g, b = [round(255.0 * x) for x in (r, g, b)]
        if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
            raise TurtleGraphicsError("bad color sequence: %s" % str(color))
        return "#%02x%02x%02x" % (r, g, b)

    def _color(self, cstr) -> str | tuple:
        if not cstr.startswith("#"):
            return cstr
        if len(cstr) == 7:
            cl = [int(cstr[i:i + 2], 16) for i in (1, 3, 5)]
        elif len(cstr) == 4:
            cl = [16 * int(cstr[h], 16) for h in cstr[1:]]
        else:
            raise TurtleGraphicsError("bad colorstring: %s" % cstr)
        return tuple(c * self._colormode / 255 for c in cl)

    def colormode(self, cmode: int | float = None) -> None | int | float:
        """Return the colormode or set it to 1.0 or 255.

        Optional argument:
        `cmode` -- one of the values 1.0 or 255

        r, g, b values of colortriples have to be in range `0..cmode`.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.colormode()) # 1.0
        t.colormode(255)
        t.pencolor(240, 160, 80)
        ```
        """
        if cmode is None:
            return self._colormode
        if cmode == 1.0:
            self._colormode = float(cmode)
        elif cmode == 255:
            self._colormode = int(cmode)

    def color(self, *args) -> None | str | tuple:
        """Return or set the pencolor and fillcolor.

        Arguments:
        Several input formats are allowed.
        They use 0, 1, 2, or 3 arguments as follows:

        - `color()` returns the current pencolor and the current fillcolor
        as a pair of color specification strings.
        - `color(colorstring)`, `color((r,g,b))`, `color(r,g,b)` sets both
        `fillcolor()` and `pencolor()` to the given value.
        - `color(colorstring1, colorstring2)`, `color((r1,g1,b1), (r2,g2,b2))`
        sets `pencolor(colorstring1)` and `fillcolor(colorstring2)` or
        `pencolor((r1,g1,b1))` and `fillcolor((r2,g2,b2))`.

        If turtleshape is a polygon, outline and interior of that polygon
        is drawn with the newly set colors.

        For more info see: `pencolor()`, `fillcolor()`

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color('red', 'green')
        print(t.color()) # ('red', 'green')
        t.colormode(255)
        t.color((40, 80, 120), (160, 200, 240))
        print(t.color()) # ('#285078', '#a0c8f0')
        ```
        """
        if args:
            l = len(args)
            if l == 1:
                pcolor = fcolor = args[0]
            elif l == 2:
                pcolor, fcolor = args
            elif l == 3:
                pcolor = fcolor = args
            pcolor = self._colorstr(pcolor)
            fcolor = self._colorstr(fcolor)
            self._pencolor = pcolor
            self._pen.stroke(self._pencolor)
            self._pen.stroke_weight(self._pensize)
            self._fillcolor = fcolor
            self._pen.fill(self._fillcolor)
            self._update()
        else:
            return self._color(self._pencolor), self._color(self._fillcolor)

    def pencolor(self, *args) -> None | str | tuple:
        """ Return or set the pencolor.

        Arguments:
        Four input formats are allowed:
          - `pencolor()`
            Return the current pencolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - `pencolor(colorstring)`
            a [Tk color specification string](https://www.tcl-lang.org/man/tcl8.4/TkCmd/colors.htm),
            such as `"red"` or `"yellow"`
          - `pencolor((r, g, b))`
            *a tuple* of `r`, `g`, and `b`, which represent, an RGB color,
            and each of `r`, `g`, and `b` are in the range `0..colormode`,
            where `colormode` is either 1.0 or 255
          - `pencolor(r, g, b)`
            `r`, `g`, and `b` represent an RGB color, and each of `r`, `g`,
            and `b` are in the range `0..colormode`

        If turtleshape is a polygon, the outline of that polygon is drawn
        with the newly set pencolor.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.pencolor('brown')
        tup = (0.2, 0.8, 0.55)
        t.pencolor(tup)
        print (t.pencolor()) # '#33cc8c'
        ```
        """
        if args:
            color = self._colorstr(args)
            if color == self._pencolor:
                return
            self._pencolor = color
            self._pen.stroke(self._pencolor)
            self._pen.stroke_weight(self._pensize)
            self._update()
        else:
            return self._color(self._pencolor)

    def fillcolor(self, *args) -> None | str | tuple:
        """Return or set the fillcolor.

        Arguments:
        Four input formats are allowed:
          - `fillcolor()`
            Return the current fillcolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - `fillcolor(colorstring)`
            a [Tk color specification string](https://www.tcl-lang.org/man/tcl8.4/TkCmd/colors.htm),
            such as `"red"` or `"yellow"`
          - `fillcolor((r, g, b))`
            *a tuple* of `r`, `g`, and `b`, which represent, an RGB color,
            and each of `r`, `g`, and `b` are in the range `0..colormode`,
            where `colormode` is either 1.0 or 255
          - `fillcolor(r, g, b)`
            `r`, `g`, and `b` represent an RGB color, and each of `r`, `g`, and `b`
            are in the range `0..colormode`

        If turtleshape is a polygon, the interior of that polygon is drawn
        with the newly set fillcolor.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.fillcolor('violet')
        col = t.pencolor()
        t.fillcolor(col)
        t.fillcolor(0, .5, 0)
        ```
        """
        if args:
            color = self._colorstr(args)
            if color == self._fillcolor:
                return
            self._fillcolor = color
            self._pen.fill(self._fillcolor)
            self._update()
        else:
            return self._color(self._fillcolor)

    def filling(self) -> bool:
        """Return fillstate (`True` if filling, `False` otherwise).

        No argument.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.begin_fill()
        if t.filling():
            t.pensize(5)
        else:
            t.pensize(3)
        ```
        """
        return isinstance(self._fillpath, list)

    def begin_fill(self):
        """Called just before drawing a shape to be filled.

        No argument.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color("black", "red")
        t.begin_fill()
        t.begin_poly()
        for i in range(4):
            t.forward(50)
            t.left(90)
        t.end_poly()
        t.end_fill()
        ```
        """
        self._fillpath = [self._position]

    def end_fill(self):
        """Fill the shape drawn after the call `begin_fill()`.

        No argument.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color("black", "red")
        t.begin_fill()
        t.begin_poly()
        for i in range(4):
            t.forward(50)
            t.left(90)
        t.end_poly()
        t.end_fill()
        ```
        """
        if self.filling():
            if len(self._fillpath) > 2:
                self._pen.begin_shape()
                for v in self._fillpath:
                    x, y = self._to_screen_coords(v)
                    self._pen.vertex(x, y)
                self._pen.end_shape()
            self._fillpath = None
            self._update()

    def begin_poly(self):
        """Start recording the vertices of a polygon.

        No argument.

        Start recording the vertices of a polygon. Current turtle position
        is first point of polygon.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color("black", "red")
        t.begin_fill()
        t.begin_poly()
        for i in range(4):
            t.forward(50)
            t.left(90)
        t.end_poly()
        t.end_fill()
        ```
        """
        self._poly = [self._position]
        self._creatingPoly = True

    def end_poly(self):
        """Stop recording the vertices of a polygon.

        No argument.

        Stop recording the vertices of a polygon. Current turtle position is
        last point of polygon. This will be connected with the first point.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.color("black", "red")
        t.begin_fill()
        t.begin_poly()
        for i in range(4):
            t.forward(50)
            t.left(90)
        t.end_poly()
        t.end_fill()
        ```
        """
        self._creatingPoly = False

    def reset(self):
        """Return the turtle to its initial state and clear its drawings from
        the screen.

        No arguments.

        **Example**
        ```python
        t = Turtle()
        t.show()

        t.forward(50)
        t.reset()
        ```
        """
        self._drawing = True
        self._pencolor = "black"
        self._pensize = 1
        self._pen.stroke(self._pencolor)
        self._pen.stroke_weight(self._pensize)
        self._speed = 3
        self._shown = True
        self._fillcolor = "black"
        self._is_filling = False
        self._poly = []
        self._fillpath = None
        self._pen.no_fill()
        self._creatingPoly = False
        self._position = Vec2D(0, 0)
        self._colormode = 1.0
        self._shape = "classic"
        self._stretchfactor = (1.0, 1.0)
        self._shearfactor = 0.0
        self._tilt = 0.0
        self._outlinewidth = 1
        self._orient = Vec2D(1, 0)
        self._angleOrient = 1.0
        self.degrees()
        self.clear()

    def clear(self):
        """Delete the turtle's drawings from the screen. Do not move turtle.

        No arguments.

        Delete the turtle's drawings from the screen. Do not move turtle.
        State and position of the turtle as well as drawings of other
        turtles are not affected.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.forward(50)
        t.clear()
        ```
        """
        self._pen.clear()
        self._update()

    def _write(self, txt: str, align: str, fontname: str, fontsize: int | float, fonttype: str):
        """Performs the writing for write()
        """
        self._pen.canvas.save()
        self._pen.scale(1, -1)
        self._pen.translate(0, -self._pen.height)
        x, y = self._to_screen_coords(self._position)
        self._pen.fill(self._pencolor)
        self._pen.no_stroke()
        self._pen.text_align(align)
        self._pen.text_font(fontname)
        self._pen.text_size(fontsize)
        self._pen.text_style(fonttype)
        self._pen.text(txt, x, self._pen.height - y)
        self._pen.canvas.restore()
        self._update()

    def write(self, arg, align: str = "left", font: tuple = ("Arial", 8, "normal")):
        """Write text at the current turtle position.

        Arguments:
        - `arg` -- info, which is to be written to the screen
        - `align` (optional) -- one of the strings `"left"`, `"center"` or
        `"right"`
        - `font` (optional) -- a triple (fontname, fontsize, fonttype)

        Write text - the string representation of `arg` - at the current
        turtle position according to align (`"left"`, `"center"` or `"right"`)
        and with the given font.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.write('Home = ', align="center")
        t.write((0, 0))
        ```
        """
        fontname, fontsize, fonttype = font
        if not align.lower() in (Sketch.LEFT, Sketch.CENTER, Sketch.RIGHT):
            raise TurtleGraphicsError('Invalid text alignment. Must be "left", "center", or "right".')
        if not isinstance(fontsize, (int, float)):
            raise TurtleGraphicsError('Font size must be a number.')
        if not fonttype in (Sketch.NORMAL, Sketch.ITALIC, Sketch.BOLD, Sketch.BOLDITALIC):
            raise TurtleGraphicsError('Invalid font type. Must be "normal", "italic", "bold", or "bolditalic".')
        self._write(str(arg), align.lower(), fontname, fontsize, fonttype)

    # ========================================
    #             Turtle State
    # ========================================

    def showturtle(self):
        """Make the turtle visible.

        Aliases:  `showturtle` | `st`

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.showturtle()
        ```
        """
        self._shown = True
        self._update()

    st = showturtle

    def hideturtle(self):
        """Make the turtle invisible.

        Aliases:  `hideturtle` | `ht`

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.hideturtle()
        ```
        """
        self._shown = False
        self._update()

    ht = hideturtle

    def isvisible(self) -> bool:
        """Return `True` if the turtle is shown, `False` if it's hidden.

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.hideturtle()
        print(t.isvisible()) # False
        t.showturtle()
        print(t.isvisible()) # True
        ```
        """
        return self._shown

    def shape(self, name: str = None) -> None | str:
        """Set turtle shape to shape with given name / return current shapename.

        Optional argument:
        `name` -- a string, which is a valid shapename

        Set turtle shape to shape with given `name` or, if `name` is not given,
        return name of current shape.
        Valid shapenames are:
        - `"arrow"`
        - `"turtle"`
        - `"circle"`
        - `"square"`
        - `"triangle"`
        - `"classic"`

        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        print(t.shape()) # 'arrow'
        t.shape("turtle")
        print(t.shape()) # 'turtle'
        ```
        """
        if name is None:
            return self._shape
        if not name in _turtle_shapes:
            raise NameError("There is no shape named %s" % name)
        self._shape = name
        self._update()

    def shapesize(
        self, stretch_wid: int | float = None, stretch_len: int | float = None
    ) -> float:
        """Set/return turtle's stretchfactors/outline. Set resizemode to "user".

        Optional arguments:
        - `stretch_wid` : positive number
        - `stretch_len` : positive number
        - `outline`  : positive number

        Return or set the pen's attributes x/y-stretchfactors and/or outline.
        The turtle will be displayed stretched according to its stretchfactors:
        - `stretch_wid` is stretchfactor perpendicular to orientation.
        - `stretch_len` is stretchfactor in direction of the turtle's orientation.
        - `outline` determines the width of the shapes's outline.

        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.shapesize(5, 5, 12)
        t.shapesize(outline=8)
        ```
        """
        if stretch_wid is stretch_len is None:
            return self._stretchfactor
        if stretch_wid == 0 or stretch_len == 0:
            raise TurtleGraphicsError("stretch_wid/stretch_len must not be zero")
        if stretch_wid is not None:
            if stretch_len is None:
                self._stretchfactor = stretch_wid, stretch_wid
            else:
                self._stretchfactor = stretch_wid, stretch_len
        elif stretch_len is not None:
            self._stretchfactor = self._stretchfactor[0], stretch_len
        else:
            self._stretchfactor = self._stretchfactor
        self._update()

    def shearfactor(self, shear: int | float = None) -> None | float:
        """Set or return the current shearfactor.

        Optional argument: `shear` -- number, tangent of the shear angle

        Shear the turtleshape according to the given shearfactor `shear`,
        which is the tangent of the shear angle. Doesn't change the
        turtle's heading (direction of movement).
        If `shear` is not given: return the current shearfactor, i. e. the
        tangent of the shear angle, by which lines parallel to the
        heading of the turtle are sheared.

        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.shape("circle")
        t.shapesize(5,2)
        t.shearfactor(0.5)
        print(t.shearfactor()) # 0.5
        ```
        """
        if shear is None:
            return self._shearfactor
        self._shearfactor = shear

    def tiltangle(self, angle: int | float = None) -> None | float:
        """Set or return the current tilt-angle.

        Optional argument: `angle` -- number

        Rotate the turtleshape to point in the direction specified by `angle`,
        regardless of its current tilt-angle. Doesn't change the turtle's
        heading (direction of movement).
        If `angle` is not given: return the current tilt-angle, i. e. the angle
        between the orientation of the turtleshape and the heading of the
        turtle (its direction of movement).

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.shape("circle")
        t.shapesize(5, 2)
        print(t.tiltangle()) # 0.0
        t.tiltangle(45)
        print(t.tiltangle()) # 45.0
        t.stamp()
        t.fd(50)
        t.tiltangle(-45)
        print(t.tiltangle()) # 315.0
        t.stamp()
        t.fd(50)
        ```
        """
        if angle is None:
            tilt = -math.degrees(self._tilt) * self._angleOrient
            return (tilt / self._degreesPerAU) % self._fullcircle
        else:
            tilt = -angle * self._degreesPerAU * self._angleOrient
            tilt = math.radians(tilt) % math.tau
            self._tilt = tilt

    def tilt(self, angle: int | float):
        """Rotate the turtleshape by angle.

        Argument:
        `angle` - a number

        Rotate the turtleshape by `angle` from its current tilt-angle,
        but don't change the turtle's heading (direction of movement).

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.shape("circle")
        t.shapesize(5,2)
        t.tilt(30)
        t.fd(50)
        t.tilt(30)
        t.fd(50)
        ```
        """
        self.tiltangle(angle + self.tiltangle())

    # ========================================
    #                Screen
    # ========================================

    def bgcolor(self, color: str | tuple[int | float] = None) -> None | str:
        """Set or return backgroundcolor of the turtle's screen.

        Arguments:
        Four input formats are allowed:
          - `bgcolor()`
            Return the current background as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - `bgcolor(colorstring)`
            a [Tk color specification string](https://www.tcl-lang.org/man/tcl8.4/TkCmd/colors.htm),
            such as `"red"` or `"yellow"`
          - `bgcolor((r, g, b))`
            *a tuple* of `r`, `g`, and `b`, which represent, an RGB color,
            and each of `r`, `g`, and `b` are in the range `0..colormode`,
            where `colormode` is either 1.0 or 255
          - `bgcolor(r, g, b)`
            `r`, `g`, and `b` represent an RGB color, and each of `r`, `g`,
            and `b` are in the range `0..colormode`

        **Example**
        ```python
        from ipycc.turtle import Turtle

        t = Turtle()
        t.show()

        t.bgcolor("orange")
        print(t.bgcolor()) # 'orange'
        ```
        """
        if color is None:
            return self._screen._bgcolor
        self._screen._bgcolor = self._colorstr(color)
        self._update()


__all__ = ["Turtle", "Vec2D", "tracer", "setup", "showscreen", "clearscreen", "resetscreen"]
