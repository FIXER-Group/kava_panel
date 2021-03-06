from django import template
from panel.models import Server_processes,Server_connections, Webs,Users

register = template.Library()

@register.simple_tag
def counts_process():
    return len(Server_processes.get_server_processes())

@register.simple_tag
def count_connections():
    return len(Server_connections.get_server_network_connections())

@register.simple_tag
def counts_webs():
    return len(Webs.nginx_reader())
@register.simple_tag
def counts_users():
    return len(Users.list_of_all_users())

@register.filter 
def get_item(dictionary, key): return dictionary.get(key)