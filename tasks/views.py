from django.shortcuts import render
from .models import Task
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# HOME PAGE - shows all tasks for this session

def home(request):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    tasks = Task.objects.filter(session_id=session_id)
    return render(request, 'tasks/home.html', {
        "tasks":tasks
    })
# CREATE NEW TASK

def create(request):
    # Ensure session exits
    if not request.session.session_key:
        request.session.create()

    session_id= request.session.session_key
    
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST["due_date"]
        completed = "completed" in request.POST

        # Convert the due_date string to a datetime object
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")


        task = Task(
            session_id=session_id,
            title=title,
            description=description,
            due_date=due_date_obj,
            completed=completed)
        task.save()
        return HttpResponseRedirect (reverse("home"))
        

    tasks= Task.objects.filter(session_id=session_id)

    return render(request, "tasks/create.html", {
        "tasks": tasks
        })

# EDIT TASK

def edit(request, task_id):
    session_id = request.session.session_key

    tasks = Task.objects.get(id=task_id, session_id=session_id)

    if request.method =="POST":
        tasks.title = request.POST['title']
        tasks.description = request.POST['description']
        tasks.due_date = datetime.strptime(request.POST["due_date"], "%Y-%m-%dT%H:%M")
        tasks.completed = 'completed' in request.POST

        tasks.save()
        return HttpResponseRedirect (reverse("home"))
        

    return render(request, "tasks/edit.html", {
        "task": tasks
    })
# DELETE TASK

def delete(request, task_id):
    session_id = request.session.session_key
    tasks= Task.objects.get(id=task_id, session_id=session_id)
    tasks.delete()
    return HttpResponseRedirect (reverse("home"))