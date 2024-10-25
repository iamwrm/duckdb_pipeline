import asyncio
from concurrent.futures import ProcessPoolExecutor
import time


# Example of a compute-heavy function (calculates the nth Fibonacci number)
def compute_fibonacci(n, k):
    if n <= 1:
        return n * k
    else:
        return compute_fibonacci(n - 1, k) + compute_fibonacci(n - 2, k)


# Asynchronous wrapper to run the compute-heavy function in a ProcessPoolExecutor
async def run_compute_heavy(executor, f, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, f, *args)


async def main():
    # Define the numbers for which to compute Fibonacci numbers
    fibonacci_numbers = [i for i in range(30, 40)]
    k = 1.1

    # Create a ProcessPoolExecutor with a number of workers equal to the CPU cores
    with ProcessPoolExecutor() as executor:
        # Schedule all compute-heavy tasks concurrently
        tasks = [
            asyncio.create_task(run_compute_heavy(executor, compute_fibonacci, n, k))
            for n in fibonacci_numbers
        ]

        # Optionally, show progress as tasks complete
        for coroutine in asyncio.as_completed(tasks):
            result = await coroutine
            print(f"Fibonacci result: {result}")


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
