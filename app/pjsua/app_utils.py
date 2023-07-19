from pjsua2 import IpChangeParam, Endpoint_instance
from pjsua2exceptions import pjsua2Exception
from utils.utility import print_pad


def handle_network_change():
    try:
        network_change = IpChangeParam()
        print_pad(network_change)
        Endpoint_instance().handleIpChange(network_change)
    except pjsua2Exception as pjsua2_exception:
        print_pad(pjsua2_exception.args)
