import pytest
import pickle
import math
from pyclothoids import Clothoid, SolveG2

# --- Helper Functions ---


def angle_difference(theta1, theta2):
    return (theta2 - theta1 + math.pi) % (2 * math.pi) - math.pi


# --- Test Clothoid Creation ---


@pytest.mark.parametrize(
    "x0, y0, t0, k0, kd, sf",
    [
        (0, 0, 0, 0, 0, 1),  # Straight line
        (1, 2, math.pi / 4, 0, 0, 2),  # Diagonal line
        (0, 0, 0, 0.1, 0.01, 5),  # Curved clothoid
        (-1, -1, math.pi / 2, -0.1, 0.02, 3),  # Negative curvature
    ],
)
def test_standard_params(x0, y0, t0, k0, kd, sf):
    clothoid = Clothoid.StandardParams(x0, y0, t0, k0, kd, sf)
    assert clothoid.XStart == pytest.approx(x0)
    assert clothoid.YStart == pytest.approx(y0)
    assert angle_difference(clothoid.ThetaStart, t0) == pytest.approx(0.0)
    assert clothoid.KappaStart == pytest.approx(k0)
    assert clothoid.dk == pytest.approx(kd)
    assert clothoid.length == pytest.approx(sf)
    assert clothoid.Parameters == (x0, y0, t0, k0, kd, sf)


@pytest.mark.parametrize(
    "x0, y0, t0, x1, y1, t1",
    [
        (0, 0, math.pi / 4, 1, 1, math.pi / 4),  # Diagonal line
        (1, 2, math.pi / 4, 0, 0, 0),
        (0, 0, 0, 0.1, 0.01, 5),
        (-1, -1, math.pi / 2, -0.1, 0.02, 1),
    ],
)
def test_g1_hermite(x0, y0, t0, x1, y1, t1):
    clothoid = Clothoid.G1Hermite(x0, y0, t0, x1, y1, t1)
    assert clothoid.XStart == pytest.approx(x0)
    assert clothoid.YStart == pytest.approx(y0)
    assert angle_difference(clothoid.ThetaStart, t0) == pytest.approx(0.0)
    assert clothoid.XEnd == pytest.approx(x1)
    assert clothoid.YEnd == pytest.approx(y1)
    assert clothoid.ThetaEnd == pytest.approx(
        ((t1 + math.pi) % (math.pi * 2)) - math.pi
    )


# --- Test Pickling ---


@pytest.mark.parametrize(
    "x0, y0, t0, k0, kd, sf",
    [
        (0, 0, 0, 0, 0, 1),
        (1, 2, math.pi / 4, 0, 0, 2),
        (0, 0, 0, 0.1, 0.01, 5),
    ],
)
def test_pickling(x0, y0, t0, k0, kd, sf):
    clothoid = Clothoid.StandardParams(x0, y0, t0, k0, kd, sf)
    pickled_clothoid = pickle.dumps(clothoid)
    unpickled_clothoid = pickle.loads(pickled_clothoid)
    assert unpickled_clothoid.Parameters == clothoid.Parameters


# --- Test Transformations ---


@pytest.mark.parametrize(
    "xoff, yoff",
    [
        (0, 0),
        (1, 1),
        (-1, -1),
        (100, -50),
    ],
)
def test_translation(xoff, yoff):
    clothoid = Clothoid.StandardParams(1.0, 2.0, 0.0, 0.0, 0.0, 1.0)
    translated = clothoid.Translate(xoff, yoff)
    assert translated.XStart == pytest.approx(1.0 + xoff)
    assert translated.YStart == pytest.approx(2.0 + yoff)
    assert translated.ThetaStart == pytest.approx(0.0)
    assert translated.KappaStart == pytest.approx(0.0)
    assert translated.dk == pytest.approx(0.0)
    assert translated.length == pytest.approx(1.0)


@pytest.mark.parametrize(
    "angle, expected_x, expected_y",
    [
        (0, 1.0, 2.0),
        (math.pi / 2, -2.0, 1.0),
        (-math.pi / 2, 2.0, -1.0),
        (math.pi, -1.0, -2.0),
    ],
)
def test_rotation(angle, expected_x, expected_y):
    clothoid = Clothoid.StandardParams(1.0, 2.0, 0.0, 0.0, 0.0, 1.0)
    rotated = clothoid.Rotate(angle, center=(0, 0))
    assert rotated.XStart == pytest.approx(expected_x)
    assert rotated.YStart == pytest.approx(expected_y)
    assert angle_difference(rotated.ThetaStart, angle) == pytest.approx(0.0)
    assert rotated.KappaStart == pytest.approx(0.0)
    assert rotated.dk == pytest.approx(0.0)
    assert rotated.length == pytest.approx(1.0)


