from ipycc.sketch import Sketch


def test_constructor():
    s = Sketch(200, 200)
    assert s.width == 200 and s.height == 200
