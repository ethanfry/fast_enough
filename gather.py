#! /home/pi/work/fast_enough/venv_fast_enough/bin/python3

import boto3
import json
import os
import subprocess

from dynamodb_json import json_util


# run() returns a CompletedProcess object if it was successful
# errors in the created process are raised here too
process = subprocess.run(['/usr/local/bin/speedtest','-f', 'json'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

data = None
with open('/home/pi/work/fast_enough/data.json', 'r') as fp:
    data = json.load(fp)
data.append(json.loads(output))
if len(data) > 50:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = None
    with open(os.path.join(dir_path, 'config.json'), 'r') as conf_fp:
        config = json.load(conf_fp)
    client = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id=config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])
    for row in data:
        client.put_item(TableName='fast_enough', Item=json_util.json.loads(json_util.dumps(row)))
    data = []

with open('/home/pi/work/fast_enough/data.json', 'w') as fp:
    json.dump(data, fp)
print(output)
