from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page 
from django.utils.decorators import method_decorator   
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Server_stat, CPULogs, RAMLogs,Server_processes,Server_connections,Server_connection_speed,Webs,Users
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
        if request.POST.get('change-pass') == "True":
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.info(request, 'password_changed', extra_tags='password_changed')
                return redirect('panel:edit_profile')
        elif request.POST.get('force-logout') == "True":
            user = User.objects.get(username=request.user)
            [s.delete() for s in Session.objects.all() if str(s.get_decoded().get('_auth_user_id')) == str(user.id)]
            messages.info(request, 'Logout_message', extra_tags='logout')
            return redirect('accounts:index')
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
    if request.method == "POST":
        if request.POST.get('del-website') == "true":
            try:
                Webs.delete_site(request.POST.get('path'),request.POST.get('path-d'),True if request.POST.get('del_directory') == "True" else False)
                messages.info(request, 'Site was deleted successfully', extra_tags='webs_info')
            except:
                messages.info(request, 'error_killed', extra_tags='web_error')
        elif request.POST.get('add-website') == "true":
            try:
                Webs.add_site(request.POST.get('domian'))
                messages.info(request, 'Site was added successfully', extra_tags='webs_info')
            except:
                messages.info(request, 'error_killed', extra_tags='web_error')
        else:
            if request.POST.get('active') == "true":
                try:
                    Webs.trun_off(request.POST.get('path'))
                    messages.info(request, 'Site was disabled successfully', extra_tags='webs_info')
                except:
                    messages.info(request, 'error_killed', extra_tags='web_error')
            else:
                try:
                    Webs.trun_on(request.POST.get('path'))
                    messages.info(request, 'Site was enabled successfully', extra_tags='webs_info')
                except:
                    messages.info(request, 'error_killed', extra_tags='web_error')
    return render(request, 'webs.html', {'List_webs': Webs.nginx_reader()})

@login_required(login_url='/')
def webs_edit(request):
    if request.method == "POST":
        if request.POST.get('save-website') == "true":
            try:
                Webs.set_edit_value(request.POST.get('path'),{'server_name': request.POST.get('server_name'),
                                                              'root': request.POST.get('root'),
                                                              'port': request.POST.get('port') })
                messages.info(request, 'Site was updated successfully', extra_tags='webs_info')
            except:
                messages.info(request, 'error_killed', extra_tags='web_error')
        return render(request, 'edit_webs.html', Webs.get_edit_vaule(request.POST.get('path')))
    else:
        return render(request, 'edit_webs_error.html')

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
def users(request):
    if request.method == "POST":
        if request.POST.get('add-user') == "true":
            try:
                Users.create_new_user(request.POST.get('user_name'),request.POST.get('password'),True if request.POST.get('root_privileges') == "True" else False)
                messages.info(request, 'User created successfully', extra_tags='users_info')
            except:
                messages.info(request, 'Error has benn occured', extra_tags='users_error')
        elif request.POST.get('del-user') == "True":
            try:
                Users.delete_user(request.POST.get('name'))
                messages.info(request, 'User deleted successfully', extra_tags='users_info')
            except:
                messages.info(request, 'Error has benn occured', extra_tags='users_error')
    return render(request, 'users.html',{'List':Users.list_of_all_users()})

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


