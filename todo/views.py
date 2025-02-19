from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from django.http import JsonResponse


@login_required
def todo_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo/todo_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
            Task.objects.create(user=request.user, title=title, description=description)
    return redirect("todo_list")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("todo_list")

@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = "completed" if task.status != "completed" else "pending"
    task.save()
    return JsonResponse({"status": task.status})


@login_required
def delete_all_tasks(request):
    Task.objects.filter(user=request.user).delete()
    return redirect("todo_list")

@login_required
def delete_completed_tasks(request):
    Task.objects.filter(user=request.user, status="completed").delete()
    return redirect("todo_list")