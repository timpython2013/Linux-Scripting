#!/usr/bin/env python3
"""
System Health Log Parser
Converts system_health.log to CSV format for analysis and dashboard preparation
"""

import re
import csv
import sys
from datetime import datetime
from pathlib import Path

def parse_log_file(log_file_path):
    """Parse the system health log and extract structured data"""
    
    if not Path(log_file_path).exists():
        print(f"Error: Log file {log_file_path} not found!")
        return []
    
    records = []
    current_record = {}
    
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for start of new health check
        if line.startswith("+++ Simple System Check +++"):
            current_record = {}
            i += 1
            continue
            
        # Parse date
        if line.startswith("Date:"):
            date_str = line.replace("Date: ", "").strip()
            try:
                # Parse the date format from your script
                current_record['timestamp'] = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Z %Y")
                current_record['date'] = current_record['timestamp'].strftime("%Y-%m-%d")
            except ValueError:
                # Fallback for different date formats
                current_record['timestamp'] = date_str
                current_record['date'] = date_str
        
        # Parse disk usage
        elif line.startswith("Disk Usage:"):
            i += 1  # Move to next line with actual data
            if i < len(lines):
                i += 1 # Skip "Filesystem Size Used..." header line
                if i < len(lines):
               	    disk_line = lines[i].strip()
                # Example: "/dev/sda1       20G  8.5G   11G  45% /"
                    disk_match = re.search(r'(\d+)%', disk_line)
                    if disk_match:
                        current_record['disk_usage_percent'] = int(disk_match.group(1))
                
                # Extract disk space info
                    parts = disk_line.split()
                    if len(parts) >= 5:
                        current_record['disk_total'] = parts[1]
                        current_record['disk_used'] = parts[2]
                        current_record['disk_available'] = parts[3]
        
        # Parse memory usage
        elif line.startswith("Memory Usage:"):
            i += 1  # Move to next line with actual data
            if i < len(lines):
                i += 1 # Move to "Mem:" data line
                if i < len(lines):
                    mem_line = lines[i].strip()
                    # Example: "Mem:           7.6Gi       2.1Gi       3.2Gi       0.0Ki       2.3Gi       5.2Gi"
                    mem_parts = mem_line.split()
                    if len(mem_parts) >= 3 and mem_parts[0] == "Mem:":
                        current_record['memory_total'] = mem_parts[1]
                        current_record['memory_used'] = mem_parts[2]
                        current_record['memory_available'] = mem_parts[6] if len(mem_parts) > 3 else ""
                    
                    # Calculate memory percentage if possible
                    try:
                        total_val = float(re.sub(r'[A-Za-z]', '', mem_parts[1]))
                        used_val = float(re.sub(r'[A-Za-z]', '', mem_parts[2]))
                        if total_val > 0:
                            current_record['memory_usage_percent'] = round((used_val / total_val) * 100, 1)
                    except:
                        current_record['memory_usage_percent'] = 0
        
        # Parse current user
        elif line.startswith("Current User:"):
            i += 1
            if i < len(lines):
                current_record['user'] = lines[i].strip()
        
        # Parse uptime
        elif line.startswith("System Uptime:"):
            i += 1
            if i < len(lines):
                uptime_line = lines[i].strip()
                current_record['uptime'] = uptime_line
                
                # Extract load average if present
                load_match = re.search(r'load average: ([\d.]+)', uptime_line)
                if load_match:
                    current_record['load_average'] = float(load_match.group(1))
        
        # Check for end of record
        elif line.startswith("+++ Check Complete +++"):
            if current_record:  # Only add if we have data
                records.append(current_record.copy())
                current_record = {}
        
        i += 1
    
    return records

def write_csv(records, output_file):
    """Write parsed records to CSV file"""
    
    if not records:
        print("No records to write!")
        return
    
    # Define CSV columns
    fieldnames = [
        'date', 'timestamp',
        'disk_usage_percent', 'disk_total', 'disk_used', 'disk_available',
        'memory_usage_percent', 'memory_total', 'memory_used', 'memory_available',
        'user', 'uptime', 'load_average'
    ]
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for record in records:
            # Fill in missing fields with empty strings
            row = {field: record.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"Successfully wrote {len(records)} records to {output_file}")

def main():
    """Main function"""
    
    # Default paths
    log_file = "/home/shlimmy/system_health.log"
    csv_file = "/home/shlimmy/system_health_data.csv"
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    if len(sys.argv) > 2:
        csv_file = sys.argv[2]
    
    print(f"Parsing log file: {log_file}")
    print(f"Output CSV file: {csv_file}")
    
    # Parse the log file
    records = parse_log_file(log_file)
    
    if records:
        # Write to CSV
        write_csv(records, csv_file)
        
        # Show summary
        print(f"\nSummary:")
        print(f"- Total records: {len(records)}")
        if records:
            print(f"- Date range: {records[0].get('date', 'Unknown')} to {records[-1].get('date', 'Unknown')}")
            print(f"- Latest disk usage: {records[-1].get('disk_usage_percent', 'Unknown')}%")
            print(f"- Latest memory usage: {records[-1].get('memory_usage_percent', 'Unknown')}%")
        
        print(f"\nYou can now:")
        print(f"1. Open {csv_file} in Excel/Google Sheets")
        print(f"2. Use this data for the web dashboard")
        print(f"3. Run analysis with pandas/matplotlib")
        
    else:
        print("No records found in log file!")

if __name__ == "__main__":
    main()
