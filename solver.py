import time
import typing
from collections import deque

import click

def describe_moves(moves: typing.List[typing.List[int]]) -> typing.List[str]:
    descriptions = []
    for a, b in zip(moves, moves[1:]):
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                remainders = [a[k] for k in range(len(a)) if k not in [i,j]]                
                operations = {
                    "+": lambda x, y: x + y,
                    "-": lambda x, y: abs(x - y),
                    "*": lambda x, y: x * y,
                }
                if  a[j] != 0 and a[i] % a[j] == 0:
                    operations["/"] = lambda x, y: x // y
                if a[i] != 0 and a[j] % a[i] == 0:
                    operations["/"] = lambda x, y: y // x
                for op_sym, op in operations.items():
                    b_candidate = sorted(remainders + [op(a[i], a[j])])
                    if b_candidate == b:
                        descriptions.append(f"{max(a[i], a[j])}{op_sym}{min(a[i], a[j])}")
    return descriptions



def solve_digits(numbers: typing.List[int] , target: int, how_many_sols=1) -> typing.List:
    numbers.sort()

    todo = deque([[numbers]])
    solutions = []
    
    while todo:
        act = todo.popleft()
        tip = act[-1]
        for i in range(len(tip)):
            for j in range(i + 1, len(tip)):
                remainders = [tip[k] for k in range(len(tip)) if k not in [i,j]]                
                operations = [
                    lambda x, y: x + y,
                    lambda x, y: abs(x - y),
                    lambda x, y: x * y,
                ]  
                if  tip[j] != 0 and tip[i] % tip[j] == 0:
                    operations.append(lambda x, y: x // y)
                if tip[i] != 0 and tip[j] % tip[i] == 0:
                    operations.append(lambda x, y: y // x)
                
                for op in operations:
                    new_tip = sorted(remainders + [op(tip[i], tip[j])])
                    if len(new_tip) > 1:
                        new_act = act[::]
                        new_act.append(new_tip)
                        todo.append(new_act)
                    elif new_tip[0] == target:
                        new_sol_candidate = act + [new_tip]
                        if new_sol_candidate not in solutions:
                            solutions.append(new_sol_candidate)
                            if how_many_sols and len(solutions) >= how_many_sols:
                                return solutions
    return solutions


def solve_digits_with_moves(numbers: typing.List[int] , target: int, how_many_sols=1) -> typing.List:
    return [
        describe_moves(solution)
        for solution in solve_digits(numbers, target, how_many_sols)
    ]


@click.command()
@click.option(
    "-n", "--numbers", type=str,
    help="Comma-separated list of numbers")
@click.option(
    "-t", "--target", type=int,
    help="target number to be built")
@click.option(
    "-c","--how_many_solutions", type=int,
    help="The number of solutions the solver should return (None=find all)",
    default=None)
def main(numbers, target, how_many_solutions):
    numbers = [int(number) for number in numbers.split(",")]
    t0 = time.time()
    solutions = solve_digits_with_moves(numbers, target, how_many_sols=how_many_solutions)
    t1 = time.time()
    print(f"Found {len(solutions)} solutions. Took {round(t1 - t0, 2)} seconds.")
    for sol in solutions:
        for move in sol:
            print(move)
        print("\n")

if __name__ == "__main__":
    main()
