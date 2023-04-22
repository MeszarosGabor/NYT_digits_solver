import pytest

from .solver import describe_moves, solve_digits, solve_digits_with_moves


@pytest.mark.parametrize(
    "moves,expected",
    [
        (
            [[1,1], [2]],
            ["1+1"],
        )
    ]
)
def test_moves(
        moves,
        expected,
):
    assert describe_moves(moves) == expected


@pytest.mark.parametrize(
    "numbers,target,solution",
    [
        (
            [1,1,],
            2,
            [[[1,1], [2]]],
        )
    ]
)
def test_unique_single_steps(
        numbers,
        target,
        solution,
):
    assert solve_digits(numbers, target) == solution
