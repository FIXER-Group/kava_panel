from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Server_stat
from django.contrib import messages
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import socket
import platform
import requests

@login_required(login_url='/')

def index(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logout_message', extra_tags='logout')
    return redirect('accounts:index')

@login_required(login_url='/')
def process(request):
    return render(request, 'process.html')


@login_required(login_url='/')
def graphs(request):
    return render(request, 'graphs.html')

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
                'uptime': Server_stat.uptime_days()}
     return JsonResponse(results)


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Usage"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [[75, 44, 92, 11, 44, 95, 35]]
    