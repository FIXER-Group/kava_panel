from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Server_stat


@login_required(login_url='/')

def index(request):
    context ={}
    cpu_cores = Server_stat.objects.all()
    context['cpu_cores'] = Server_stat.cpu_percent(True)
    return render(request, 'dashboard.html', context )

def logout_view(request):
    logout(request)
    return redirect('accounts:index')

def about(request):
    return render(request, 'about.html')

def stats_update(request):
     results = {'cpu_percent': Server_stat.cpu_percent(),
                'cpu_per_core': Server_stat.cpu_percent(True),
                'cpu_name': Server_stat.cpu_name(),
                'ram_percent': Server_stat.ram_percent(),
                'ram_total': Server_stat.ram_total(),
                'ram_usage': Server_stat.ram_used(),
                'disk_percent': Server_stat.disk_percent(),
                'disk_total': Server_stat.disk_total(),
                'disk_usage': Server_stat.disk_usage(),
                'swap_percent': Server_stat.swap_percent(),
                'swap_total': Server_stat.swap_total(),
                'uptime': Server_stat.uptime_days()}
     return JsonResponse(results)