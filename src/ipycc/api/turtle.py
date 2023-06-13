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
        self._bgcolor = "white"
        self._pen = Sketch(self.width, self.height)
        self.reset()
        self.end_poly()

    def _render(self):
        with hold_canvas():
            self._bg.background(self._bgcolor)
            # TODO: implement push() and pop()
            self._bg.scale(1, -1)
            self._bg.translate(0, -self.height)
            self._bg.image(self._pen.canvas, 0, 0)
            self._bg.translate(self._x, self._y)
            self._bg.rotate(self._angle)
            self._bg.stroke(self._pencolor)
            self._bg.stroke_weight(2)
            self._bg.fill(self._fillcolor)
            self._bg.triangle(0, -4, 0, 4, 8, 0)
            self._bg.reset_matrix()

    def draw(self):
        """Display the turtle's drawing canvas."""
        self._render()
        self._bg.run_sketch()

    def remove(self):
        """Remove the turtle's drawing canvas."""
        self._pen.remove()

    # ========================================
    #              Turtle Motion
    # ========================================

    def forward(self, distance):
        """Move the turtle forward by the specified distance.

        Aliases: forward | fd

        Argument:
        distance -- a number (integer or float)

        Move the turtle forward by the specified distance, in the direction
        the turtle is headed.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.forward(25)
        >>> turtle.position()
        (25.00,0.00)
        >>> turtle.forward(-75)
        >>> turtle.position()
        (-50.00,0.00)
        """
        x = self._x + distance * math.cos(self._angle)
        y = self._y + distance * math.sin(self._angle)
        if self._is_drawing:
            self._pen.line(self._x, self._y, x, y)
        self._x = x
        self._y = y
        if self._is_drawing_poly:
            self._pen.vertex(x, y)
        self._render()

    def fd(self, distance):
        """Move the turtle forward by the specified distance.

        Aliases: forward | fd

        Argument:
        distance -- a number (integer or float)

        Move the turtle forward by the specified distance, in the direction
        the turtle is headed.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.forward(25)
        >>> turtle.position()
        (25.00,0.00)
        >>> turtle.forward(-75)
        >>> turtle.position()
        (-50.00,0.00)
        """
        self.forward(distance)

    def backward(self, distance):
        """Move the turtle backward by distance.

        Aliases: back | backward | bk

        Argument:
        distance -- a number

        Move the turtle backward by distance, opposite to the direction the
        turtle is headed. Do not change the turtle's heading.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.backward(30)
        >>> turtle.position()
        (-30.00, 0.00)
        """
        self.forward(-distance)

    def bk(self, distance):
        """Move the turtle backward by distance.

        Aliases: back | backward | bk

        Argument:
        distance -- a number

        Move the turtle backward by distance, opposite to the direction the
        turtle is headed. Do not change the turtle's heading.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.backward(30)
        >>> turtle.position()
        (-30.00, 0.00)
        """
        self.forward(-distance)

    def back(self, distance):
        """Move the turtle backward by distance.

        Aliases: back | backward | bk

        Argument:
        distance -- a number

        Move the turtle backward by distance, opposite to the direction the
        turtle is headed. Do not change the turtle's heading.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.backward(30)
        >>> turtle.position()
        (-30.00, 0.00)
        """
        self.forward(-distance)

    def right(self, angle):
        """Turn turtle right by angle units.

        Aliases: right | rt

        Argument:
        angle -- a number (integer or float)

        Turn turtle right by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.right(45)
        >>> turtle.heading()
        337.0
        """
        self._angle -= math.radians(angle)
        self._render()

    def rt(self, angle):
        """Turn turtle right by angle units.

        Aliases: right | rt

        Argument:
        angle -- a number (integer or float)

        Turn turtle right by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.right(45)
        >>> turtle.heading()
        337.0
        """
        self._angle -= math.radians(angle)
        self._render()

    def left(self, angle):
        """Turn turtle left by angle units.

        Aliases: left | lt

        Argument:
        angle -- a number (integer or float)

        Turn turtle left by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.left(45)
        >>> turtle.heading()
        67.0
        """
        self._angle += math.radians(angle)
        self._render()

    def lt(self, angle):
        """Turn turtle left by angle units.

        Aliases: left | lt

        Argument:
        angle -- a number (integer or float)

        Turn turtle left by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.left(45)
        >>> turtle.heading()
        67.0
        """
        self._angle += math.radians(angle)
        self._render()

    def goto(self, x, y):
        """Move turtle to an absolute position.

        Aliases: setpos | setposition | goto:

        Arguments:
        x -- a number
        y -- a number

        call: goto(x, y)         # two coordinates

        Move turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.

        Example (for a Turtle instance named turtle):
        >>> tp = turtle.pos()
        >>> tp
        (0.00, 0.00)
        >>> turtle.setpos(60,30)
        >>> turtle.pos()
        (60.00,30.00)
        """
        next_x = self.width * 0.5 + x
        next_y = self.height * 0.5 + y
        if self._is_drawing:
            self._pen.line(self._x, self._y, next_x, next_y)
        if self._is_drawing_poly:
            self._pen.vertex(next_x, next_y)
        self._x = next_x
        self._y = next_y
        self._render()

    def setpos(self, x, y):
        """Move turtle to an absolute position.

        Aliases: setpos | setposition | goto:

        Arguments:
        x -- a number
        y -- a number

        call: goto(x, y)         # two coordinates

        Move turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.

        Example (for a Turtle instance named turtle):
        >>> tp = turtle.pos()
        >>> tp
        (0.00, 0.00)
        >>> turtle.setpos(60,30)
        >>> turtle.pos()
        (60.00,30.00)
        """
        self.goto(x, y)

    def setposition(self, x, y):
        """Move turtle to an absolute position.

        Aliases: setpos | setposition | goto:

        Arguments:
        x -- a number
        y -- a number

        call: goto(x, y)         # two coordinates

        Move turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.

        Example (for a Turtle instance named turtle):
        >>> tp = turtle.pos()
        >>> tp
        (0.00, 0.00)
        >>> turtle.setpos(60,30)
        >>> turtle.pos()
        (60.00,30.00)
        """
        self.goto(x, y)

    def setx(self, x):
        """Set the turtle's first coordinate to x

        Argument:
        x -- a number (integer or float)

        Set the turtle's first coordinate to x, leave second coordinate
        unchanged.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 240.00)
        >>> turtle.setx(10)
        >>> turtle.position()
        (10.00, 240.00)
        """
        next_x = self.width * 0.5 + x
        if self._is_drawing:
            self._pen.line(self._x, self._y, next_x, self._y)
        if self._is_drawing_poly:
            self._pen.vertex(next_x, self._y)
        self._x = next_x
        self._render()

    def sety(self, y):
        """Set the turtle's second coordinate to y

        Argument:
        y -- a number (integer or float)

        Set the turtle's first coordinate to x, second coordinate remains
        unchanged.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 40.00)
        >>> turtle.sety(-10)
        >>> turtle.position()
        (0.00, -10.00)
        """
        next_y = 0.5 * self.height + y
        if self._is_drawing:
            self._pen.line(self._x, self._y, self._x, next_y)
        if self._is_drawing_poly:
            self._pen.vertex(self._x, next_y)
        self._y = next_y
        self._render()

    def setheading(self, angle):
        """Set the orientation of the turtle to to_angle.

        Aliases:  setheading | seth

        Argument:
        to_angle -- a number (integer or float)

        Set the orientation of the turtle to to_angle.
        Here are some common directions in degrees:

         standard - mode:          logo-mode:
        -------------------|--------------------
           0 - east                0 - north
          90 - north              90 - east
         180 - west              180 - south
         270 - south             270 - west

        Example (for a Turtle instance named turtle):
        >>> turtle.setheading(90)
        >>> turtle.heading()
        90
        """
        self._angle = math.radians(angle)
        self._render()

    def seth(self, angle):
        """Set the orientation of the turtle to to_angle.

        Aliases:  setheading | seth

        Argument:
        to_angle -- a number (integer or float)

        Set the orientation of the turtle to to_angle.
        Here are some common directions in degrees:

         standard - mode:          logo-mode:
        -------------------|--------------------
           0 - east                0 - north
          90 - north              90 - east
         180 - west              180 - south
         270 - south             270 - west

        Example (for a Turtle instance named turtle):
        >>> turtle.setheading(90)
        >>> turtle.heading()
        90
        """
        self._angle = math.radians(angle)
        self._render()

    def home(self):
        """Move turtle to the origin - coordinates (0,0).

        No arguments.

        Move turtle to the origin - coordinates (0,0) and set its
        heading to its start-orientation (which depends on mode).

        Example (for a Turtle instance named turtle):
        >>> turtle.home()
        """
        self.goto(0, 0)
        self.seth(0)

    def speed(self, speed=None):
        """Return or set the turtle's speed.

        Optional argument:
        speed -- an integer in the range 0..10 or a speedstring (see below)

        Set the turtle's speed to an integer value in the range 0 .. 10.
        If no argument is given: return current speed.

        If input is a number greater than 10 or smaller than 0.5,
        speed is set to 0.
        Speedstrings  are mapped to speedvalues in the following way:
            'fastest' :  0
            'fast'    :  10
            'normal'  :  6
            'slow'    :  3
            'slowest' :  1
        speeds from 1 to 10 enforce increasingly faster animation of
        line drawing and turtle turning.

        Attention:
        speed = 0 : *no* animation takes place. forward/back makes turtle jump
        and likewise left/right make the turtle turn instantly.

        Example (for a Turtle instance named turtle):
        >>> turtle.speed(3)
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

    def position(self):
        """Return the turtle's current location (x,y), as a tuple.

        Aliases: pos | position

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.pos()
        (0.00, 240.00)
        """
        return (self.xcor(), self.ycor())

    def pos(self):
        """Return the turtle's current location (x,y), as a tuple.

        Aliases: pos | position

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.pos()
        (0.00, 240.00)
        """
        return (self.xcor(), self.ycor())

    def xcor(self):
        """Return the turtle's x coordinate.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> reset()
        >>> turtle.left(60)
        >>> turtle.forward(100)
        >>> turtle.xcor()
        50.0
        """
        return self._x - self.width * 0.5

    def ycor(self):
        """Return the turtle's y coordinate
        ---
        No arguments.

        Example (for a Turtle instance named turtle):
        >>> reset()
        >>> turtle.left(60)
        >>> turtle.forward(100)
        >>> turtle.ycor()
        86.6025403784
        """
        return self._y - self.height * 0.5

    def heading(self):
        """Return the turtle's current heading.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.left(67)
        >>> turtle.heading()
        67.0
        """
        return math.degrees(self._angle) % 360

    # ========================================
    #               Pen Control
    # ========================================

    def pendown(self):
        """Pull the pen down -- drawing when moving.

        Aliases: pendown | pd | down

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pendown()
        """
        self._is_drawing = True

    def pd(self):
        """Pull the pen down -- drawing when moving.

        Aliases: pendown | pd | down

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pendown()
        """
        self._is_drawing = True

    def down(self):
        """Pull the pen down -- drawing when moving.

        Aliases: pendown | pd | down

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pendown()
        """
        self._is_drawing = True

    def penup(self):
        """Pull the pen up -- no drawing when moving.

        Aliases: penup | pu | up

        No argument

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        """
        self._is_drawing = False

    def pu(self):
        """Pull the pen up -- no drawing when moving.

        Aliases: penup | pu | up

        No argument

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        """
        self._is_drawing = False

    def up(self):
        """Pull the pen up -- no drawing when moving.

        Aliases: penup | pu | up

        No argument

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        """
        self._is_drawing = False

    def pensize(self, width=None):
        """Set or return the line thickness.

        Aliases:  pensize | width

        Argument:
        width -- positive number

        Set the line thickness to width or return it. If resizemode is set
        to "auto" and turtleshape is a polygon, that polygon is drawn with
        the same line thickness. If no argument is given, current pensize
        is returned.

        Example (for a Turtle instance named turtle):
        >>> turtle.pensize()
        1
        >>> turtle.pensize(10)   # from here on lines of width 10 are drawn
        """
        if width is None:
            return self._pensize
        self._pensize = width
        self._pen.stroke_weight(self._pensize)

    def isdown(self):
        """Return True if pen is down, False if it's up.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        >>> turtle.isdown()
        False
        >>> turtle.pendown()
        >>> turtle.isdown()
        True
        """
        return self._is_drawing

    def color(self, color=None):
        """Return or set the pencolor and fillcolor.

        Arguments:
        Two input formats are allowed.
        They use 0 or 1 arguments as follows:

        color()
            Return the current pencolor and the current fillcolor
            as a pair of color specification strings as are returned
            by pencolor and fillcolor.
        color(colorstring)
            inputs as in pencolor, set both, fillcolor and pencolor,
            to the given value.
        If turtleshape is a polygon, outline and interior of that polygon
        is drawn with the newly set colors.
        For more info see: pencolor, fillcolor

        Example (for a Turtle instance named turtle):
        >>> turtle.color()
        ('black', 'white')
        >>> turtle.color("red")
        >>> turtle.color()
        ('red', 'red')
        """
        if color is None:
            return (self._pencolor, self._fillcolor)
        self.pencolor(color)
        self.fillcolor(color)

    def pencolor(self, color=None):
        """Return or set the pencolor.

        Arguments:
        Two input formats are allowed:
          - pencolor()
            Return the current pencolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - pencolor(colorstring)
            s is a CSS color string, such as "red" or "#ff0000"

        If turtleshape is a polygon, the outline of that polygon is drawn
        with the newly set pencolor.

        Example (for a Turtle instance named turtle):
        >>> turtle.pencolor('red')
        >>> turtle.pencolor()
        'red'
        """
        if color is None:
            return self._pencolor
        self._pencolor = color
        self._pen.stroke(self._pencolor)
        self._render()

    def fillcolor(self, color=None):
        """Return or set the fillcolor.

        Arguments:
        Four input formats are allowed:
          - fillcolor()
            Return the current fillcolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - fillcolor(colorstring)
            s is a CSS color string, such as "red" or "#ff0000"

        If turtleshape is a polygon, the interior of that polygon is drawn
        with the newly set fillcolor.

        Example (for a Turtle instance named turtle):
        >>> turtle.fillcolor('violet')
        >>> col = turtle.pencolor()
        >>> turtle.fillcolor(col)
        """
        if color is None:
            return self._fillcolor
        self._fillcolor = color
        self._render()

    def clear(self):
        """Delete the turtle's drawings from the screen. Do not move turtle.

        No arguments.

        Delete the turtle's drawings from the screen. Do not move turtle.
        State and position of the turtle as well as drawings of other
        turtles are not affected.

        Examples (for a Turtle instance named turtle):
        >>> turtle.clear()
        """
        self._pen.clear()
        self._render()

    def reset(self):
        """Return the turtle to its initial state and clear its drawings from
        the screen.

        No arguments.

        Examples (for a Turtle instance named turtle):
        >>> turtle.reset()
        """
        self._is_drawing = True
        self._pencolor = "black"
        self._pensize = 1
        self._speed = 1
        self._pen.stroke(self._pencolor)
        self._pen.stroke_weight(self._pensize)
        self._is_filling = False
        self._fillcolor = "white"
        self._pen.no_fill()
        self._is_drawing_poly = False
        self._x = self.width * 0.5
        self._y = self.height * 0.5
        self._angle = 0
        self.clear()

    def begin_poly(self):
        """Start recording the vertices of a polygon.

        No argument.

        Start recording the vertices of a polygon. Current turtle position
        is first point of polygon.

        Example (for a Turtle instance named turtle):
        >>> turtle.begin_poly()
        """
        if self._is_drawing:
            self._pen.begin_shape()
            self._is_drawing_poly = True

    def end_poly(self):
        """Stop recording the vertices of a polygon.

        No argument.

        Stop recording the vertices of a polygon. Current turtle position is
        last point of polygon. This will be connected with the first point.

        Example (for a Turtle instance named turtle):
        >>> turtle.end_poly()
        """
        self._pen.end_shape()
        if self._is_drawing_poly:
            self._render()
        self._is_drawing_poly = False

    def begin_fill(self):
        """Called just before drawing a shape to be filled.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pencolor("black")
        >>> turtle.fillcolor("red")
        >>> turtle.begin_fill()
        >>> turtle.circle(60)
        >>> turtle.end_fill()
        """
        self._is_filling = True
        self._pen.fill(self._fillcolor)

    def end_fill(self):
        """Fill the shape drawn after the call begin_fill().

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pencolor("black")
        >>> turtle.fillcolor("red")
        >>> turtle.begin_fill()
        >>> turtle.circle(60)
        >>> turtle.end_fill()
        """
        self._is_filling = False
        self._pen.no_fill()

    def filling(self):
        """Return fillstate (True if filling, False else).

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.begin_fill()
        >>> if turtle.filling():
        ...     turtle.pensize(5)
        ... else:
        ...     turtle.pensize(3)
        """
        return self._is_filling

    # ========================================
    #                Screen
    # ========================================

    def bgcolor(self, color=None):
        """Set or return backgroundcolor of the TurtleScreen.

        Arguments (if given): a color string or three numbers
        in the range 0..colormode or a 3-tuple of such numbers.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bgcolor("orange")
        >>> screen.bgcolor()
        'orange'
        """
        if color is None:
            return self._bgcolor
        self._bgcolor = color
        self._render()

    async def delay(self, secs):
        """Delay drawing for a given number of seconds.

        Optional argument:
        delay -- positive integer

        Example (for a TurtleScreen instance named screen):
        >>> for side in range(4):
        ...     turtle.fd(10)
        ...     turtle.lt(90)
        ...     await turtle.delay(1)
        """
        await asyncio.sleep(secs)
