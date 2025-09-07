from ipycc.turtle import Turtle


def test_constructor():
    t = Turtle()
    assert t.width == 400 and t.height == 400
