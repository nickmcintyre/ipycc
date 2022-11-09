import asyncio
from contextlib import contextmanager
import time
from IPython.display import display, clear_output
from ipycanvas import Canvas, hold_canvas


_DELAY = 0.02


class Sketch:
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

    def display(self):
        display(self.canvas)

    def clear(self):
        self.canvas.clear()

    def remove(self):
        clear_output()

    def stop(self):
        self._is_looping = False
        self.clear()
        self.remove()

    def fill(self, color):
        self.canvas.fill_style = color

    def stroke(self, color):
        self.canvas.stroke_style = color

    def stroke_weight(self, weight):
        self.canvas.line_width = weight

    def no_stroke(self):
        self.canvas.stroke_style = '#00000000'

    def no_fill(self):
        self.canvas.fill_style = '#00000000'

    def rect(self, x, y, w, h):
        self.canvas.fill_rect(x, y, w, h)
        self.canvas.stroke_rect(x, y, w, h)

    def square(self, x, y, s):
        self.rect(x, y, s, s)

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

    def circle(self, x, y, d):
        self.canvas.fill_circle(x, y, d)
        self.canvas.stroke_circle(x, y, d)

    def ellipse(self, x, y, w, h):
        # ellipse_mode == 'center'
        dx = w / 2
        dy = h / 2
        cx = x - dx
        cy = y - dy

        kappa = 0.5522847498
        # control point offset horizontal
        ox = w / 2 * kappa
        # control point offset vertical
        oy = h / 2 * kappa
        # x-end
        xe = cx + w
        # y-end
        ye = cy + h
        # x-middle
        xm = cx + w / 2
        # y-middle
        ym = cy + h / 2
        self.canvas.begin_path()
        self.canvas.move_to(cx, ym)
        self.canvas.bezier_curve_to(cx, ym - oy, xm - ox, cy, xm, cy)
        self.canvas.bezier_curve_to(xm + ox, cy, xe, ym - oy, xe, ym)
        self.canvas.bezier_curve_to(xe, ym + oy, xm + ox, ye, xm, ye)
        self.canvas.bezier_curve_to(xm - ox, ye, cx, ym + oy, cx, ym)
        self.canvas.fill()
        self.canvas.stroke()

    def line(self, x1, y1, x2, y2):
        self.canvas.stroke_line(x1, y1, x2, y2)

    def point(self, x, y):
        self.circle(x, y, 0.1)

    async def loop(self, draw, *args):
        if self.frame_count == 0 and not self._is_looping:
            self._is_looping = True
            self._start_time = time.time()
        if len(args) > 0 and type(args[0]) == int:
            self.frame_count += 1
            while self._is_looping:
                now = time.time()
                if now - self._start_time > args[0]:
                    break
                with hold_canvas():
                    draw()
                await asyncio.sleep(_DELAY)
        else:
            self.frame_count += 1
            while self._is_looping:
                with hold_canvas():
                    draw()
                await asyncio.sleep(_DELAY)

    async def pause(self, secs):
        await asyncio.sleep(secs)


@contextmanager
def sketch(width, height):
    p5 = Sketch(width, height)
    p5.display()
    yield p5
    p5.clear()
    p5.remove()
