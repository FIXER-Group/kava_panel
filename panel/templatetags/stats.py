from django import template
from panel.models import Server_processes

register = template.Library()

@register.simple_tag
def counts_process():
    return len(Server_processes.get_server_processes())