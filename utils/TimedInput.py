import msvcrt
import sys
import time


class TimeoutExpired(Exception):
    pass


def input_with_timeout(timeout, prompt=None, timer=time.monotonic) -> str:
    if prompt is not None:
        sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    line = ''
    while timer() < endtime:
        if msvcrt.kbhit():
            c = msvcrt.getwche()
            if c in ('\r', '\n'):
                return line
            if c == '\003':
                raise KeyboardInterrupt
            else:
                line += c
        time.sleep(0.04)  # just to yield to other processes/threads
    raise TimeoutExpired
