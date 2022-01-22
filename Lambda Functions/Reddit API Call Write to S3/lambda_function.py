import urllib3

import boto3
import json
from datetime import date

client = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket = 'reddit-text'

    subreddit_list = ['wallstreetbets', 'investing', 'stocks']
    limit = 100
    timeframe = 'day'
    for j in subreddit_list:
        base_url = 'https://www.reddit.com/r/'+j+'/top.json?limit='+str(limit)+'&t='+timeframe+'&restrict_sr=on'
        http = urllib3.PoolManager()
        request = http.request('GET', base_url, headers={'User-agent': 'yourbot'})
        r = json.loads(request.data)
        for post in r['data']['children']:
            data_file = open('/tmp/test.txt', 'a', encoding='utf-8')
            data_file.write(post['data']['title'])
            data_file.write('\n')

    fileName = 'reddit posts '+str(date.today())+'.txt'
    
    f = open('/tmp/test.txt', 'r', encoding='utf-8')
    contents = f.read()
    f.close()

    response = client.put_object(Bucket=bucket, Key=fileName, Body=contents)