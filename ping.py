import subprocess
import re



def get_ping_output(host, ping_count):
    # Run the ping command and capture the output
    ping_output = subprocess.check_output(["ping", "-c", str(ping_count), host])
    return ping_output



def extract_ping_round_trip(ping_output):
    # Extract the average ping time from the output
    ping_lines = ping_output.decode("utf-8").split("\n")
    for line in ping_lines:
        if "round-trip" in line:
            ping_time = (line.split()[-2])
            break
    return ping_time


def calculate_jitter(ping_output):
    # Get the output of the ping command
    output = ping_output.decode('utf-8')

    # Extract the round-trip time (RTT) values from the output
    rtt_values = re.findall(r"time=([\d\.]+) ms", output)

    # Calculate the differences between each pair of RTT values
    differences = [abs(float(rtt_values[i+1]) - float(rtt_values[i])) for i in range(len(rtt_values)-1)]

    # Calculate the average difference (jitter)
    # By dividing the average difference by 2, we get a measure of the deviation in the RTT, 
    # which is commonly referred to as the jitter. Dividing by 2 assumes that the delay variation is symmetric, 
    # meaning that the difference in delay in both directions is roughly the same. 
    jitter = (sum(differences) / len(differences)) /2

    return jitter



 
# Define the number of times to ping the server
ping_count = 5

# Define the regions to ping
regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "ap-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "sa-east-1"
]

pings_info = {}
for region in regions:
    host = "gamelift.%s.amazonaws.com" % region
    ping_output = get_ping_output(host=host, ping_count=ping_count)
    pings_info[region]={
            "jitter": calculate_jitter(ping_output),
            "time": extract_ping_round_trip(ping_output)
            }


sorted_data = sorted(pings_info.items(), key=lambda x: x[1]['jitter'])
for region, stats in sorted_data:
    print(f"{region} has a jitter of {stats['jitter']} and an age of {stats['time']}.")

