import os, time, asyncio, typing
from . import colors as colors


def clear() -> None:
    """Clears the console output."""
    os.system("cls" if os.name == "nt" else "clear")
    print(colors.RESET, end="")


def sleep(x: int | float = 0) -> None:
    """Suspend execution of the calling thread for the given number of seconds."""
    time.sleep(x)


async def sleep_async(delay: int | float = 0, result: typing.Any = None) -> None:
    """
    Block for delay seconds.

    If result is provided, it is returned to the caller when the coroutine completes.

    `sleep()` always suspends the current task, allowing other tasks to run.
    """
    return await asyncio.sleep(delay, result)
