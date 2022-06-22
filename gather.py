#! /home/pi/work/fast_enough/venv_fast_enough/bin/python3

import boto3
import json
import os
import subprocess
import time

from dynamodb_json import json_util

# The directory we're located in
dir_path = os.path.dirname(os.path.realpath(__file__))

# Get our configuration
config = None
with open(os.path.join(dir_path, 'config.json'), 'r') as conf_fp:
    config = json.load(conf_fp)

while True:
    # run() returns a CompletedProcess object if it was successful
    # errors in the created process are raised here too
    process = subprocess.run(['/usr/local/bin/speedtest','-f', 'json'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout


    # Check our local data cache. If there are too many entries, send them up to AWS
    data = None
    with open(os.path.join(dir_path, 'data.json'), 'r') as fp:
        data = json.load(fp)
    data.append(json.loads(output))
    if len(data) > config['LOCAL_CACHE_LIMIT']:  
        client = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id=config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])
        for row in data:
            client.put_item(TableName='fast_enough', Item=json_util.json.loads(json_util.dumps(row)))
        data = []
    
    with open(os.path.join(dir_path, 'data.json'), 'w') as fp:
        json.dump(data, fp)
    print(output)
    time.sleep(config['PERIOD_IN_SECONDS'])
