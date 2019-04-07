#!/bin/bash

stat=`date +'%Y%m%d%H%M%S'`
CWD=`pwd`
timestamp=`date -u +'%Y-%m-%dT%H:%M:%S.%5N'`

# Get VM Hostname
        hostname=`hostname` 2> /dev/null

# System parameters
  # Syatem status UP/DOWN
        status=`uptime | awk '{print $2}'`   
  # No of days from last reboot
        updays=`uptime | awk '{print $3}'`
  # Load on CPU
        cpuload=`top -b -n1 | grep "Cpu(s)" | awk '{print $2 + $4}'`
  # Total Memory
        totalRam=`free -g | awk 'FNR == 2 {print $2}'`
  # Used Memory
        usedRam=`free -g| awk 'FNR == 2 {print $3}'`
  # Disk space
        temp=`df -kh /var`
  # Disk % used
        disk_perc=`echo $temp | awk -F ' ' '{print $12}' | sed 's/.$//'`
  # Disk used
        disk_used=`echo $temp | awk -F ' ' '{print $10}' | sed 's/.$//'`
  # Disk total
        disk_total=`echo $temp | awk -F ' ' '{print $9}' | sed 's/.$//'`
  # Is reboot required
        if [[ -f /var/run/reboot-required ]] 
        then
	        reboot_required=1
        else
	        reboot_required=0
        fi
