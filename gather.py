import json
import subprocess

# run() returns a CompletedProcess object if it was successful
# errors in the created process are raised here too
process = subprocess.run(['/usr/local/bin/speedtest','-f', 'json'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

fp = open('data.json', 'r')
data = json.load(fp)
data.append(json.loads(output))
fp.close()
fp = open('data.json', 'w')
json.dump(data, fp)
print(output)