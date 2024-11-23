# todo/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'


@login_required
def task_list(request):
    cache_key = f'task_list_{request.user.id}'
    tasks = cache.get(cache_key)

    if not tasks:
        tasks = list(Task.objects.filter(user=request.user).order_by('status', '-created_at'))
        cache.set(cache_key, tasks, 300)  # Cache for 5 minutes

    return render(request, 'todo/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(user=request.user, title=title, description=description)
        return redirect('task_list')
    return render(request, 'todo/task_create.html')


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        return redirect('task_list')
    return render(request, 'todo/task_update.html', {'task': task})
