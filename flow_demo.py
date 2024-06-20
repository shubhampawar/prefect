import os
import asyncio
from prefect import flow, task
import time
# Define asynchronous tasks with appropriate delays
@flow
def do_something_important(duration: int, not_so_secret_value: str) -> None:
    print(f"Sleeping for {duration} seconds")
    time.sleep(duration)
    print(f"Doing something important with {not_so_secret_value} after {duration} seconds!")

# Define the flow
@flow(log_prints=True)
async def some_work():
    # Fetch environment variables
    environment = os.environ.get("EXECUTION_ENVIRONMENT", "local")
    not_so_secret_value = os.environ.get("MY_NOT_SO_SECRET_CONFIG")

    print(f"Coming to you live from {environment}!")

    if not_so_secret_value is None:
        raise ValueError("You forgot to set MY_NOT_SO_SECRET_CONFIG!")

    # Create a list of tasks with different sleep durations

    do_something_important(5, not_so_secret_value),
    do_something_important(4, not_so_secret_value),
    do_something_important(3, not_so_secret_value),
    do_something_important(2, not_so_secret_value)


    # Run all tasks concurrently
    # await asyncio.gather(*tasks)

# Run the flow
if __name__ == "__main__":
    asyncio.run(some_work())
