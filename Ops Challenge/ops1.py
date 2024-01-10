import time
from ping3 import ping

# Transmit a single ICMP (ping) packet to a specific IP every two seconds
# Target address
destination_ip = "192.168.1.1"
# Number of seconds
interval = 2

# Only run while True meaning forever
while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    response = ping(destination_ip)
    # Set the value of success while not NULL
    success = response is not None
    # Evaluate the response as either success or failure
    # Assign success or failure to a status variable
    status = "Success" if success else "Failure"
    # For every ICMP transmission attempted, print the status variable along 
    # with a comprehensive timestamp and destination IP tested
    print(f"{timestamp} - Destination: {destination_ip} - Status: {status}")

    time.sleep(interval)