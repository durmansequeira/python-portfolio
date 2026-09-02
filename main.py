import subprocess
import csv
#List of hosts to ping

devices = [
    {
        "name": "R1",
        "ip": "127.0.0.1"
    },
    {
        "name": "R2",
        "ip": "8.8.8.8"
    },
    {
        "name": "SW1",
        "ip": "192.0.2.1"
    }
]

#definition of the ping_host function
      
def ping_host(target):
        try:
            result = subprocess.run(
                ["ping", target],
                capture_output=True,
                text=True,
                timeout=10
                
             )
            
            #Check wether hostname could be resolved or not
            if "could not find host" in result.stdout.lower():
                return "Host_not_found",None, None
           
            packet_loss = None
            average_latency = None
        
            for line in result.stdout.splitlines():
             if "Lost =" in line:
                parts = line.split()
                packet_loss = int(parts[10].strip('(%'))
             if "Average =" in line:
                parts = line.split()
                average_latency = int(parts[-1].replace("ms", ""))
            
            
            return result.returncode, packet_loss, average_latency

        except subprocess.TimeoutExpired:
         return "TIMEOUT", None, None
     
# assess network health

def assess_health(packet_loss, average_latency):
        if packet_loss ==0  and average_latency <100:
            return "Healthy"
        elif packet_loss <50 and average_latency <200:
            return "Warning"
        else:
            return "Critical"
    
#store dignostic results
    
results = []    

#Check every device 
       
for device in devices:
    print (f"\nChecking {device['name']}({device['ip']})")
    status, packet_loss, average_latency = ping_host(device['ip'])
    
    if status == "Host_not_found":
        print(f"{device['name']} could not be resolved.")
        results.append({
            "name": device['name'],
            "ip": device['ip'],
            "status": "Host_not_found",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })
    elif status == "TIMEOUT":
        print(f"Requested timed out.")
        results.append({
            "name": device['name'],
            "ip": device['ip'],
            "status": "TIMEOUT",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })
    elif status == 0:
        health = assess_health(packet_loss, average_latency)
        
        print (f"{device['name']} is UP")
        print(f"Packet loss: {packet_loss}%")
        print(f"Average latency: {average_latency} ms")
        print (f"Health status: {health}")
        results.append({
            "name": device['name'],
            "ip": device['ip'],
            "status": "UP",
            "packet_loss": packet_loss,
            "average_latency": average_latency,
            "health": health
        })
    else:
        print(f"{device['name']} is DOWN")
        results.append({
            "name": device['name'],
            "ip": device['ip'],
            "status": "DOWN",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })
        
#Display stored results
print("\n" + "=" * 70)
print("NOC NETWORK REPORT")
print("=" * 70)

for result in results:

    print(
        f"{result['name']:<8}"
        f"{result['ip']:<16}"
        f"{result['status']:<15}"
        f"{str(result['packet_loss']):<12}"
        f"{str(result['average_latency']):<12}"
        f"{str(result['health']):<10}"
    )
    
# Save results to CSV
with open("network_report.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "name",
            "ip",
            "status",
            "packet_loss",
            "average_latency",
            "health"
        ]
    )

    writer.writeheader()
    writer.writerows(results)

print("\nReport saved to network_report.csv")

print("=" * 70)    