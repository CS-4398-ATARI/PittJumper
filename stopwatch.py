# import the builtin time module, this is always available
import time


class Stopwatch:

    # Utility class to keep track of time.
    def __init__(self):
        self.seconds = time.time()
        self.pausedTime = 0

    def get_seconds(self):
         # Get seconds.
        tempTime = time.time()
        seconds = tempTime - self.seconds
        return seconds


    def reset(self):
        # Reset the timer.
        self.seconds = time.time()



