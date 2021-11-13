import numpy as np
from time import sleep
from logging import getLogger

logger = getLogger(__name__)


def randsleep(target: int, max_: int = 400):
    """Sleep for a random length of time around target but less than max.

    We use a poisson distribution, since that models human action a bit better
    than a linear.
    """
    duration = min(np.random.poisson(target), max_)
    logger.debug(f"Sleeping for {duration} s")
    sleep(duration)
