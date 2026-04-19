"""
Tests for pymadcad brick() function - the NaN bug with default parameters.

This test validates the workaround for the bug where brick() without parameters
generates NaN coordinates due to inf - inf = nan in Box calculation.
"""

from math import isfinite
from madcad import *


def test_brick_default_generates_nan():
    """Test that brick() without parameters produces NaN (the bug)."""
    b = brick()
    has_nan = any(
        not isfinite(p.x) or not isfinite(p.y) or not isfinite(p.z) for p in b.points
    )
    assert has_nan, "brick() should produce NaN with default params"


def test_brick_with_explicit_center_and_width():
    """Test workaround with explicit center and width."""
    b = brick(center=vec3(0, 0, 0), width=vec3(1, 1, 1))

    assert len(b.points) == 8, "brick should have 8 vertices"
    assert len(b.faces) == 12, "brick should have 12 faces"

    for p in b.points:
        assert isfinite(p.x), f"Point {p} has non-finite x"
        assert isfinite(p.y), f"Point {p} has non-finite y"
        assert isfinite(p.z), f"Point {p} has non-finite z"

    box = b.box()
    assert abs(box.min.x + 0.5) < 0.001
    assert abs(box.min.y + 0.5) < 0.001
    assert abs(box.min.z + 0.5) < 0.001
    assert abs(box.max.x - 0.5) < 0.001
    assert abs(box.max.y - 0.5) < 0.001
    assert abs(box.max.z - 0.5) < 0.001


def test_brick_with_min_max():
    """Test workaround with explicit min and max."""
    b = brick(min=vec3(-1, -2, -3), max=vec3(1, 2, 3))

    for p in b.points:
        assert isfinite(p.x)
        assert isfinite(p.y)
        assert isfinite(p.z)

    box = b.box()
    assert abs(box.min.x + 1) < 0.001
    assert abs(box.min.y + 2) < 0.001
    assert abs(box.min.z + 3) < 0.001


def test_brick_with_two_args():
    """Test brick(min, max) with two vec3 arguments."""
    b = brick(vec3(0, 0, 0), vec3(2, 2, 2))

    for p in b.points:
        assert isfinite(p.x)
        assert isfinite(p.y)
        assert isfinite(p.z)

    box = b.box()
    assert box.size.x == 2.0
    assert box.size.y == 2.0
    assert box.size.z == 2.0


def test_brick_is_surface():
    """Test that brick generates a valid surface."""
    b = brick(center=vec3(0, 0, 0), width=vec3(1, 1, 1))
    assert b.issurface()


def test_brick_face_count():
    """Test that brick has correct number of faces."""
    b = brick(center=vec3(0, 0, 0), width=vec3(1, 1, 1))
    assert len(b.faces) == 12


def test_brick_vertex_count():
    """Test that brick has correct number of vertices."""
    b = brick(center=vec3(0, 0, 0), width=vec3(1, 1, 1))
    assert len(b.points) == 8


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        ("test_brick_default_generates_nan", test_brick_default_generates_nan),
        (
            "test_brick_with_explicit_center_and_width",
            test_brick_with_explicit_center_and_width,
        ),
        ("test_brick_with_min_max", test_brick_with_min_max),
        ("test_brick_with_two_args", test_brick_with_two_args),
        ("test_brick_is_surface", test_brick_is_surface),
        ("test_brick_face_count", test_brick_face_count),
        ("test_brick_vertex_count", test_brick_vertex_count),
    ]

    passed = 0
    failed = 0

    for name, test in tests:
        try:
            test()
            print(f"  PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {name} - {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {name} - {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    print("Testing brick() NaN bug and workarounds...")
    success = run_all_tests()
    exit(0 if success else 1)
