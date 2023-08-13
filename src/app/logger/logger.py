import logging
import traceback

from inspect import iscoroutinefunction, isgeneratorfunction
from types import TracebackType

from rich.logging import RichHandler




logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[RichHandler(rich_tracebacks=True)]
)


class MyLogger(logging.getLoggerClass()):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.catch._logger = self

    class catch:
        _logger = None

        msg = None
        func = None
        exc = None

        def __init__(self, msg="An error in func '{name}':", *, reraise=False, exc=Exception):
            self.msg = msg
            self.func = None
            self.reraise = reraise
            self.exc = exc

        async def __async_wrapper(self, *args, **kwargs):
            with self:
                return await self.func(*args, **kwargs)

        def __gen_wrapper(self, *args, **kwargs):
            with self:
                return (yield from self.func(*args, **kwargs))

        def __sync_wrapper(self, *args, **kwargs):
            with self:
                return self.func(*args, **kwargs)

        def __call__(self, func):
            self.func = func

            if iscoroutinefunction(func):
                return self.__async_wrapper

            if isgeneratorfunction(func):
                return self.__gen_wrapper

            return self.__sync_wrapper

        def __enter__(self):
            return None

        def __exit__(self, type_, value, traceback_):
            if type_ is None: return
            if not isinstance(value, self.exc): return

            tb = None
            frames = tuple(traceback.walk_tb(traceback_))
            stop = len(frames) - 1

            for i, (frame, _) in enumerate(reversed(frames)):
                if i == stop: break

                tb = TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)

            value.with_traceback(tb)

            self._logger.exception(self.msg.format(name=self.func.__name__))

            return not self.reraise


logging.setLoggerClass(MyLogger)
