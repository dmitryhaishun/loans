from .worker import app


@app.task(name="my_task")
def print_hello():
    print("HELLO")