@pytest.mark.parametrize(
    "axis, expected_x, expected_y, expected_theta",
    [
        ("x", 1.0, -2.0, -math.pi / 4),
        ("y", -1.0, 2.0, math.pi - math.pi / 4),
        ("start", 1.0, 2.0, math.pi / 4),
    ],
)
def test_flip(axis, expected_x, expected_y, expected_theta):
    clothoid = Clothoid.StandardParams(1.0, 2.0, math.pi / 4, 0.0, 0.0, 1.0)
    flipped = clothoid.Flip(axis)
    assert flipped.XStart == pytest.approx(expected_x)
    assert flipped.YStart == pytest.approx(expected_y)
    assert angle_difference(flipped.ThetaStart, expected_theta) == pytest.approx(0.0)
    assert flipped.KappaStart == pytest.approx(-clothoid.KappaStart)
    assert flipped.dk == pytest.approx(-clothoid.dk)
    assert flipped.length == pytest.approx(clothoid.length)


@pytest.mark.parametrize("sfactor", [0.5, 2.0, -1.0])
def test_scaling(sfactor):
    clothoid = Clothoid.StandardParams(1.0, 2.0, 0.0, 0.0, 0.0, 1.0)
    scaled = clothoid.Scale(sfactor, center=(0, 0))
    assert scaled.XStart == pytest.approx(clothoid.XStart * sfactor)
    assert scaled.YStart == pytest.approx(clothoid.YStart * sfactor)
    assert scaled.length == pytest.approx(clothoid.length * sfactor)
    assert scaled.KappaStart == pytest.approx(clothoid.KappaStart / sfactor)
    assert scaled.dk == pytest.approx(clothoid.dk / sfactor**2)


@pytest.mark.parametrize(
    "s_begin, s_end",
    [
        (0, 0.5),
        (0.25, 0.75),
        (0, 1),
    ],
)
def test_trim(s_begin, s_end):
    clothoid = Clothoid.StandardParams(1.0, 2.0, 0.0, 0.0, 0.0, 1.0)
    trimmed = clothoid.Trim(s_begin, s_end)
    assert trimmed.length == pytest.approx(s_end - s_begin)
    assert trimmed.XStart == pytest.approx(clothoid.X(s_begin))
    assert trimmed.YStart == pytest.approx(clothoid.Y(s_begin))
    assert trimmed.KappaStart == pytest.approx(clothoid.ThetaD(s_begin))
    assert trimmed.ThetaStart == pytest.approx(clothoid.Theta(s_begin))
    assert trimmed.XEnd == pytest.approx(clothoid.X(s_end))
    assert trimmed.YEnd == pytest.approx(clothoid.Y(s_end))
    assert trimmed.KappaEnd == pytest.approx(clothoid.ThetaD(s_end))
    assert trimmed.ThetaEnd == pytest.approx(clothoid.Theta(s_end))
    assert trimmed.dk == pytest.approx(clothoid.dk)


# --- Test Closest Point Projection ---


@pytest.mark.parametrize(
    "x, y",
    [
        (1.0, 2.0),
        (0.5, 0.5),
        (-1.0, -2.0),
    ],
)
def test_closest_point_projection(x, y):
    clothoid = Clothoid.StandardParams(0, 0, 0, 0.1, 0.01, 5)
    projected_point = clothoid.ClosestPoint(x, y)
    assert isinstance(projected_point, tuple)
    assert len(projected_point) == 2
    assert isinstance(projected_point[0], float)
    assert isinstance(projected_point[1], float)


@pytest.mark.parametrize(
    "x, y",
    [
        (1.0, 2.0),
        (0.5, 0.5),
        (-1.0, -2.0),
    ],
)
def test_closest_point_arc_length(x, y):
    clothoid = Clothoid.StandardParams(0, 0, 0, 0.1, 0.01, 5)
    arc_length = clothoid.ClosestPointArcLength(x, y)
    assert isinstance(arc_length, float)
    assert 0 <= arc_length <= clothoid.length


