from rest_framework.test import APITestCase, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
import platform,subprocess
class Kava_PanelTests(APITestCase):
    def setUp(self):
        self.username = 'andrew'
        self.password = 'smith'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)
    def test_get_serverstats(self):
        response =  self.client.get('/panel/api/stats', {"cpu_percent":6.7,"cpu_per_core":[20.4,3.0,3.2,0.0,4.2,4.0],"cpu_name":"QEMU Virtual CPU version 2.5+","ram_percent":25.5,"ram_total":"31.37 GB","ram_usage":"7.71 GB","disk_percent":18.0,"disk_total":"182.03 GB","disk_usage":"32.68 GB","swap_percent":0.0,"swap_total":"4.0 GB","uptime":33.0}, format='json')
        return response
    def test_get_system(self):
        response =  self.client.get('/panel/api/system', {"name":"Linux","release":"5.4.0-1028-kvm","version":"#29-Ubuntu SMP Thu Nov 26 06:52:24 UTC 2020","architecture":"x86_64","hostname":"androjus","ipadress":"x.x.x.x","processor":"x86_64"}, format='json')
        return response
    def test_get_proceses(self):
        response =  self.client.get('/panel/api/process', {"List":[{"pid":5899,"name":"java","cpu_percent":3.32,"memory_percent":15.36},{"pid":1665,"name":"java","cpu_percent":0.81,"memory_percent":8.14}]}, format='json')
        return response
    def test_post_proces_kill(self):
        response =  self.client.post("/panel/api/process -d 'pid=2137'", 'false', format='json')
        return response
    def test_post_reboot(self):
        response =  self.client.post("/panel/api/reboot", 'true', format='json')
        if platform.system() == 'Windows':
            subprocess.call(["shutdown", "-a"])
        elif platform.system() == 'Linux':
            subprocess.run(["sudo", "shutdown", "-c"])
        return response