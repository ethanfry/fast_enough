#! /home/pi/work/fast_enough/venv_fast_enough/bin/python3

import json
import subprocess

# run() returns a CompletedProcess object if it was successful
# errors in the created process are raised here too
process = subprocess.run(['/usr/local/bin/speedtest','-f', 'json'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

fp = open('/home/pi/work/fast_enough/data.json', 'r')
data = json.load(fp)
data.append(json.loads(output))
fp.close()
fp = open('/home/pi/work/fast_enough/data.json', 'w')
json.dump(data, fp)
print(output)
