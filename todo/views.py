from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from django.contrib.auth.decorators import login_required


@login_required
def addTask(request):
    if request.method == "POST":
        task = request.POST.get('task')
        priority = request.POST.get('priority', 'Medium')
        due_date = request.POST.get('due_date')
        category_id=request.POST.get('category')
        if task:
            Task.objects.create(
                user=request.user,
                task=task,
                category_id=category_id,
                priority=priority,
                due_date=due_date if due_date else None
            )

    return redirect('home')


@login_required
def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('home')


@login_required
def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = False
    task.save()
    return redirect('home')


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    categories=Category.objects.all()
    if request.method == "POST":
        task.task = request.POST.get("task")
        task.priority = request.POST.get("priority")
        task.due_date = request.POST.get("due_date") or None
        task.category_id=request.POST.get("category")
        task.save()

        return redirect('home')

    return render(
        request,
        'edit_task.html',
        {'task': task,
         'categories':categories}
    )


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('home')