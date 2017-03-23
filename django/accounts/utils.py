from django.conf import settings

from ipaddress import ip_address, ip_network


def passless_login_allowed(ip):
    ip = ip_address(ip)
    passless_ip_networks = getattr(settings, 'PASSLESS_IP_NETWORKS', [])
    for network in passless_ip_networks:
        if ip in ip_network(network):
            return True
    return False
