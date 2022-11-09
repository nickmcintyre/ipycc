# jupy5
> A library for creative coding in Python using Jupyter

This library makes it easy to explore creative coding in Python using Jupyter notebooks. Its design is heavily inspired by [p5.js](https://github.com/processing/p5.js).

```python
from jupy5 import sketch

with sketch(400, 400) as p5:
  p5.background('dodgerblue')
  p5.circle(200, 200, 50)
  await p5.pause(2)
```

jupy5 provides a simplified interface to the HTML canvas by wrapping [ipycanvas](https://ipycanvas.readthedocs.io/en/latest/index.html) in a beginner-friendly API.

## Roadmap
- 2D Primitives
- Turtles
