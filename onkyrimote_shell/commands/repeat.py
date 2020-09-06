import itertools
import time

from kien import create_commander, transform, validate, var
from kien.validation import is_float, is_gte, is_int

command = create_commander(
    "repeat",
    description=(
        "Conveniently execute a command multiple times (e.g. "
        "following changes of the color sampling results)."
    ),
)


@command("repeat", is_abstract=True)
def repeat():
    pass


_repetitions = var("repetitions", description="number of repetitions, 0 for infinite")
_delay = var("delay", description="delay in seconds, 0 for no delay")


@command(
    _repetitions,
    _delay,
    var("arguments", greedy=True),
    parent=repeat,
    inject=["dispatch"],
)
@validate(repetitions=(is_int() & is_gte(0)), delay=(is_float() & is_gte(0)))
@transform(repetitions=int, delay=float)
def repeat_do(dispatch, repetitions, delay, arguments):
    """
    Repeat a single command for a number of times with a given delay.
    You may stop execution with CTRL-C.
    """

    for i in itertools.count(start=0):
        repetitions += 1
        if i != 0:
            time.sleep(delay)
        yield from dispatch(arguments)
        if repetitions == i:
            break
