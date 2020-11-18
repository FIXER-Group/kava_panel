from django.db import models
import psutil


class Server_stat(models.Model):
    def cpu_percent(percore=False):
        return psutil.cpu_percent(interval=1, percpu=percore)