@pytest.mark.parametrize(
    "x, y",
    [
        (1.0, 2.0),
        (0.5, 0.5),
        (-1.0, -2.0),
    ],
)
def test_distance_to_clothoid(x, y):
    clothoid = Clothoid.StandardParams(0, 0, 0, 0.1, 0.01, 5)
    distance = clothoid.Distance(x, y)
    assert isinstance(distance, float)
    assert distance >= 0


# --- Intersections ---


@pytest.mark.parametrize(
    "G1Params1, G1Params2, expectedNumIntersections",
    [
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (0.0, 0.0, math.pi, 1, 0.95, -math.pi / 4),
            2,
        ),
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (1.0, 0.0, math.pi, 1, 2, -math.pi / 4),
            1,
        ),
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (1.0, 0.0, math.pi, 0.5, 0.5, -math.pi / 4),
            0,
        ),
    ],
)
def test_intersection_arc_lengths(G1Params1, G1Params2, expectedNumIntersections):
    clothoid = Clothoid.G1Hermite(*G1Params1)
    other = Clothoid.G1Hermite(*G1Params2)
    parameter_list = clothoid.IntersectionArcLengths(other)
    assert len(parameter_list) == expectedNumIntersections
    P1, P2 = zip(*parameter_list) if parameter_list else ((), ())
    for i, j in zip(P1, P2):
        assert clothoid.X(i) == pytest.approx(other.X(j))
        assert clothoid.Y(i) == pytest.approx(other.Y(j))


@pytest.mark.parametrize(
    "G1Params1, G1Params2, expectedNumIntersections",
    [
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (0.0, 0.0, math.pi, 1, 0.95, -math.pi / 4),
            2,
        ),
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (1.0, 0.0, math.pi, 1, 2, -math.pi / 4),
            1,
        ),
        (
            (0.0, 0.0, math.pi / 4, 1, 1, 0),
            (1.0, 0.0, math.pi, 0.5, 0.5, -math.pi / 4),
            0,
        ),
    ],
)
def test_intersection_points(G1Params1, G1Params2, expectedNumIntersections):
    clothoid = Clothoid.G1Hermite(*G1Params1)
    other = Clothoid.G1Hermite(*G1Params2)
    points = clothoid.IntersectionPoints(other)
    assert len(points) == expectedNumIntersections
    for p in points:
        assert other.Distance(*p) == pytest.approx(0)


# --- Caching ---


def test_default_cache_size_configurable():
    clothoid = Clothoid.G1Hermite(0.0, 0.0, math.pi / 4, 1, 1, 0)
    assert clothoid.ProjectPointOntoClothoid.cache_info().maxsize == 32
    clothoid.SetupProjectionCache(64)
    assert clothoid.ProjectPointOntoClothoid.cache_info().maxsize == 64


def test_cache_disable():
    clothoid = Clothoid.G1Hermite(0.0, 0.0, math.pi / 4, 1, 1, 0)
    assert clothoid.ProjectPointOntoClothoid.cache_info().maxsize == 32
    clothoid.SetupProjectionCache(None)
    assert not hasattr(clothoid.ProjectPointOntoClothoid, "cache_info")


def test_caches_are_independent(mocker):
    clothoid1 = Clothoid.G1Hermite(0.0, 0.0, math.pi / 4, 1, 1, 0)
    clothoid2 = Clothoid.G1Hermite(0.0, 0.0, math.pi / 4, 1, 1, 0)

    clothoid1.Distance(5, 5)

    assert clothoid1.ProjectPointOntoClothoid.cache_info().currsize == 1
    assert clothoid2.ProjectPointOntoClothoid.cache_info().currsize == 0


# --- Test G2 Solver ---


@pytest.mark.parametrize(
    "x0, y0, t0, k0, x1, y1, t1, k1",
    [
        (0, 0, 0, 0, 1, 1, math.pi / 4, 0.1),
        (1, 2, math.pi / 6, 0.2, -1, -2, -math.pi / 6, -0.2),
    ],
)
def test_solve_g2(x0, y0, t0, k0, x1, y1, t1, k1):
    clothoids = SolveG2(x0, y0, t0, k0, x1, y1, t1, k1)
    assert len(clothoids) == 3
    assert all(isinstance(clothoid, Clothoid) for clothoid in clothoids)
