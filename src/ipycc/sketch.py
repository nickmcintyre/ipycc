import math
import time
from typing import Callable, Self
from ipycanvas import Canvas, hold_canvas
from IPython.display import display
import numpy as np


class SketchError(Exception):
    """Some Sketch Error.
    """


class Sketch:
    """A class to describe a 2D drawing canvas."""

    # Constants
    HALF_PI: float = math.pi / 2.0
    """A number constant that's approximately 1.5708."""

    PI: float = math.pi
    """A number constant that's approximately 3.1416."""

    QUARTER_PI: float = math.pi / 4.0
    """A number constant that's approximately 0.7854."""

    TAU: float = math.tau
    """A number constant that's approximately 6.2382."""

    TWO_PI: float = math.tau
    """A number constant that's approximately 6.2382."""

    NORMAL: str = "normal"
    """A string constant used with the `text_style()` method."""

    ITALIC: str = "italic"
    """A string constant used with the `text_style()` method."""

    BOLD: str = "bold"
    """A string constant used with the `text_style()` method."""

    BOLDITALIC: str = "bolditalic"
    """A string constant used with the `text_style()` method."""

    LEFT: str = "left"
    """A string constant used with the `text_align()` method."""

    CENTER: str = "center"
    """A string constant used with the `text_align()` method."""

    RIGHT: str = "right"
    """A string constant used with the `text_align()` method."""

    BOTTOM: str = "bottom"
    """A string constant used with the `text_align()` method."""

    TOP: str = "top"
    """A string constant used with the `text_align()` method."""

    BASELINE: str = "alphabetic"
    """A string constant used with the `text_align()` method."""

    MIDDLE: str = "middle"
    """A string constant used with the `text_align()` method."""

    _DEFAULT_STROKE = "black"
    _DEFAULT_STROKE_WEIGHT = 1
    _DEFAULT_LINE_CAP = "round"
    _DEFAULT_FILL = "white"
    _DEFAULT_TEXT_FILL = "black"
    _DEFAULT_TEXT_WEIGHT = 0.3
    _DEFAULT_TEXT_ALIGN = LEFT
    _DEFAULT_TEXT_BASELINE = BASELINE
    _TRANSPARENT = "#00000000"
    _DEFAULT_FONT = "Arial"
    _DEFAULT_FONT_SIZE = 12
    _DEFAULT_FONT_STYLE = "normal"
    _DEFAULT_FONT_WEIGHT = "normal"

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        pixel_denstiy: int = 2,
    ):
        # Create the Canvas.
        self.width: int = width
        """The width of the canvas in pixels."""

        self.height: int = height
        """The height of the canvas in pixels."""

        self.pixel_density: int = pixel_denstiy
        """The number of physical pixels used to draw a pixel on the canvas."""

        self.canvas: Canvas = Canvas(
            width=width * pixel_denstiy,
            height=height * pixel_denstiy,
            layout={"width": f"{width}px", "height": f"{height}px"})
        """The `Canvas` widget used for drawing."""
        
        # Set default the styles.
        self._init_style()
        # Set the default transformations.
        self._init_transformation()
        # Create an empty list for shape vertices.
        self._vertices = []
        # Set the current frame count (for animation).
        self.frame_count: int = 0
        """The number of frames drawn since the sketch started."""

        self._is_looping = False

    def _init_transformation(self):
        sx = self.pixel_density
        sy = self.pixel_density
        self._matrix = np.array([[sx,  0,  0],
                                 [ 0, sy,  0],
                                 [ 0,  0,  1]], dtype=float)
        self.canvas.scale(self.pixel_density, y=self.pixel_density)

    def _init_style(self):
        # Set initial styles.
        self.canvas.fill_style = Sketch._DEFAULT_FILL
        self.canvas.stroke_style = Sketch._DEFAULT_STROKE
        self.canvas.line_width = Sketch._DEFAULT_STROKE_WEIGHT
        self.canvas.line_cap = Sketch._DEFAULT_LINE_CAP
        self._is_fill_set = False
        self._is_stroke_set = False
        self._is_stroke_weight_set = False
        self._font = Sketch._DEFAULT_FONT
        self._font_size = Sketch._DEFAULT_FONT_SIZE
        self._font_style = Sketch._DEFAULT_FONT_STYLE
        self._font_weight = Sketch._DEFAULT_FONT_WEIGHT
        self._text_align = Sketch._DEFAULT_TEXT_ALIGN
        self._text_baseline = Sketch._DEFAULT_TEXT_BASELINE
        self.canvas.text_align = self._text_align
        self.canvas.text_baseline = self._text_baseline
        self.canvas.font = (
            f"{self._font_style} {self._font_weight} {self._font_size}px {self._font}"
        )

    # ========================================
    #                 Color
    # ========================================

    def background(self, *args):
        """Sets the color used for the background of the canvas.

        The version of `background()` with one parameter interprets the value
        one of four ways. If the parameter is an int or float, it's
        interpreted as a grayscale value. If the parameter is a string,
        it's interpreted as a CSS color string. RGB, RGBA, HSL, HSLA, hex,
        and named color strings are supported.

        The version of `background()` with two parameters interprets the first
        one as a grayscale value. The second parameter sets the alpha
        (transparency) value.

        The version of `background()` with three parameters interprets them as
        RGB. Calling `background(255, 204, 0)` sets the background a bright
        yellow color.

        The version of `background()` with four parameters interprets them as
        RGBA. Calling `background(255, 204, 0, 20)` sets the background a
        bright yellow color that is transparent.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()
        ```

        ```python
        # A grayscale value.
        s.background(51)
        ```

        ```python
        # A grayscale value and an alpha value.
        s.background(51, 0.4)
        ```

        ```python
        # R, G & B values.
        s.background(255, 204, 0)
        ```

        ```python
        # A CSS named color.
        s.background("red")
        ```

        ```python
        # Integer RGBA notation.
        s.background("rgba(0, 255, 0, 0.25)")
        ```

        ```python
        # R, G, B & A values.
        s.background(0, 255, 0, 64)
        ```
        """
        if len(args) == 0:
            return
        color = self._colorstr(*args)
        self.canvas.save()
        self.canvas.reset_transform()
        self.canvas.scale(self.pixel_density, y=self.pixel_density)
        old_fill = self.canvas.fill_style
        old_stroke = self.canvas.stroke_style
        old_weight = self.canvas.line_width
        self.canvas.fill_style = color
        self.canvas.stroke_style = color
        self.canvas.line_width = 1
        self.canvas.fill_rect(0, 0, self.canvas.width, self.canvas.height)
        self.canvas.stroke_rect(0, 0, self.canvas.width, self.canvas.height)
        self.canvas.fill_style = old_fill
        self.canvas.stroke_style = old_stroke
        self.canvas.line_width = old_weight
        self.canvas.restore()

    def _colorstr(self, *args) -> str:
        """Return a CSS color string corresponding to args.
        """
        num = (int, float)
        color = ""
        if len(args) == 1:
            c = args[0]
            if isinstance(c, num):
                color = f"rgb({c}, {c}, {c})"
            elif isinstance(color, str):
                color = c
        elif len(args) == 2:
            c = args[0]
            a = args[1]
            if isinstance(c, num) and isinstance(a, num):
                color = f"rgba({c}, {c}, {c}, {a / 255})"
        elif len(args) == 3:
            r = args[0]
            g = args[1]
            b = args[2]
            if isinstance(r, num) and isinstance(g, num) and isinstance(b, num):
                color = f"rgb({r}, {g}, {b})"
        elif len(args) == 4:
            r = args[0]
            g = args[1]
            b = args[2]
            a = args[3]
            if isinstance(r, num) and isinstance(g, num) and isinstance(b, num) and isinstance(a, num):
                color = f"rgba({r}, {g}, {b}, {a / 255})"
        return color

    def fill(self, *args):
        """Sets the color used to fill shapes.

        Calling `fill(255, 165, 0)` or `fill("orange")` means all shapes drawn
        after calling `fill()` will be filled with the color orange.

        The version of `fill()` with one parameter interprets the value one of
        three ways. If the parameter is an int or float, it's interpreted as a
        grayscale value. If the parameter is a string, it's interpreted as a
        CSS color string. RGB, RGBA, HSL, HSLA, hex, and named color strings
        are supported.

        The version of `fill()` with two parameters interprets the first one
        as a grayscale value. The second parameter sets the alpha
        (transparency) value.

        The version of `fill()` with three parameters interprets them as RGB
        colors.

        The version of `fill()` with four parameters interprets them as RGBA
        colors. The last parameter sets the alpha (transparency) value.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()
        ```

        ```python
        # A grayscale value.
        s.background(200)
        s.no_stroke()
        s.fill(51)
        s.square(20, 20, 60)
        ```

        ```python
        # Grayscale and alpha values.
        s.background(200)
        s.no_stroke()
        s.fill(51, 64)
        s.square(20, 20, 60)
        ```

        ```python
        # R, G & B values.
        s.background(200)
        s.no_stroke()
        s.fill(255, 204, 0)
        s.square(20, 20, 60)
        ```

        ```python
        # A CSS named color.
        s.background(200)
        s.no_stroke()
        s.fill("red")
        s.square(20, 20, 60)
        ```

        ```python
        # Integer RGBA notation.
        s.background(200)
        s.no_stroke()
        s.fill("rgba(0, 255, 0, 0.25)")
        s.square(20, 20, 60)
        ```

        ```python
        # R, G, B & A values.
        s.background(200)
        s.no_stroke()
        s.fill(0, 255, 0, 64)
        s.square(20, 20, 60)
        ```
        """
        if len(args) == 0:
            return
        color = self._colorstr(*args)
        if not self._is_fill_set:
            self._is_fill_set = True
        self.canvas.fill_style = color

    def no_fill(self):
        """Disables setting the fill color for shapes.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.no_stroke()
        s.square(20, 20, 60)
        ```
        """
        if not self._is_fill_set:
            self._is_fill_set = True
        self.canvas.fill_style = Sketch._TRANSPARENT

    def no_stroke(self):
        """Disables drawing points, lines, and the outlines of shapes.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.no_stroke()
        s.square(20, 20, 60)
        ```
        """
        if not self._is_stroke_set:
            self._is_stroke_set = True
        self.canvas.stroke_style = Sketch._TRANSPARENT

    def stroke(self, *args):
        """Sets the color used to draw points, lines, and the outlines of shapes.

        Calling `stroke(255, 165, 0)` or `stroke("orange")` means all shapes
        drawn after calling `stroke()` will be outlined with the color orange.

        The version of `stroke()` with one parameter interprets the value one
        of three ways. If the parameter is a number, it's interpreted as a
        grayscale value. If the parameter is a string, it's interpreted as a
        CSS color string. RGB, RGBA, HSL, HSLA, hex, and named color strings
        are supported.

        The version of `stroke()` with two parameters interprets the first one
        as a grayscale value. The second parameter sets the alpha
        (transparency) value.

        The version of `stroke()` with three parameters interprets them as RGB
        colors.

        The version of `stroke()` with four parameters interprets them as RGBA
        colors. The last parameter sets the alpha (transparency) value.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()
        ```

        ```python
        # A grayscale value.
        s.background(200)
        s.stroke_weight(4)
        s.stroke(51)
        s.square(20, 20, 60)
        ```

        ```python
        # Grayscale and alpha values.
        s.background(200)
        s.stroke(51, 64)
        s.square(20, 20, 60)
        ```

        ```python
        # R, G & B values.
        s.background(200)
        s.stroke(255, 204, 0)
        s.square(20, 20, 60)
        ```

        ```python
        # A CSS named color.
        s.background(200)
        s.stroke("red")
        s.square(20, 20, 60)
        ```

        ```python
        # Integer RGBA notation.
        s.background(200)
        s.stroke("rgba(0, 255, 0, 0.25)")
        s.square(20, 20, 60)
        ```

        ```python
        # R, G, B & A values.
        s.background(200)
        s.stroke(0, 255, 0, 64)
        s.square(20, 20, 60)
        ```
        """
        if len(args) == 0:
            return
        color = self._colorstr(*args)
        if not self._is_stroke_set:
            self._is_stroke_set = True
        self.canvas.stroke_style = color

    def clear(self):
        """Clears all drawings on the canvas.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.clear()
        ```
        """
        self.canvas.clear()

    def reset(self):
        """Resets the canvas to its default state.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.reset()
        ```
        """
        self.clear()
        self.canvas.reset_transform()
        self._init_style()
        self._init_transformation()

    # ========================================
    #              2D Primitives
    # ========================================

    def _acute_arc_to_bezier(self, start: int | float, size: int | float) -> dict:
        # Evaluate constants.
        alpha = size * 0.5
        cos_alpha = math.cos(alpha)
        sin_alpha = math.sin(alpha)
        cot_alpha = 1 / math.tan(alpha)
        # This is how far the arc needs to be rotated.
        phi = start + alpha
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        lam = (4.0 - cos_alpha) / 3
        mu = sin_alpha + (cos_alpha - lam) * cot_alpha

        # Return rotated waypoints.
        return {
            "ax": round(math.cos(start), 7),
            "ay": round(math.sin(start), 7),
            "bx": round((lam * cos_phi + mu * sin_phi), 7),
            "by": round((lam * sin_phi - mu * cos_phi), 7),
            "cx": round((lam * cos_phi - mu * sin_phi), 7),
            "cy": round((lam * sin_phi + mu * cos_phi), 7),
            "dx": round(math.cos(start + size), 7),
            "dy": round(math.sin(start + size), 7),
        }

    def arc(
        self,
        x: int | float,
        y: int | float,
        w: int | float,
        h: int | float,
        start: int | float,
        stop: int | float,
    ):
        """Draws an arc.

        An arc is a section of an ellipse defined by the `x`, `y`, `w`, and
        `h` parameters. `x` and `y` set the location of the arc's center. `w`
        and `h` set the arc's width and height.
        
        The fifth and sixth parameters, `start` and `stop`, set the angles
        between which to draw the arc. Arcs are always drawn clockwise from
        `start` to `stop`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Bottom-right.
        s.arc(50, 55, 50, 50, 0, s.HALF_PI)

        s.no_fill()
        
        # Bottom-left.
        s.arc(50, 55, 60, 60, s.HALF_PI, s.PI)
        
        # Top-left.
        s.arc(50, 55, 70, 70, s.PI, s.PI + s.QUARTER_PI)
        
        # Top-right.
        s.arc(50, 55, 80, 80, s.PI + s.QUARTER_PI, s.TWO_PI)
        ```
        """
        rx = w * 0.5
        ry = h * 0.5
        epsilon = 0.00001  # Smallest visible angle on displays up to 4K.
        arc_to_draw = 0
        curves = []

        # Create curves
        while stop - start >= epsilon:
            arc_to_draw = min(stop - start, Sketch.HALF_PI)
            curves.append(self._acute_arc_to_bezier(start, arc_to_draw))
            start += arc_to_draw

        self.canvas.begin_path()
        for index, curve in enumerate(curves):
            if index == 0:
                self.canvas.move_to(x + curve["ax"] * rx, y + curve["ay"] * ry)
            self.canvas.bezier_curve_to(
                x + curve["bx"] * rx,
                y + curve["by"] * ry,
                x + curve["cx"] * rx,
                y + curve["cy"] * ry,
                x + curve["dx"] * rx,
                y + curve["dy"] * ry,
            )
        self.canvas.line_to(x, y)
        self.canvas.close_path()
        self.canvas.fill()
        self.canvas.stroke()

    def ellipse(self, x: int | float, y: int | float, w: int | float, h: int | float):
        """Draws an ellipse (oval).

        An ellipse is a round shape defined by the `x`, `y`, `w`, and `h`
        parameters. `x` and `y` set the location of its center. `w` and `h`
        set its width and height.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # A circle.
        s.ellipse(20, 20, 40, 40)
        
        # An oval.
        s.ellipse(80, 80, 40, 20)
        ```
        """
        dx = w * 0.5
        dy = h * 0.5
        cx = x - dx
        cy = y - dy

        kappa = 0.5522847498
        # control point offset horizontal
        ox = w * 0.5 * kappa
        # control point offset vertical
        oy = h * 0.5 * kappa
        # x-end
        xe = cx + w
        # y-end
        ye = cy + h
        # x-middle
        xm = cx + w * 0.5
        # y-middle
        ym = cy + h * 0.5
        self.canvas.begin_path()
        self.canvas.move_to(cx, ym)
        self.canvas.bezier_curve_to(cx, ym - oy, xm - ox, cy, xm, cy)
        self.canvas.bezier_curve_to(xm + ox, cy, xe, ym - oy, xe, ym)
        self.canvas.bezier_curve_to(xe, ym + oy, xm + ox, ye, xm, ye)
        self.canvas.bezier_curve_to(xm - ox, ye, cx, ym + oy, cx, ym)
        self.canvas.fill()
        self.canvas.stroke()

    def circle(self, x: int | float, y: int | float, d: int | float):
        """Draws a circle.

        A circle is a round shape defined by the `x`, `y`, and `d` parameters.
        `x` and `y` set the location of its center. `d` sets its width and
        height (diameter). Every point on the circle's edge is the same
        distance, `0.5 * d`, from its center. `0.5 * d` (half the diameter) is
        the circle's radius.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.circle(50, 50, 25)
        ```
        """
        r = d * 0.5
        self.canvas.fill_circle(x, y, r)
        self.canvas.stroke_circle(x, y, r)

    def line(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float):
        """Draws a straight line between two points.

        A line's default width is one pixel. The first two parameters set the
        starting coordinates of the line. The next two parameters set the
        ending coordinates of the line. To color a line, use the `stroke()`
        method. To change its width, use the `stroke_weight()` method.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.line(30, 20, 85, 75)
        
        # Style the line.
        s.background(200)
        s.stroke("magenta")
        s.stroke_weight(5)
        s.line(30, 20, 85, 75)
        ```
        """
        self.canvas.stroke_line(x1, y1, x2, y2)

    def point(self, x: int | float, y: int | float):
        """Draws a single point in space.

        A point's default width is one pixel. To color a point, use the
        `stroke()` method. To change its width, use the `stroke_weight()`
        method. A point can't be filled, so the `fill()` method won't
        affect the point's color.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        
        # Top-left.
        s.point(30, 20)
        
        # Top-right. 
        s.point(85, 20)
        
        # Style the next points.
        s.stroke("purple")
        s.stroke_weight(10)
        
        # Bottom-right.
        s.point(85, 75)
        
        # Bottom-left.
        s.point(30, 75)
        ```
        """
        s = f"{self.canvas.stroke_style}"
        f = f"{self.canvas.fill_style}"
        self.canvas.fill_style = s
        self.canvas.begin_path()
        self.canvas.arc(x, y, self.canvas.line_width * 0.5, 0, self.TWO_PI, False)
        self.canvas.fill()
        self.canvas.fill_style = f

    def quad(
        self,
        x1: int | float,
        y1: int | float,
        x2: int | float,
        y2: int | float,
        x3: int | float,
        y3: int | float,
        x4: int | float,
        y4: int | float,
    ):
        """Draws a quadrilateral (four-sided shape).

        Quadrilaterals include rectangles, squares, rhombuses, and trapezoids.
        The first pair of parameters `(x1, y1)` sets the quad's first point.
        The next three pairs of parameters set the coordinates for its next
        three points `(x2, y2)`, `(x3, y3)`, and `(x4, y4)`. Points should be
        added in either clockwise or counter-clockwise order.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.quad(50, 62, 86, 50, 50, 38, 14, 50)
        ```
        """
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        self.vertex(x4, y4)
        self.end_shape()

    def rect(self, x: int | float, y: int | float, w: int | float, h: int | float):
        """Draws a rectangle.

        A rectangle is a four-sided shape defined by the `x`, `y`, `w`, and
        `h` parameters. `x` and `y` set the location of its top-left corner.
        `w` sets its width and `h` sets its height. Every angle in the
        rectangle measures 90˚.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.rect(30, 20, 55, 40)
        ```
        """
        self.canvas.fill_rect(x, y, w, h)
        self.canvas.stroke_rect(x, y, w, h)

    def square(self, x: int | float, y: int | float, s: int | float):
        """Draws a square.

        A square is a four-sided shape defined by the `x`, `y`, and `s`
        parameters. `x` and `y` set the location of its top-left corner. `s`
        sets its width and height. Every angle in the square measures 90˚
        and all its sides are the same length. 

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.square(30, 20, 55)
        ```
        """
        self.canvas.fill_rect(x, y, s, s)
        self.canvas.stroke_rect(x, y, s, s)

    def triangle(
        self,
        x1: int | float,
        y1: int | float,
        x2: int | float,
        y2: int | float,
        x3: int | float,
        y3: int | float,
    ):
        """Draws a triangle.

        A triangle is a three-sided shape defined by three points. The first
        two parameters specify the triangle's first point `(x1, y1)`. The
        middle two parameters specify its second point `(x2, y2)`. And the
        last two parameters specify its third point `(x3, y3)`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.triangle(30, 75, 58, 20, 86, 75)
        ```
        """
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        self.end_shape()

    # ========================================
    #               Attributes
    # ========================================

    def stroke_weight(self, weight: int | float):
        """Sets the width of the stroke used for points, lines, and the outlines of shapes.

        Note: stroke_weight() is affected by transformations, especially calls to scale().
        
        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Top.
        s.line(20, 20, 80, 20)

        # Middle.
        s.stroke_weight(4)
        s.line(20, 40, 80, 40)

        # Bottom.
        s.stroke_weight(10)
        s.line(20, 70, 80, 70)
        ```
        """
        if not self._is_stroke_weight_set:
            self._is_stroke_weight_set = True
        self.canvas.line_width = weight

    # ========================================
    #               Curves
    # ========================================

    def bezier(
        self,
        x1: int | float,
        y1: int | float,
        x2: int | float,
        y2: int | float,
        x3: int | float,
        y3: int | float,
        x4: int | float,
        y4: int | float,
    ):
        """Draws a Bézier curve.

        Bézier curves can form shapes and curves that slope gently. They're
        defined by two anchor points and two control points.

        The first two parameters, `x1` and `y1`, set the first anchor point.
        The first anchor point is where the curve starts.

        The next four parameters, `x2`, `y2`, `x3`, and `y3`, set the two
        control points. The control points "pull" the curve towards them.

        The seventh and eighth parameters, `x4` and `y4`, set the last anchor
        point. The last anchor point is where the curve ends.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Draw the anchor points in black.
        s.stroke(0)
        s.stroke_weight(5)
        s.point(85, 20)
        s.point(15, 80)

        # Draw the control points in red.
        s.stroke(255, 0, 0)
        s.point(10, 10)
        s.point(90, 90)

        # Draw a black bezier curve.
        s.no_fill()
        s.stroke(0)
        s.stroke_weight(1)
        s.bezier(85, 20, 10, 10, 90, 90, 15, 80)

        # Draw red lines from the anchor points to the control points.
        s.stroke(255, 0, 0)
        s.line(85, 20, 10, 10)
        s.line(15, 80, 90, 90)
        ```
        """
        self.canvas.begin_path()
        self.canvas.move_to(x1, y1)
        self.canvas.bezier_curve_to(x2, y2, x3, y3, x4, y4)
        self.canvas.stroke()

    def bezier_point(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        d: int | float,
        t: int | float,
    ) -> float:
        """Calculates coordinates along a Bézier curve using interpolation.

        `bezier_point()` calculates coordinates along a Bézier curve using the
        anchor and control points. It expects points in the same order as the
        bezier() method. `bezier_point()` works one axis at a time. Passing
        the anchor and control points' x-coordinates will calculate the
        x-coordinate of a point on the curve. Passing the anchor and control
        points' y-coordinates will calculate the y-coordinate of a point on
        the curve.

        The first parameter, `a`, is the coordinate of the first anchor point.

        The second and third parameters, `b` and `c`, are the coordinates of
        the control points.

        The fourth parameter, `d`, is the coordinate of the last anchor point.

        The fifth parameter, `t`, is the amount to interpolate along the
        curve. 0 is the first anchor point, 1 is the second anchor point, and
        0.5 is halfway between them.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Set the coordinates for the curve's anchor and control points.
        x1 = 85
        x2 = 10
        x3 = 90
        x4 = 15
        y1 = 20
        y2 = 10
        y3 = 90
        y4 = 80

        # Style the curve.
        s.no_fill()

        # Draw the curve.
        s.bezier(x1, y1, x2, y2, x3, y3, x4, y4)

        # Draw circles along the curve's path.
        s.fill(255)

        # Top-right.
        x = s.bezier_point(x1, x2, x3, x4, 0)
        y = s.bezier_point(y1, y2, y3, y4, 0)
        s.circle(x, y, 5)

        x = s.bezier_point(x1, x2, x3, x4, 0.5)
        y = s.bezier_point(y1, y2, y3, y4, 0.5)
        s.circle(x, y, 5) # center circle
        x = s.bezier_point(x1, x2, x3, x4, 1)
        y = s.bezier_point(y1, y2, y3, y4, 1)
        s.circle(x, y, 5) # bottom-left circle
        ```
        """
        adjusted_t = 1 - t
        return (
            pow(adjusted_t, 3) * a
            + 3 * pow(adjusted_t, 2) * t * b
            + 3 * adjusted_t * pow(t, 2) * c
            + pow(t, 3) * d
        )

    def bezier_tangent(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        d: int | float,
        t: int | float,
    ) -> float:
        """Calculates coordinates along a line that's tangent to a Bézier curve.

        Tangent lines skim the surface of a curve. A tangent line's slope
        equals the curve's slope at the point where it intersects.

        `bezier_tangent()` calculates coordinates along a tangent line using
        the Bézier curve's anchor and control points. It expects points in the
        same order as the `bezier()` method. `bezier_tangent()` works one axis
        at a time. Passing the anchor and control points' x-coordinates will
        calculate the x-coordinate of a point on the tangent line. Passing the
        anchor and control points' y-coordinates will calculate the
        y-coordinate of a point on the tangent line.

        The first parameter, `a`, is the coordinate of the first anchor point.

        The second and third parameters, `b` and `c`, are the coordinates of
        the control points.

        The fourth parameter, `d`, is the coordinate of the last anchor point.

        The fifth parameter, `t`, is the amount to interpolate along the curve.
        0 is the first anchor point, 1 is the second anchor point, and 0.5 is
        halfway between them.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Set the coordinates for the curve's anchor and control points.
        x1 = 85
        x2 = 10
        x3 = 90
        x4 = 15
        y1 = 20
        y2 = 10
        y3 = 90
        y4 = 80

        # Style the curve.
        s.no_fill()

        # Draw the curve.
        s.bezier(x1, y1, x2, y2, x3, y3, x4, y4)

        # Draw tangents along the curve's path.
        s.fill(255)

        # Top-right circle.
        s.stroke(0)
        x = s.bezier_point(x1, x2, x3, x4, 0)
        y = s.bezier_point(y1, y2, y3, y4, 0)
        s.circle(x, y, 5)

        # Top-right tangent line.
        # Scale the tangent point to draw a shorter line.
        s.stroke(255, 0, 0) 
        tx = 0.1 * s.bezier_tangent(x1, x2, x3, x4, 0)
        ty = 0.1 * s.bezier_tangent(y1, y2, y3, y4, 0)
        s.line(x + tx, y + ty, x - tx, y - ty)

        # Center circle.
        s.stroke(0)
        x = s.bezier_point(x1, x2, x3, x4, 0.5)
        y = s.bezier_point(y1, y2, y3, y4, 0.5)
        s.circle(x, y, 5)
        
        # Center tangent line.
        # Scale the tangent point to draw a shorter line.
        stroke(255, 0, 0)
        tx = 0.1 * s.bezier_tangent(x1, x2, x3, x4, 0.5)
        ty = 0.1 * s.bezier_tangent(y1, y2, y3, y4, 0.5)
        s.line(x + tx, y + ty, x - tx, y - ty)

        # Bottom-left circle.
        stroke(0)
        x = s.bezier_point(x1, x2, x3, x4, 1)
        y = s.bezier_point(y1, y2, y3, y4, 1)
        s.circle(x, y, 5)
        
        # Bottom-left tangent.
        # Scale the tangent point to draw a shorter line.
        s.stroke(255, 0, 0)
        tx = 0.1 * s.bezier_tangent(x1, x2, x3, x4, 1)
        ty = 0.1 * s.bezier_tangent(y1, y2, y3, y4, 1)
        s.line(x + tx, y + ty, x - tx, y - ty)
        ```
        """
        adjusted_t = 1 - t
        return (
            3 * d * pow(t, 2)
            - 3 * c * pow(t, 2)
            + 6 * c * adjusted_t * t
            - 6 * b * adjusted_t * t
            + 3 * b * pow(adjusted_t, 2)
            - 3 * a * pow(adjusted_t, 2)
        )

    # ========================================
    #                Vertex
    # ========================================

    def begin_shape(self):
        """Begins adding vertices to a custom shape.

        The `begin_shape()` and `end_shape()` methods allow for creating
        custom shapes. `begin_shape()` begins adding vertices to a custom
        shape and `end_shape()` stops adding them. After calling
        `begin_shape()`, shapes can be built by calling `vertex()`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.begin_shape() # begin drawing
        s.vertex(30, 20)
        s.vertex(85, 20)
        s.vertex(85, 75)
        s.vertex(30, 75)
        s.end_shape() # end drawing
        ```
        """
        self._vertices.clear()

    def end_shape(self):
        """Stops adding vertices to a custom shape.

        The `begin_shape()` and `end_shape()` methods allow for creating
        custom shapes. `begin_shape()` begins adding vertices to a custom
        shape and `end_shape()` stops adding them. After calling
        `begin_shape()`, shapes can be built by calling `vertex()`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.begin_shape() # begin drawing
        s.vertex(30, 20)
        s.vertex(85, 20)
        s.vertex(85, 75)
        s.vertex(30, 75)
        s.end_shape() # end drawing
        ```
        """
        if len(self._vertices) > 0:
            self.canvas.fill_polygon(self._vertices)
            self.canvas.stroke_polygon(self._vertices)
            self._vertices.clear()

    def vertex(self, x: int | float, y: int | float):
        """Adds a vertex to a custom shape.

        `vertex()` sets the coordinates of vertices drawn between the
        `begin_shape()` and `end_shape()` methods.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.begin_shape() # begin drawing
        s.vertex(30, 20)
        s.vertex(85, 20)
        s.vertex(85, 75)
        s.vertex(30, 75)
        s.end_shape() # end drawing
        ```
        """
        self._vertices.append((x, y))

    # ========================================
    #                Structure
    # ========================================

    def show(self):
        """Display the sketch beneath the current code cell.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.show()
        ```
        """
        display(self.canvas)

    # ========================================
    #               Transform
    # ========================================

    def apply_matrix(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        d: int | float,
        e: int | float,
        f: int | float,
    ):
        """Applies a transformation matrix to the coordinate system.

        Transformations such as `translate()`, `rotate()`, and `scale()` use
        matrix-vector multiplication behind the scenes. A table of numbers,
        called a matrix, encodes each transformation. The values in the matrix
        then multiply each point on the canvas, which is represented by a
        vector.

        `apply_matrix()` allows for many transformations to be applied at once.
        See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Matrix_math_for_the_web)
        for more details about transformations.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        
        # Translate the origin to the center.
        s.apply_matrix(1, 0, 0, 1, 50, 50)
        
        # Draw the circle at coordinates (0, 0).
        s.circle(0, 0, 40)
        ```
        """
        m = np.array(((a, c, e), (b, d, f), (0, 0, 1)), dtype=float)
        self._matrix = m @ self._matrix
        self.canvas.transform(a, b, c, d, e, f)

    def reset_matrix(self):
        """Clears all transformations applied to the coordinate system.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        
        # Translate the origin to the center.
        s.translate(50, 50)
        
        # Draw a blue circle at the coordinates (25, 25).
        s.fill("blue")
        s.circle(25, 25, 20)
        
        # Clear all transformations.
        # The origin is now at the top-left corner.
        s.reset_matrix()
        
        # Draw a red circle at the coordinates (25, 25).
        s.fill("red")
        s.circle(25, 25, 20)
        ```
        """
        self._matrix = np.eye(3)
        self.canvas.reset_transform()

    def rotate(self, angle: int | float):
        """Rotates the coordinate system.

        By default, the positive x-axis points to the right and the positive
        y-axis points downward. The `rotate()` method changes this orientation
        by rotating the coordinate system about the origin. Everything drawn
        after `rotate()` is called will appear to be rotated. Angles are
        measured in radians.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Rotate the coordinate system 1/8 turn.
        s.rotate(s.QUARTER_PI)

        # Draw a rectangle at coordinates (50, 0).
        s.rect(50, 0, 40, 20)
        ```
        """
        ca, sa = math.cos(angle), math.sin(angle)
        m = np.array(((ca, -sa, 0), (sa, ca, 0), (0, 0, 1)), dtype=float)
        self._matrix = m @ self._matrix
        self.canvas.rotate(angle)

    def scale(self, x: int | float, y: int | float = None):
        """Scales the coordinate system.

        By default, shapes are drawn at their original scale. A rectangle
        that's 50 pixels wide appears to take up half the width of a 100
        pixel-wide canvas. The `scale()` method can shrink or stretch the
        coordinate system so that shapes appear at different sizes.

        The first parameter, `s`, sets the amount to scale each axis. For
        example, calling `scale(2)` stretches the x- and y-axes by a factor
        of 2. The next parameter, `y`, is optional. It sets the amount to
        scale the y-axis. For example, calling `scale(2, 0.5)` stretches the
        x-axis by a factor of 2 and shrinks the y-axis by a factor of 0.5.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        
        # Draw a square at (30, 20).
        s.square(30, 20, 40)
        
        # Scale the coordinate system by a factor of 0.5.
        s.scale(0.5)
        
        # Draw a square at (30, 20).
        # It appears at (15, 10) after scaling.
        s.square(30, 20, 40)
        s.background(200)
        s.reset_matrix()
        
        # Draw a square at (30, 20).
        s.square(30, 20, 40)
        
        # Scale the coordinate system by factors of
        # 0.5 along the x-axis and
        # 1.3 along the y-axis.
        s.scale(0.5, 1.3)
        
        # Draw a square at (30, 20).
        # It appears as a rectangle at (15, 26) after scaling.
        s.square(30, 20, 40)
        ```
        """
        if y is None:
            m = np.array(((x, 0, 0), (0, x, 0), (0, 0, 1)), dtype=float)
            self._matrix = m @ self._matrix
            self.canvas.scale(x)
        else:
            m = np.array(((x, 0, 0), (0, y, 0), (0, 0, 1)), dtype=float)
            self._matrix = m @ self._matrix
            self.canvas.scale(x, y=y)

    def shear_x(self, angle: int | float):
        """Shears the x-axis so that shapes appear skewed.

        By default, the x- and y-axes are perpendicular. The `shear_x()`
        method transforms the coordinate system so that x-coordinates are
        translated while y-coordinates are fixed.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Shear the coordinate system along the x-axis.
        s.shear_x(s.QUARTER_PI)

        # Draw the square.
        s.square(0, 0, 50)
        ```
        """
        self.apply_matrix(1, 0, math.tan(angle), 1, 0, 0)

    def shear_y(self, angle: int | float):
        """Shears the y-axis so that shapes appear skewed.

        By default, the x- and y-axes are perpendicular. The `shear_y()`
        method transforms the coordinate system so that y-coordinates are
        translated while x-coordinates are fixed.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Shear the coordinate system along the y-axis.
        s.shear_y(s.QUARTER_PI)

        # Draw the square.
        s.square(0, 0, 50)
        ```
        """
        self.apply_matrix(1, math.tan(angle), 0, 1, 0, 0)

    def translate(self, x: int | float, y: int | float):
        """Translates the coordinate system.

        By default, the origin (0, 0) is at the sketch's top-left corner. The
        `translate()` method shifts the origin to a different position.
        Everything drawn after `translate()` is called will appear to be
        shifted.
    
        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Translate the origin to the center.
        s.translate(50, 50)

        # Draw a circle at coordinates (0, 0).
        s.circle(0, 0, 40)
        ```
        """
        m = np.array(((0, 0, x), (0, 0, y), (0, 0, 1)), dtype=float)
        self._matrix = m @ self._matrix
        self.canvas.translate(x, y)

    # ========================================
    #                  Image
    # ========================================

    def image(
        self,
        img: Self,
        x: int | float,
        y: int | float,
        width: int | float = None,
        height: int | float = None,
    ):
        """Draws an image to the canvas.

        The first parameter, `img`, is the source image to be drawn. `img` can be
        another `Sketch` instance.

        The second and third parameters, `x` and `y`, set the coordinates of the
        destination image's top left corner.

        The fourth and fifth parameters, `width` and `height`, are optional. They
        set the the width and height to draw the destination image. By
        default, `image()` draws the full source image at its original size.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        # Create the Sketches.
        s1 = Sketch()
        s2 = Sketch()

        # Draw to s1.
        s1.background(200)
        s1.circle(50, 50, 20)

        # Draw s1 on s2 at full size.
        s2.image(s1, 0, 0)

        # Draw s1 on s2 at half size.
        s2.image(s1, 0, 0, 50, 50)

        # Show s2.
        s2.show()
        ```
        """
        if width is None:
            width = img.width
        if height is None:
            height = img.height
        self.canvas.draw_image(img.canvas, x=x, y=y, width=width, height=height)

    # ========================================
    #                Typography
    # ========================================

    def text(self, text: str, x: int | float, y: int | float):
        """Draws text to the canvas.

        The first parameter, `text`, is the text to be drawn. The second and
        third parameters, `x` and `y`, set the coordinates of the text's
        bottom-left corner. See `text_align()` for other ways to align text.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()
        ```

        ```python
        # Plain text.
        s.background(200)
        s.text("hi", 50, 50)
        ```
        
        
        ```python
        # Emoji.
        s.background("skyblue")
        s.text_size(100)
        s.text("🌈", 0, 100)
        ```
        
        ```python
        # No fill.
        s.background(200)
        s.text_size(32)
        s.fill(255)
        s.stroke(0)
        s.stroke_weight(4)
        s.text("hi", 50, 50)
        ```
        
        ```python
        # Multicolor text.
        s.background("black")
        s.text_size(22)
        s.fill("yellow")
        s.text("rainbows", 6, 20)
        s.fill("cornflowerblue")
        s.text("rainbows", 6, 45)
        s.fill("tomato")
        s.text("rainbows", 6, 70)
        s.fill("limegreen")
        s.text("rainbows", 6, 95)
        ```
        """
        if self._is_fill_set:
            self.canvas.fill_text(text, x, y)
        else:
            self.canvas.fill_style = Sketch._DEFAULT_TEXT_FILL
            self.canvas.fill_text(text, x, y)
            self.canvas.fill_style = Sketch._DEFAULT_FILL

        if self._is_stroke_set:
            if self._is_stroke_weight_set:
                self.canvas.stroke_text(text, x, y)
            else:
                self.canvas.line_width = Sketch._DEFAULT_TEXT_WEIGHT
                self.canvas.stroke_text(text, x, y)
                self.canvas.line_width = Sketch._DEFAULT_STROKE_WEIGHT

    def text_font(self, font: str):
        """Sets the font used by the `text()` method.

        The font should be a string with the name of a system font such as
        `"Courier New"`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)
        s.text_font("Courier New")
        s.text_size(24)
        s.text("hi", 35, 55)
        ```
        """
        self._font = font
        self.canvas.font = (
            f"{self._font_style} {self._font_weight} {self._font_size}px {self._font}"
        )

    def text_size(self, size: int | float):
        """Sets the font size when `text()` is called.

        Note: Font size is measured in pixels.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Top row.
        s.text_size(12)
        s.text("Font Size 12", 10, 30)

        # Middle row.
        s.text_size(14)
        s.text("Font Size 14", 10, 60)

        # Bottom row.
        s.text_size(16)
        s.text("Font Size 16", 10, 90)
        ```
        """
        self._font_size = size
        self.canvas.font = (
            f"{self._font_style} {self._font_weight} {self._font_size}px {self._font}"
        )

    def text_align(self, horizontal: str, vertical: str = None):
        """Sets the way text is aligned when `text()` is called.

        By default, calling `text("hi", 10, 20)` places the bottom-left corner
        of the text's bounding box at (10, 20).

        The first parameter, `horizontal`, changes the way `text()` interprets
        x-coordinates. By default, the x-coordinate sets the left edge of the
        bounding box. `text_align()` accepts the following values for horizontal:
        `LEFT`, `CENTER`, or `RIGHT`.

        The second parameter, `vertical`, is optional. It changes the way `text()`
        interprets y-coordinates. By default, the y-coordinate sets the bottom
        edge of the bounding box. `text_align()` accepts the following values
        for vertical: `TOP`, `BOTTOM`, `CENTER`, or `BASELINE`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # Draw a vertical line.
        s.stroke_weight(0.5)
        s.line(50, 0, 50, 100)

        # Top row.
        s.text_size(16)
        s.text_align(s.RIGHT)
        s.text("ABCD", 50, 30)
        
        # Middle row.
        s.text_align(s.CENTER)
        s.text("EFGH", 50, 50)
        
        # Bottom row.
        s.text_align(s.LEFT)
        s.text("IJKL", 50, 70)
        ```
        """
        if horizontal == Sketch.LEFT:
            self._text_align = Sketch.LEFT
        elif horizontal == Sketch.RIGHT:
            self._text_align = Sketch.RIGHT
        elif horizontal == Sketch.CENTER:
            self._text_align = Sketch.CENTER
        self.canvas.text_align = self._text_align

        if vertical is None:
            return
        if vertical == Sketch.TOP:
            self._text_baseline = Sketch.TOP
        elif vertical == Sketch.BOTTOM:
            self._text_baseline = Sketch.BOTTOM
        elif vertical == Sketch.CENTER:
            self._text_baseline = Sketch.CENTER
        elif vertical == Sketch.BASELINE:
            self._text_baseline = Sketch.BASELINE
        self.canvas.text_baseline = vertical

    def text_style(self, style: str):
        """Sets the style for system fonts when `text()` is called.

        The parameter, `style`, can be either `NORMAL`, `ITALIC`, `BOLD`, or
        `BOLDITALIC`.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        s.background(200)

        # First row.
        s.text_size(12)
        s.text_style(s.NORMAL)
        s.text("Normal", 20, 15)

        # Second row.
        s.text_style(s.ITALIC)
        s.text("Italic", 20, 40)

        # Third row.
        s.text_style(s.BOLD)
        s.text("Bold", 20, 65)

        # Fourth row.
        s.text_style(s.BOLDITALIC)
        s.text("Bold Italic", 20, 90)
        ```
        """
        if style == Sketch.NORMAL:
            self._font_weight = Sketch.NORMAL
            self._font_style = Sketch.NORMAL
        elif style == Sketch.ITALIC:
            self._font_weight = Sketch.NORMAL
            self._font_style = Sketch.ITALIC
        elif style == Sketch.BOLD:
            self._font_weight = Sketch.BOLD
            self._font_style = Sketch.NORMAL
        elif style == Sketch.BOLDITALIC:
            self._font_weight = Sketch.BOLD
            self._font_style = Sketch.ITALIC
        self.canvas.font = (
            f"{self._font_style} {self._font_weight} {self._font_size}px {self._font}"
        )

    # ========================================
    #                Utilities
    # ========================================

    def _unpack_transform(self) -> tuple[float]:
        """Unpacks the sketch's transformation matrix."""
        a = self._matrix[0][0]
        b = self._matrix[1][0]
        c = self._matrix[0][1]
        d = self._matrix[1][1]
        e = self._matrix[2][0]
        f = self._matrix[2][2]
        return a, b, c, d, e, f

    def run_sketch(self, draw: Callable, seconds: int | float, delay: float = 20):
        """Draws frames in an animation by calling a function repeatedly.

        `run_sketch()` repeatedly calls a function that contains drawing
        commands. The rate at which each frame is drawn depends on many
        factors. `run_sketch()` doesn't attempt to maintain a constant
        framerate.

        The first parameter, `draw`, is a function containing the commands for
        drawing each frame.

        The second parameter, `seconds`, sets the number of seconds the
        animation should run.

        The third parameter, `delay`, is optional. It sets the number of
        milliseconds the sketch should pause after drawing the current frame.
        The default value is 20. If `draw` contains many drawing commands,
        each frame may take much longer than `delay` milliseconds to render.

        **Example**
        ```python
        from ipycc.sketch import Sketch

        s = Sketch()
        s.show()

        def draw():
            # Paint the background.
            s.background(200)

            # Calculate the circle's x-coordinate.
            x = s.frame_count

            # Draw the circle.
            s.circle(x, 50, 20)

        # Run the animation for 5 seconds.
        s.run_sketch(draw, 5)
        ```
        """
        if delay < 0:
            raise SketchError("Your delay value must be positive.")
        start = time.time()
        end = start + seconds
        delay *= 0.001
        self.frame_count = 0
        while time.time() < end:
            with hold_canvas():
                a, b, c, d, e, f = self._unpack_transform()
                draw()
                self.reset_matrix()
                self.apply_matrix(a, b, c, d, e, f)
                self.frame_count += 1
                time.sleep(delay)


__all__ = ["Sketch"]
