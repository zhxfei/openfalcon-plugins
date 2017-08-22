#!/bin/bash
# author: zhxfei


LINK_PEER=$(ss -antp|grep "^ESTAB.*1003"|wc -l)

ts=`date +%s`;

curl -X POST -d "[{\"metric\": \"net.link.ss_links_for_taolei\", \"endpoint\": \"hk.zhxfei.com\", \"timestamp\": $ts,\"step\": 60,\"value\": ${LINK_PEER},\"counterType\": \"GAUGE\",\"tags\": \"idc=hk,project=shadowsocks\"}]" http://127.0.0.1:1988/v1/push
# echo "[{\"metric\": \"net.link.ss_links\", \"endpoint\": \"hk.zhxfei.com\", \"timestamp\": $ts,\"step\": 60,\"value\": ${LINK_PEER},\"counterType\": \"GAUGE\",\"tags\": \"idc=hk,project=shadowsocks\"}]" 
