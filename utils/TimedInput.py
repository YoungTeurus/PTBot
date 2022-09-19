import msvcrt
import sys
import time


def wasKeyHitInTime(timeSecs: float, timer=time.monotonic) -> bool:
    sys.stdout.flush()
    endtime = timer() + timeSecs
    while timer() < endtime:
        if msvcrt.kbhit():
            c = msvcrt.getwche()
            if c == '\003':
                raise KeyboardInterrupt
            elif c in ('\r', '\n'):
                return True
        time.sleep(0.04)
    return False
