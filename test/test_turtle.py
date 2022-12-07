from ipycc import Turtle


def test_constructor():
    t = Turtle()
    assert t.width == 200 and t.height == 200
