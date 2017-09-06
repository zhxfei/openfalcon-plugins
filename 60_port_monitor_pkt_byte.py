#!/usr/bin/python
# coding: utf-8
import sys
import os
import time
import requests
import json
import re

ts = int(time.time())
payload_lst = []


def get_mon_by_port(port):
    command = ''' iptables -L -n -v -x| grep {}'''
    res = os.popen(command.format(port)).read().strip()
    if res:
        pkt, byte = map(int, re.split('\s+', res)[:2])
        return {
            'packet-received': pkt,
            'byte-received': byte
        }


def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'


def get_send_json(port, user):
    info_dict = get_mon_by_port(port)
    for k, v in info_dict.items():
        payload = {
                "endpoint": get_hostname(),
                "metric": k,
                "timestamp": ts,
                "step": 60,
                "value": v,
                "counterType": "COUNTER",
                "tags": "port={port} user={user}".format(port=port, user=user)
            }
        #print payload
        payload_lst.append(payload)


def main():
    monitor_port_user = {
        1001: u'small partner',
        1002: 'own',
        1003: 'taolei'
    }

    for port, user in monitor_port_user.items():
        get_send_json(port, user)

    print payload_lst

main()
#print payload_lst
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_lst))
print r.text

