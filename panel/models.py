from django.db import models
import math
import psutil
import cpuinfo
import time
import socket
import threading
import platform
import subprocess
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from datetime import datetime
import asyncio
from asgiref.sync import sync_to_async
import glob
import os



class Webs(models.Model):
    def ngnix_reader():
        path = '/etc/nginx/sites-available' #for test only
        webs_list = list()
        for filepath in glob.glob(os.path.join(path, '*')):
            with open(filepath) as f:
                domians = ""
                cur_path =" s"
                content = f.read()
                for line in content.splitlines():
                    if 'server_name' in line:
                        domians = line.split('server_name ',1)[1][:-1]
                    if 'root' in line:
                        cur_path = line.split('root ',1)[1][:-1]
                    if domians != "" and cur_path != "":
                        ngnixDict = {
                            "domian": domians,
                            "path": cur_path
                            }
                        webs_list.append(ngnixDict)
                        break
        return webs_list
                



class Server_stat(models.Model):
    def cpu_percent(percore=False):
        return psutil.cpu_percent(interval=1, percpu=percore)

    def cpu_name():
        return cpuinfo.get_cpu_info()['brand_raw']
    
    def ram_percent():
        return psutil.virtual_memory().percent
    def ram_used():
        size_bytes = psutil.virtual_memory().used
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def ram_total():
        size_bytes = psutil.virtual_memory().total
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def disk_percent():
        return psutil.disk_usage('/').percent

    def disk_total():
        size_bytes = psutil.disk_usage('/').total
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    def disk_usage():
        size_bytes = psutil.disk_usage('/').used
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def swap_percent():
        return psutil.swap_memory().percent

    def swap_total():
        size_bytes = psutil.swap_memory().total
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def uptime_days():
        return (time.time() - psutil.boot_time())//(60*60*24)
    def reboot_system():
        if platform.system() == 'Windows':
            subprocess.call(["shutdown", "/r"])
        elif platform.system() == 'Linux':
            subprocess.run(["sudo", "shutdown", "-r", "+1"])

class Server_processes(models.Model):
    def get_server_processes():
        listOfProcessNames = list()
        for proc in psutil.process_iter():
            pInfoDict = proc.as_dict(attrs=['cpu_percent', 'pid', 'name', 'memory_percent'])
            orderedDict = {
                "pid": pInfoDict['pid'],
                "name": pInfoDict['name'],
                "cpu_percent": round(pInfoDict['cpu_percent']/10,2),
                "memory_percent": round(pInfoDict['memory_percent'], 2)
            }
            listOfProcessNames.append(orderedDict)
        return sorted(listOfProcessNames, key=lambda k: k['cpu_percent'], reverse=True)
    def kill_server_process(pid):
        p = psutil.Process(pid)
        p.terminate()

class Server_connections(models.Model):
    def get_server_network_connections():
        AD = "-"
        AF_INET6 = getattr(socket, 'AF_INET6', object())
        proto_map = {
            (AF_INET, SOCK_STREAM): 'tcp',
            (AF_INET6, SOCK_STREAM): 'tcp6',
            (AF_INET, SOCK_DGRAM): 'udp',
            (AF_INET6, SOCK_DGRAM): 'udp6',
        }
        proc_names = {}
        listofnetworkconnections=[]
        for p in psutil.process_iter(['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']
        for c in psutil.net_connections(kind='inet'):
            laddr = "%s:%s" % c.laddr
            raddr = ""
            if c.raddr:
                raddr = "%s:%s" % c.raddr
            name = proc_names.get(c.pid, '?') or ''
            dictionary={
                "Protocol": proto_map[(c.family, c.type)],
                "Local_address": laddr,
                "Remote_address": raddr or AD,
                "Status:": c.status,
                "PID": c.pid or AD,
                "Name": name,
                }
            listofnetworkconnections.append(dictionary)
        return listofnetworkconnections

class Server_connection_speed(models.Model):
    def network_usage():
        upload = psutil.net_io_counters()[0]
        download = psutil.net_io_counters()[1]
        threading.Event().wait(1)
        upload2 = psutil.net_io_counters()[0]
        download2 = psutil.net_io_counters()[1]
        size_bytes = (upload2 - upload)
        size_bytes2 = (download2 - download)
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        if size_bytes == 0:
            upload_return = "0B"
        else:
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            upload_return = f"{s} {size_name[i]}"
        if size_bytes2 == 0:
            download_return = "0B"
        else:
            i = int(math.floor(math.log(size_bytes2, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes2 / p, 2)
            download_return = f"{s} {size_name[i]}"
        return upload_return, download_return

def get_server_processes_number():
    return len(Server_processes.get_server_processes())



class CPULogs(models.Model):
    created = models.DateField(auto_now_add=True)
    date = models.CharField(max_length=30)
    usage = models.FloatField(default=Server_stat.cpu_percent)


class RAMLogs(models.Model):
    created = models.DateField(auto_now_add=True)
    date = models.CharField(max_length=30, default=datetime.today().strftime("%d %b %Y %H:%M:%S"))
    usage = models.FloatField(default=Server_stat.ram_percent)

@sync_to_async
def get_logs_cpu():
    logcpu = CPULogs(date=datetime.today().strftime("%d %b %Y %H:%M:%S"))
    logcpu.save()

@sync_to_async
def get_logs_ram():
    logram = RAMLogs(date=datetime.today().strftime("%d %b %Y %H:%M:%S"))
    logram.save()

class AutoLogs(models.Model):
    async def loop_logs():
        while True:
            await get_logs_cpu()
            await get_logs_ram()
            await asyncio.sleep(60*30)





