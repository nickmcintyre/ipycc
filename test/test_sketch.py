import pytest
from ipycc.sketch import Sketch


@pytest.fixture(scope="class")
def sketch():
    return Sketch()


class Test2DPrimitives:

    def test_constructor(self, sketch):
        assert sketch.width == 100 and sketch.height == 100
    
    def test_arc(self, sketch):
        assert callable(sketch.arc)
    
    def test_ellipse(self, sketch):
        assert callable(sketch.ellipse)
    
    def test_line(self, sketch):
        assert callable(sketch.line)
    
    def test_point(self, sketch):
        assert callable(sketch.point)

    def test_quad(self, sketch):
        assert callable(sketch.quad)
    
    def test_rect(self, sketch):
        assert callable(sketch.rect)

    def test_triangle(self, sketch):
        assert callable(sketch.triangle)
    
    def test_square(self, sketch):
        assert callable(sketch.square)


class TestAttributes:

    def test_background(self, sketch):
        assert callable(sketch.background)
    
    def test_clear(self, sketch):
        assert callable(sketch.clear)

    def test_fill(self, sketch):
        assert callable(sketch.fill)
    
    def test_no_fill(self, sketch):
        assert callable(sketch.no_fill)
    
    def test_no_stroke(self, sketch):
        assert callable(sketch.no_stroke)
    
    def test_reset(self, sketch):
        assert callable(sketch.reset)
    
    def test_stroke(self, sketch):
        assert callable(sketch.stroke)
    
    def test_stroke_weight(self, sketch):
        assert callable(sketch.stroke_weight)


class TestCurves:

    def test_bezier(self, sketch):
        assert callable(sketch.bezier)
    
    def test_bezier_point(self, sketch):
        assert callable(sketch.bezier_point)
        result = sketch.bezier_point(85, 10, 90, 15, 0.5)
        assert result == 50
        assert result != -1
    
    def test_bezier_tangent(self, sketch):
        assert callable(sketch.bezier_tangent)
        result = sketch.bezier_tangent(95, 73, 73, 15, 0.5)
        assert result == -60

    
class TestEnvironment:

    def test_width(self, sketch):
        assert sketch.width == 100
        s = Sketch(200, 200)
        assert s.width == 200
    
    def test_height(self, sketch):
        assert sketch.height == 100
        s = Sketch(200, 200)
        assert s.height == 200
    
    def test_pixel_density(self, sketch):
        assert sketch.pixel_density == 2
        s = Sketch(200, 200, 1)
        assert s.pixel_density == 1

    def test_frame_count(self, sketch):
        assert sketch.frame_count == 0
        def draw():
            pass
        sketch.run_sketch(draw, 0.001)
        assert sketch.frame_count > 0


class TestImage:

    def test_image(self, sketch):
        assert callable(sketch.image)


class TestStructure:

    def test_show(self, sketch):
        assert callable(sketch.show)


class TestTransform:

    def test_apply_matrix(self, sketch):
        assert callable(sketch.apply_matrix)
    
    def test_reset_matrix(self, sketch):
        assert callable(sketch.reset_matrix)
    
    def test_rotate(self, sketch):
        assert callable(sketch.rotate)
    
    def test_scale(self, sketch):
        assert callable(sketch.scale)
    
    def test_shear_x(self, sketch):
        assert callable(sketch.shear_x)
    
    def test_shear_y(self, sketch):
        assert callable(sketch.shear_y)
    
    def test_translate(self, sketch):
        assert callable(sketch.translate)


class TestTypography:

    def test_text(self, sketch):
        assert callable(sketch.text)
    
    def test_text_font(self, sketch):
        assert callable(sketch.text_font)
    
    def test_text_align(self, sketch):
        assert callable(sketch.text_align)
    
    def test_text_size(self, sketch):
        assert callable(sketch.text_size)
    
    def test_text_style(self, sketch):
        assert callable(sketch.text_style)


class TestUtilities:

    def test_run_sketch(self, sketch):
        assert callable(sketch.run_sketch)


class TestVertex:

    def test_begin_shape(self, sketch):
        assert callable(sketch.begin_shape)
    
    def test_end_shape(self, sketch):
        assert callable(sketch.end_shape)
    
    def test_vertex(self, sketch):
        assert callable(sketch.vertex)
