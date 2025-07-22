#!/bin/bash

echo "+++ Simple System Check +++"
echo "Date: $(date)"
echo

echo "Disk Usage:"
df -h /

echo
echo "Memory Usage:"
free -h

echo
echo "Current User:"
whoami

echo
echo "System Uptime:"
uptime

echo "+++ Check Complete +++"
