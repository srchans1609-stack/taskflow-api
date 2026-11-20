from fastapi import FastAPI, Request
from collections.abc import Callable
import time


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable
):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    print(f"Tiempo de proceso: {process_time}")

    response.headers["X-Process-Time"] = str(process_time)

    return response