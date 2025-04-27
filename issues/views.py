from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ElectricityIssueForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import ElectricityIssue, Feedback
from .forms import FeedbackForm
# Create your views here.

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'issues/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('issue_list')
    else:
        form = AuthenticationForm()
    return render(request, 'issues/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Report an Electricity Issue
@login_required
def report_issue(request):
    if request.method == 'POST':
        form = ElectricityIssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('issue_list')
    else:
        form = ElectricityIssueForm()
    return render(request, 'issues/report_issue.html', {'form': form})

@login_required
def issue_list(request):
    issues = ElectricityIssue.objects.filter(user=request.user)
    return render(request, 'issues/issue_list.html', {'issues': issues})

@staff_member_required
def admin_issue_list(request):
    issues = ElectricityIssue.objects.all().order_by('-created_at')  # Latest first
    return render(request, 'issues/admin_issue_list.html', {'issues': issues})

# Admin view to update complaint status
@staff_member_required
def update_issue_status_admin(request, issue_id):
    issue = ElectricityIssue.objects.get(id=issue_id)
    if request.method == 'POST':
        issue.status = request.POST.get('status')
        issue.save()
        return redirect('admin_issue_list')
    return render(request, 'issues/update_issue_admin.html', {'issue': issue})


@login_required
def submit_feedback(request, issue_id):
    issue = get_object_or_404(ElectricityIssue, id=issue_id)
    existing_feedback = Feedback.objects.filter(user=request.user, complaint=issue).first()

    if request.method == "POST" and not existing_feedback:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.complaint = issue
            feedback.save()
            return redirect('issue_list')  # Redirect after submission
    else:
        form = FeedbackForm()

    return render(request, 'issues/submit_feedback.html', {
        'form': form,
        'issue': issue,
        'existing_feedback': existing_feedback
    })


@login_required
def view_feedback(request):
    if request.user.is_staff:  # Only admin can see feedback
        feedbacks = Feedback.objects.all().order_by('-created_at')
        return render(request, 'issues/view_feedback.html', {'feedbacks': feedbacks})
    else:
        return redirect('issue_list')  # Redirect normal users
