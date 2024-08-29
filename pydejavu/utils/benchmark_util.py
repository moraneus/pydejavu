import os
import time
from functools import wraps

import psutil


def gtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start measuring
        process = psutil.Process(os.getpid())
        start_time = time.time()
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)

        # Execute the function
        result = func(*args, **kwargs)

        # End measuring
        end_time = time.time()
        end_memory = process.memory_info().rss
        end_cpu = process.cpu_percent(interval=None)

        # Calculate results
        elapsed_time = end_time - start_time
        memory_used = end_memory - start_memory  # in bytes
        cpu_used = end_cpu - start_cpu  # percentage

        # Convert memory usage to MB
        memory_used_mb = memory_used / (1024 * 1024)

        # Print results
        print(f"Function '{func.__name__}' - Elapsed time: {elapsed_time:.6f} seconds")
        print(f"Function '{func.__name__}' - Memory used: {memory_used_mb:.2f} MB")
        print(f"Function '{func.__name__}' - CPU used: {cpu_used:.2f}%")

        return result

    return wrapper
