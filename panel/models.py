from django.db import models
import psutil
import cpuinfo


class Server_stat(models.Model):
    def cpu_percent(percore=False):
        return psutil.cpu_percent(interval=1, percpu=percore)

    def cpu_name():
        return cpuinfo.get_cpu_info()['brand_raw']


