import os, time, asyncio, typing
from . import colors

ANSI = colors.ANSI

Any = typing.Any


class CONSOLE:
    @classmethod
    def clear(self) -> None:
        """Clears the console output."""
        os.system("cls" if os.name == "nt" else "clear")
        print(ANSI.RESET, end="")

    @classmethod
    def sleep(self, x: int | float | None = 0) -> None:
        """Suspend execution of the calling thread for the given number of seconds."""
        time.sleep(x)

    @classmethod
    async def sleep_async(
        self, delay: int | float | None = 0, result: Any | None = None
    ) -> None:
        """
        Block for delay seconds.

        If result is provided, it is returned to the caller when the coroutine completes.

        `sleep()` always suspends the current task, allowing other tasks to run.
        """
        return await asyncio.sleep(delay, result)
