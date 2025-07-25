#!/bin/bash

# Log file location
LOG_FILE="$HOME/system_health.log"

echo "+++ Simple System Check +++" >> $LOG_FILE
echo "Date: $(date)" >> $LOG_FILE
echo >> $LOG_FILE

echo "Disk Usage:" >> $LOG_FILE
df -h / >> $LOG_FILE

echo >> $LOG_FILE
echo "Memory Usage:" >> $LOG_FILE
free -h >> $LOG_FILE

echo >> $LOG_FILE
echo "Current User:" >> $LOG_FILE
whoami >> $LOG_FILE

echo >> $LOG_FILE
echo "System Uptime:" >> $LOG_FILE
uptime >> $LOG_FILE

echo "+++ Check Complete +++" >> $LOG_FILE
echo >> $LOG_FILE
