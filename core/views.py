from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone

from .models import Project, Task, Profile
from .forms import SignupForm, ProjectForm, TaskForm, UserUpdateForm, ProfileUpdateForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'core/profile.html', context)


@login_required
def dashboard(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    if request.user.profile.role == 'admin':
        tasks = Task.objects.filter(project__in=projects)
    else:
        tasks = Task.objects.filter(project__in=projects, assigned_to=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    progress_tasks = tasks.filter(status='progress').count()
    overdue_tasks = tasks.filter(
        due_date__lt=timezone.now().date()
    ).exclude(status='completed').count()

    recent_tasks = tasks.order_by('-created_at')[:5]

    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress_tasks': progress_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks,
    }

    return render(request, 'core/dashboard.html', context)


@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct()

    return render(request, 'core/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    if request.user.profile.role != 'admin':
        messages.error(request, "Only admin can create projects.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            messages.success(request, "Project created successfully.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'core/project_form.html', {'form': form, 'title': 'Create Project'})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.profile.role != 'admin':
        messages.error(request, "Only admin can update projects.")
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'core/project_form.html', {'form': form, 'title': 'Update Project'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not project.is_member(request.user):
        messages.error(request, "You do not have access to this project.")
        return redirect('project_list')

    if request.user.profile.role == 'admin':
        tasks = project.tasks.all().order_by('-created_at')
    else:
        tasks = project.tasks.filter(assigned_to=request.user).order_by('-created_at')

    return render(request, 'core/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user.profile.role != 'admin':
        messages.error(request, "Only admin can create tasks.")
        return redirect('project_detail', pk=project.id)

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.full_clean()
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm(project=project)

    return render(request, 'core/task_form.html', {
        'form': form,
        'title': 'Create Task',
        'project': project
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if not project.is_member(request.user):
        messages.error(request, "You do not have access to this task.")
        return redirect('project_list')

    if request.user.profile.role != 'admin':
        messages.error(request, "Only admin can edit tasks.")
        return redirect('project_detail', pk=project.id)

    is_admin = True # Since we checked the role above
    is_assigned_member = task.assigned_to == request.user

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)

        if form.is_valid():
            updated_task = form.save(commit=False)

            if not is_admin:
                updated_task.title = task.title
                updated_task.description = task.description
                updated_task.assigned_to = task.assigned_to
                updated_task.priority = task.priority
                updated_task.due_date = task.due_date

            updated_task.full_clean()
            updated_task.save()
            messages.success(request, "Task updated successfully.")
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm(instance=task, project=project)

    return render(request, 'core/task_form.html', {
        'form': form,
        'title': 'Update Task',
        'project': project
    })