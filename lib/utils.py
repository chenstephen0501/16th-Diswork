from datetime import datetime
from django.utils import timezone

def to_aware_datetime(time):
    naive_datetime = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
    return aware_datetime

def comparison_time(get_time, start_time, end_time, ):
    task_state = {}
    get_naive_time = datetime.strptime(get_time, "%Y-%m-%dT%H:%M")
    start_naive_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_naive_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    
    if (get_naive_time > end_naive_time):
        task_state["state"] = "error"
        task_state["message"] = "The completion time cannot be earlier than the time the task is received"

        return task_state
    elif (start_naive_time > end_naive_time):
        task_state["state"] = "error"
        task_state["message"] = "The completion time cannot be earlier than the start time."

        return task_state
    else:
        task_state["state"] = "success"
        task_state["message"] = "Task created successfully."
        
        return task_state