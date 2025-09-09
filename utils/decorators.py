import time
import logging

def timer(func):
    """
    This decorator measures the execution time of our algorithms.
    Usage: '@timer' above the function you want to measure. 
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"{func.__name__} took {duration:.6f} seconds")
        print(f"{func.__name__} took {duration:.6f} seconds")
        return result
    return wrapper