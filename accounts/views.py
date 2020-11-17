from django.shortcuts import render, redirect
from accounts.forms import LoginAuthForm
from django.contrib.auth import login



def index(request):
    if request.user.is_authenticated:
        return redirect('panel:index')
    else:
        if request.method == 'POST':
            form = LoginAuthForm(data=request.POST)
            if form.is_valid():
                login(request,form.get_user())
                return redirect('panel:index')
        else:
            form = LoginAuthForm()
        return render(request, 'registration/login.html', {'form': form})



