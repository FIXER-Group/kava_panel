from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:index')
