from ipycc import Sketch


def test_constructor():
    p5 = Sketch(200, 200)
    assert p5.width == 200 and p5.height == 200
