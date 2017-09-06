#!/usr/bin/python
#!-*- coding:utf8 -*-

import requests
import time
import json
import os

# status_counter means : http://tengine.taobao.org/document_cn/http_reqstat_cn.html
status_counter = {
    'kv': 'www.zhxfei.com',
    'bytes_in': 0,
    'bytes_out': 0,
    'conn_total': 0,
    'req_total': 0,
    'http_2xx': 0,
    'http_3xx': 0,
    'http_4xx': 0,
    'http_5xx': 0,
    'http_other_status': 0,
    'rt': 0,
    'ups_req': 0,
    'ups_rt': 0,
    'ups_tries': 0,
    'http_200': 0,
    'http_206': 0,
    'http_302': 0,
    'http_304': 0,
    'http_403': 0,
    'http_404': 0,
    'http_416': 0,
    'http_499': 0,
    'http_500': 0,
    'http_502': 0,
    'http_503': 0,
    'http_504':0,
    'http_508': 0,
    'http_other_detail_status': 0,
    'http_ups_4xx': 0,
    'http_ups_5xx': 0
}


def proc_status(lines):
    status = [
        'bytes_in',
        'bytes_out',
        'conn_total',
        'req_total',
        'http_2xx',
        'http_3xx',
        'http_4xx',
        'http_5xx',
        'http_other_status',
        'rt',
        'ups_req',
        'ups_rt',
        'ups_tries',
        'http_200',
        'http_206',
        'http_302',
        'http_304',
        'http_403',
        'http_404',
        'http_416',
        'http_499',
        'http_500',
        'http_502',
        'http_503',
        'http_504',
        'http_508',
        'http_other_detail_status',
        'http_ups_4xx',
        'http_ups_5xx'
    ]
    res_dict_lst = [dict(zip(status, line.split(','))) for line in lines]
    for res_dict in res_dict_lst:
        dict_key_value_sum(res_dict)


def dict_key_value_sum(res_dict):
    global status_counter
    for k, v in res_dict.items():
        status_counter[k] += int(v)


def get_info():
    req_headers = {
        'user-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1b2) Gecko/20060823 SeaMonkey/1.1',
        'Host': 'zhxfei.com',
        }
    res = requests.get("http://localhost/monitor/nginx_status",
                        headers=req_headers)
    if res.status_code == 200:
        info_lines = [','.join(line.split(',')[2:]) for line in res.text.split('\n') if 'zhxfei' in line and
                                    line.split(',')[1] == '10.144.89.245:80']
        return info_lines


def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'

def get_ip_port():
    command_ip = "ip addr show eth0|grep 'inet '| awk '{print $2}'"
    res_ip_addr = os.popen(command_ip).read().strip()
    return {
        'ip': res_ip_addr,
        'port': 80
        }

def main():
    res = get_info()
    if res:
        ts = int(time.time())
        payload_lst = []
        proc_status(res)
        #print status_counter
        for k, v in status_counter.items():
            payload = {
                "endpoint": get_hostname(),
                "metric": k,
                "timestamp": ts,
                "step": 60,
                "value": v,
                "counterType": "COUNTER",
                "tags": "ip={ip} port={port}".format(**get_ip_port())
            }
            payload_lst.append(payload)
        return payload_lst

payload = main()

r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))

print r.text

