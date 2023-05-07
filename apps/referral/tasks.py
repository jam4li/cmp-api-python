from celery import shared_task


@shared_task
def my_example_task():
    # Your task logic here
    print("Task completed")
    return "Task completed"
