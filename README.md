# jupy5
> A library for creative coding in Python using Jupyter

This library makes it easy to explore creative coding in Python using Jupyter notebooks. Its design is heavily inspired by [p5.js](https://github.com/processing/p5.js) and [Turtle graphics](https://docs.python.org/3/library/turtle.html) from the Python standard library.

## Turtles
A light blue square with a smaller square outlined in green at its center. The square is drawn one side at a time.
```python
from jupy5 import turtle


with turtle(400, 400) as t:
    t.background('dodgerblue')
    t.pencolor('limegreen')
    t.pensize(4)
    t.pendown()
    for side in range(4):
        t.forward(100)
        t.left(90)
        await t.pause(1)
```

## Sketches
A light blue square with a circle in its center. The circle is drawn with a white center and black edge.
```python
from jupy5 import sketch


with sketch(400, 400) as p5:
    p5.background('dodgerblue')
    p5.circle(200, 200, 50)
    await p5.pause(2)
```

A dark blue square with ten circles in its center. The circles are drawn in white and move in synchrony.
```python
import math
from random import uniform
from jupy5 import sketch


with sketch(400, 400) as p5:
    coupling = 1
    num_bugs = 10
    k_n = coupling / num_bugs
    
    class Bug:
        def __init__(self):
            self.x = p5.width * 0.5
            self.y = p5.height * 0.5
            self.r = 5
            self.angle = uniform(0, math.tau)
            self.freq = uniform(5, 10)
            self.dadt = 0
            self.dt = 0.01
        
        def render(self):
            p5.fill('ghostwhite')
            p5.no_stroke()
            p5.circle(self.x, self.y, 2 * self.r)
        
        def update(self):
            dx = math.cos(self.angle)
            dy = math.sin(self.angle)
            self.x += dx
            self.y += dy
            self.angle += self.dadt * self.dt
        
        def sync(self, bugs):
            self.dadt = self.freq
            for bug in bugs:
                self.dadt += k_n * math.sin(bug.angle - self.angle)
    
    bugs = [Bug() for _ in range(num_bugs)]
    
    def draw():
        p5.background('#1919706F')
        for bug in bugs:
            bug.sync(bugs)
        
        for bug in bugs:
            bug.update()
            bug.render()
    
    await p5.loop(draw, 10)
```

jupy5 provides a simplified interface to the HTML canvas by wrapping [ipycanvas](https://ipycanvas.readthedocs.io/en/latest/index.html) in a beginner-friendly API.

## Roadmap
- 2D Primitives
- Turtles
