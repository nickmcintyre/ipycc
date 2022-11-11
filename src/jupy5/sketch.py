import asyncio
from contextlib import contextmanager
import math
import time
from IPython.display import display, clear_output
from ipycanvas import Canvas, hold_canvas


class Sketch:

    # Constants
    DELAY = 0.02
    HALF_PI = math.pi * 0.5
    PI = math.pi
    QUARTER_PI = math.pi * 0.25
    TAU = math.tau
    TWO_PI = math.tau
    DEGREES = 'degrees'
    RADIANS = 'radians'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = Canvas(width=width, height=height)
        self.canvas.fill_style = 'white'
        self.canvas.stroke_style = 'black'
        self.canvas.line_width = 1
        self._is_looping = False
        self.frame_count = 0
        self._start_time = 0
        self._vertices = []

    # ========================================
    #                Setting
    # ========================================

    def background(self, color):
        old_fill = self.canvas.fill_style
        old_stroke = self.canvas.stroke_style
        old_weight = self.canvas.line_width
        self.fill(color)
        self.stroke(color)
        self.stroke_weight(1)
        self.canvas.fill_rect(0, 0, self.width, self.height)
        self.canvas.stroke_rect(0, 0, self.width, self.height)
        self.fill(old_fill)
        self.stroke(old_stroke)
        self.stroke_weight(old_weight)

    def clear(self):
        self.canvas.clear()

    def fill(self, color):
        self.canvas.fill_style = color

    def no_fill(self):
        self.canvas.fill_style = '#00000000'

    def no_stroke(self):
        self.canvas.stroke_style = '#00000000'

    def stroke(self, color):
        self.canvas.stroke_style = color

    def _display(self):
        display(self.canvas)

    def remove(self):
        self.clear()
        clear_output()

    # ========================================
    #              2D Primitives
    # ========================================

    def _acute_arc_to_bezier(self, start, size):
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
            'ax': round(math.cos(start), 7),
            'ay': round(math.sin(start), 7),
            'bx': round((lam * cos_phi + mu * sin_phi), 7),
            'by': round((lam * sin_phi - mu * cos_phi), 7),
            'cx': round((lam * cos_phi - mu * sin_phi), 7),
            'cy': round((lam * sin_phi + mu * cos_phi), 7),
            'dx': round(math.cos(start + size), 7),
            'dy': round(math.sin(start + size), 7),
        }

    def arc(self, x, y, w, h, start, stop):
        rx = w * 0.5
        ry = h * 0.5
        epsilon = 0.00001  # Smallest visible angle on displays up to 4K.
        arc_to_draw = 0
        curves = []
        # x += rx
        # y += ry

        # Create curves
        while stop - start >= epsilon:
            arc_to_draw = min(stop - start, Sketch.HALF_PI)
            curves.append(self._acute_arc_to_bezier(start, arc_to_draw))
            start += arc_to_draw

        self.canvas.begin_path()
        for index, curve in enumerate(curves):
            if index == 0:
                self.canvas.move_to(x + curve['ax'] * rx, y + curve['ay'] * ry)
            self.canvas.bezier_curve_to(x + curve['bx'] * rx, y + curve['by'] * ry,
                                        x + curve['cx'] * rx, y +
                                        curve['cy'] * ry,
                                        x + curve['dx'] * rx, y + curve['dy'] * ry)
        # if mode == constants['PIE'] or mode == None:
        self.canvas.line_to(x, y)
        self.canvas.close_path()
        self.canvas.fill()
        self.canvas.stroke()

    def ellipse(self, x, y, w, h):
        # ellipse_mode == 'center'
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

    def circle(self, x, y, d):
        r = d * 0.5
        self.canvas.fill_circle(x, y, r)
        self.canvas.stroke_circle(x, y, r)

    def line(self, x1, y1, x2, y2):
        self.canvas.stroke_line(x1, y1, x2, y2)

    def point(self, x, y):
        self.canvas.fill_circle(x, y, 0.001)

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        self.vertex(x4, y4)
        self.end_shape()

    def rect(self, x, y, w, h):
        self.canvas.fill_rect(x, y, w, h)
        self.canvas.stroke_rect(x, y, w, h)

    def square(self, x, y, s):
        self.rect(x, y, s, s)

    def triangle(self, x1, y1, x2, y2, x3, y3):
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        self.end_shape()

    # ========================================
    #               Attributes
    # ========================================

    def stroke_weight(self, weight):
        self.canvas.line_width = weight

    # ========================================
    #                Vertex
    # ========================================

    def begin_shape(self):
        self._vertices.clear()

    def end_shape(self):
        if len(self._vertices) > 0:
            self.canvas.fill_polygon(self._vertices)
            self.canvas.stroke_polygon(self._vertices)

    def vertex(self, x, y):
        self._vertices.append((x, y))

    # ========================================
    #                Structure
    # ========================================

    async def delay(self, secs):
        await asyncio.sleep(secs)

    async def loop(self, draw, *args):
        if self.frame_count == 0 and not self._is_looping:
            self._is_looping = True
            self._start_time = time.time()
        if len(args) > 0 and type(args[0]) == int:
            while self._is_looping:
                self.frame_count += 1
                now = time.time()
                if now - self._start_time > args[0]:
                    break
                with hold_canvas():
                    draw()
                    self._vertices.clear()
                await asyncio.sleep(Sketch.DELAY)
        else:
            while self._is_looping:
                self.frame_count += 1
                with hold_canvas():
                    draw()
                    self._vertices.clear()
                await asyncio.sleep(Sketch.DELAY)

    def no_loop(self):
        self._is_looping = False


@contextmanager
def sketch(width, height):
    p5 = Sketch(width, height)
    p5._display()
    yield p5
    p5.remove()
