from ipycc.turtle import Turtle


def test_constructor():
    t = Turtle()
    assert t.pencolor() == "black"
