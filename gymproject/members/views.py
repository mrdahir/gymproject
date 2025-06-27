from django.shortcuts import render, redirect
from .models import Member
from .forms import MemberForm, StaffUserCreationForm
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum

def register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.registered_by = request.user
            member.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'members/register.html', {'form': form})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'members/list.html', {'members': members, 'today': date.today()})

def is_admin(user):
    return user.is_superuser

@login_required
def dashboard(request):
    return render(request, 'members/dashboard.html')

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'members/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = StaffUserCreationForm()
    return render(request, 'members/create_user.html', {'form': form})

@login_required
def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'members/member_detail.html', {'member': member})

@login_required
def report(request):
    members = Member.objects.all()
    total_usd = members.filter(currency='usd').aggregate(total=Sum('amount_paid'))['total'] or 0
    total_sls = members.filter(currency='sls').aggregate(total=Sum('amount_paid'))['total'] or 0
    return render(request, 'members/report.html', {'members': members, 'total_usd': total_usd, 'total_sls': total_sls})
