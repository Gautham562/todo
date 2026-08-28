from django.shortcuts import render, redirect
from todo.models import Task, Category
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from todo.forms import RegisterForm

@login_required
def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    tasks = Task.objects.filter(
        user=request.user,
        is_completed=False
    ).order_by('-updated_at')

    completed_tasks = Task.objects.filter(
        user=request.user,
        is_completed=True
    )

    if query:
        tasks = tasks.filter(task__icontains=query)
        completed_tasks = completed_tasks.filter(
            task__icontains=query
        )

    if category:
        tasks = tasks.filter(category_id=category)
        completed_tasks = completed_tasks.filter(
            category_id=category
        )

    categories = Category.objects.all()

    context = {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'categories': categories,
        'query': query,
    }

    return render(request, 'home.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})