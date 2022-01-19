#!/bin/bash

logDir="/data/comlogs"

mkdir -p ${logDir}

while true; do
  for port in $(cat "${HOME}/.comlog"); do
    if [[ -c ${port} ]]; then
      if [[ ! $(ps aux | grep -v grep | grep "cat ${port}") ]]; then 
        deviceName=$(basename ${port})
        datetime=$(date '+%y%m%d%H%M%S')
        logFile="${deviceName}_${datetime}.log"
        cat ${port} > ${logDir}/${logFile} &
      fi
    fi
  done
done

