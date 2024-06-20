import os
import time
from prefect import flow, task
import asyncio


@task
async def do_something_important5(not_so_secret_value: str) -> None:
    print("sleeping 5")
    await asyncio.sleep(5)
    print(f"Doing something important with {not_so_secret_value}!")


@task
async def do_something_important4(not_so_secret_value: str) -> None:
    print("sleeping 4")
    await asyncio.sleep(4)
    print(f"Doing something important with {not_so_secret_value}!")


@task
async def do_something_important3(not_so_secret_value: str) -> None:
    print("sleeping 3")
    await asyncio.sleep(3)
    print(f"Doing something important with {not_so_secret_value}!")


@task
async def do_something_important2(not_so_secret_value: str) -> None:
    print("sleeping 2")
    await asyncio.sleep(2)
    print(f"Doing something important with {not_so_secret_value}!")


@flow(log_prints=True)
async def some_work():
    environment = os.environ.get("EXECUTION_ENVIRONMENT", "local")

    print(f"Coming to you live from {environment}!")

    not_so_secret_value = os.environ.get("MY_NOT_SO_SECRET_CONFIG")

    if not_so_secret_value is None:
        raise ValueError("You forgot to set MY_NOT_SO_SECRET_CONFIG!")

    await do_something_important5(not_so_secret_value)
    await do_something_important4(not_so_secret_value)
    await do_something_important3(not_so_secret_value)
    await do_something_important2(not_so_secret_value)


if __name__ == "__main__":
    some_work.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/demo_flow.py:some_work",
    ).deploy(
        name="demo-deployment",
        work_pool_name="local",
        job_variables={
            "env": {
                "EXECUTION_ENVIRONMENT": "{{ $EXECUTION_ENVIRONMENT }}",
                "MY_NOT_SO_SECRET_CONFIG": "{{ $MY_NOT_SO_SECRET_CONFIG }}",
            }
        },
    )
