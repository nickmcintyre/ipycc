# [ipycc](https://ipy.cc)
> A Python package for creative coding in Jupyter

ipycc is a friendly tool for learning to code, making art, and exploring mathematics within [Jupyter](https://jupyter.org/) notebooks. Try it out at [https://code.ipy.cc](https://code.ipy.cc)!

ipycc's `Sketch` class provides a beginner-friendly API for drawing that is heavily inspired by [p5.js](https://p5js.org). `Sketch` lovingly borrows from p5.js' source code and documentation, and mimics [py5](https://py5coding.org/) where possible. Under the hood, it uses the powerful [ipycanvas](https://ipycanvas.readthedocs.io/en/latest/index.html) package for drawing.

The package also includes a (mostly) drop-in replacement for [Turtle graphics](https://docs.python.org/3/library/turtle.html) from the Python standard library. The `Turtle` class is based on the standard library's implementation and uses the `Sketch` class for rendering. ipycc bundles the standard library's `Vec2D` class for vector arithmetic along with a few helper functions.

ipycc runs smoothly in [JupyterLite](https://jupyterlite.readthedocs.io/en/stable/howto/index.html), creating a nice way to start coding in the web browser without installing any software.

## A tour of ipycc

Here are a few quick examples of ipycc in action.

### Sketches

A light gray square with a circle in its center. The circle is drawn with a white center and a black edge.
```python
from ipycc.sketch import Sketch

# Create a sketch and show it.
s = Sketch()
s.show()

# Paint the background.
s.background(200)

# Draw a circle.
s.circle(50, 50, 20)
```

A purple square with a circle in its center. The circle is drawn with a pink center and a thick white edge.
```python
from ipycc.sketch import Sketch

# Create a sketch and show it.
s = Sketch(400, 400)
s.show()

# Paint the background.
s.background("darkorchid")

# Style the circle.
s.stroke_weight(5)
s.stroke("ghostwhite")
s.fill("fuchsia")

# Draw the circle.
s.circle(200, 200, 100)
```

A purple square with a circle in its center. The circle is drawn with a pink center and a thick white edge. It moves slowly to the right.
```python
from ipycc.sketch import Sketch

# Create a sketch and show it.
s = Sketch(400, 400)
s.show()

# Define a function to draw frames in an animation.
def draw():
    # Paint the background.
    s.background("darkorchid")

    # Calculate the circle's x-coordinate.
    x = s.frame_count * 3

    # Style the circle.
    s.stroke_weight(5)
    s.stroke(248, 248, 255)
    s.fill("#FF00FF")

    # Draw the circle.
    s.circle(x, 200, 100)

# Run the animation for 5 seconds.
s.run_sketch(draw, 5)
```

### Turtles

A white square with a short black line extending from the center to the right. A black arrow tip at the end of the line points up.
```python
from ipycc.turtle import Turtle

# Create a turtle and show it.
t = Turtle()
t.show()

# Draw a line.
t.forward(50)
# Turn left.
t.left(90)
```

A white square with the outline of a smaller black square. The smaller square is drawn one side at a time.
```python
from ipycc.turtle import Turtle

# Create a turtle and show it.
t = Turtle()
t.show()

# Draw a square.
for i in range(4):
    t.forward(50)
    t.left(90)
```

A black square with a sprial pattern drawn in green. The spiral is drawn one side at a time.
```python
from ipycc.turtle import Turtle

# Create a turtle and show it.
t = Turtle()
t.show()

# Style the turtle.
t.bgcolor("black")
t.color(0, 1, 0)

# Draw a spiral.
for i in range(40):
    length = i * 5
    t.forward(length)
    t.left(90)
```

## Installation

If you'd like to install ipycc locally on your computer, start by [downloading Python](https://www.python.org/downloads/). You can then create a virtual environment, install ipycc, and launch JupyterLab from your system shell like so:

On Linux/macOS:
```sh
mkdir ipycc
cd ipycc
python3 -m venv venv
source venv/bin/activate
pip install jupyterlab ipycc
jupyter lab
```

On Windows:
```powershell
mkdir ipycc
cd ipycc
py -m venv venv
venv\Scripts\activate
pip install jupyterlab ipycc
jupyter lab
```

The [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/installing-packages/) has additional information to help you get up and running.

### 💡 Local alternatives

If you're running ipycc locally, you may also be interested in [py5](https://py5coding.org/) which uses [Processing](https://processing) for drawing. py5 has advanced features that you may wish to explore at some point.

The standard library's version of Turtle graphics doesn't run in the web browser, but you can run it locally from Jupyter using the following [magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-gui):

```python
from turtle import Turtle

%gui tk

t = Turtle()
t.forward(50) # opens in a separate window
```

## License

ipycc is licensed under the [GNU Lesser General Public License v3.0](https://choosealicense.com/licenses/lgpl-3.0/).

## Contributing

Found a bug or typo? Want a new feature? Feel free to open an issue in the project's [GitHub repository](https://github.com/nickmcintyre/ipycc)!
