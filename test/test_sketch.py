from ipycc.sketch import Sketch


def test_constructor():
    s = Sketch()
    assert s.width == 100 and s.height == 100
