from django.db import models
import math
import psutil
import cpuinfo
import time
from datetime import datetime
import asyncio
from asgiref.sync import sync_to_async



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
        return "%s %s" % (s, size_name[i])

    def ram_total():
        size_bytes = psutil.virtual_memory().total
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

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
        return "%s %s" % (s, size_name[i])
    def disk_usage():
        size_bytes = psutil.disk_usage('/').used
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

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
        return "%s %s" % (s, size_name[i])

    def uptime_days():
        return (time.time() - psutil.boot_time())//(60*60*24)

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
    logcpu = CPULogs(date = datetime.today().strftime("%d %b %Y %H:%M:%S"))
    logcpu.save()

@sync_to_async
def get_logs_ram():
    logcpu = RAMLogs(date = datetime.today().strftime("%d %b %Y %H:%M:%S"))
    logcpu.save()

async def loop_logs():
    while True:
        await get_logs_cpu()
        await get_logs_ram()
        await asyncio.sleep(60*30)