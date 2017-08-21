#!/bin/bash
# author: zhxfei


LINK_PEER=$(uptime|awk -F',' '{print $1}'|awk -F'up' '{print $2}'|sed 's/ //'|awk '{print $1}')
HOST_NAME=$(hostname)
ts=`date +%s`;

curl -X POST -d "[{\"metric\": \"sys.uptime\", \"endpoint\": \"${HOST_NAME}\", \"timestamp\": $ts,\"step\": 60,\"value\": ${LINK_PEER},\"counterType\": \"GAUGE\",\"tags\": \"owner=zhxfei\"}]" http://127.0.0.1:1988/v1/push
# echo "[{\"metric\": \"net.link.ss_links\", \"endpoint\": \"hk.zhxfei.com\", \"timestamp\": $ts,\"step\": 60,\"value\": ${LINK_PEER},\"counterType\": \"GAUGE\",\"tags\": \"idc=hk,project=shadowsocks\"}]" 
