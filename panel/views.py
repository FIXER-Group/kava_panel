from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Server_stat, CPULogs, RAMLogs,Server_processes,Server_connections,Server_connection_speed
from django.contrib import messages
from chartjs.views.lines import BaseLineChartView
import socket
import platform
import requests
import datetime
from rest_framework.authtoken.models import Token


@login_required(login_url='/')

def index(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logout_message', extra_tags='logout')
    return redirect('accounts:index')

@login_required(login_url='/')
def edit_profile(request):
    token, created = Token.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'password_changed', extra_tags='password_changed')
            return redirect('panel:edit_profile')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'edit_profile.html', {'form' : form, 'token': token.key})

@login_required(login_url='/')
def process(request):
    return render(request, 'process.html', {'List': Server_processes.get_server_processes()})

@login_required(login_url='/')
def network(request):
    return render(request, 'network.html', {'List': Server_connections.get_server_network_connections()})

@login_required(login_url='/')
def system(request):
    return render(request, 'system.html',
                  {'Name': platform.system(),
                  'Release': platform.release(),
                  'Version': platform.version(),
                  'Architecture': platform.machine(),
                  'Hostname': socket.gethostname(),
                  'IpAdress': requests.get('https://checkip.amazonaws.com').text.strip(),
                  'Processor': platform.processor()}
                  )

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
                'uptime': Server_stat.uptime_days(),
                'upload': Server_connection_speed.network_usage()[0],
                'download': Server_connection_speed.network_usage()[1]
                }
     return JsonResponse(results)


class LineChartCpu(BaseLineChartView):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.earlier = self.now - datetime.timedelta(hours=24)
        self.results = CPULogs.objects.filter(created__range=(self.earlier,self.now))

    def get_labels(self):
        return list(self.results.values_list('date', flat=True))

    def get_providers(self):
        return ["Usage"]

    def get_data(self):
        self.now = datetime.datetime.now()
        self.earlier = self.now - datetime.timedelta(hours=24)
        self.results = CPULogs.objects.filter(created__range=(self.earlier,self.now))
        CPULogs.objects.filter(created__lte=datetime.date.today()-datetime.timedelta(days=7)).delete()
        return [list(self.results.values_list('usage', flat=True))]


class LineChartRam(BaseLineChartView):
    def __init__(self):
        self.now = datetime.datetime.now()
        self.earlier = self.now - datetime.timedelta(hours=24)
        self.results = RAMLogs.objects.filter(created__range=(self.earlier,self.now))

    def get_labels(self):
        return list(self.results.values_list('date', flat=True))

    def get_providers(self):
        return ["Usage"]

    def get_data(self):
        self.now = datetime.datetime.now()
        self.earlier = self.now - datetime.timedelta(hours=24)
        self.results = RAMLogs.objects.filter(created__range=(self.earlier,self.now))
        RAMLogs.objects.filter(created__lte=datetime.date.today()-datetime.timedelta(days=7)).delete()
        return [list(self.results.values_list('usage', flat=True))]

