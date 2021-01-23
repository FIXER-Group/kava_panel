from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Server_stat, CPULogs, RAMLogs,Server_processes,Server_connections,Server_connection_speed, Webs
from django.contrib import messages
from chartjs.views.lines import BaseLineChartView
import socket
import platform
import requests
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



@login_required(login_url='/')

def index(request):
    if request.method == "POST":
        Server_stat.reboot_system()
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
    if request.method == "POST":
        try:
            Server_processes.kill_server_process(int(request.POST.get('process')))
            messages.info(request, 'process_killed', extra_tags='process_killed')
        except:
            messages.info(request, 'error_killed', extra_tags='error_killed')
    return render(request, 'process.html', {'List': Server_processes.get_server_processes()})

@login_required(login_url='/')
def network(request):
    return render(request, 'network.html', {'List': Server_connections.get_server_network_connections()})

@login_required(login_url='/')
def webs(request):
    return render(request, 'webs.html', {'List_webs': Webs.ngnix_reader()})

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
                  
@login_required(login_url='/')
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

class StatsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'cpu_percent': Server_stat.cpu_percent(),
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
                }
        return Response(content)

class SystemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'name': platform.system(),
                  'release': platform.release(),
                  'version': platform.version(),
                  'architecture': platform.machine(),
                  'hostname': socket.gethostname(),
                  'ipadress': requests.get('https://checkip.amazonaws.com').text.strip(),
                  'processor': platform.processor()}
        return Response(content)

class ProcessListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'List': Server_processes.get_server_processes()}
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            Server_processes.kill_server_process(int(request.data.get("pid")))
            return Response(True, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_202_ACCEPTED)

class NetworkListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'List': Server_connections.get_server_network_connections()}
        return Response(content)

class SystemRebootAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        Server_stat.reboot_system()
        return Response(True, status=status.HTTP_200_OK)


