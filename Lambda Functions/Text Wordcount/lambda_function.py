import boto3
import csv
from datetime import date

client = boto3.client('s3')

def lambda_handler(event, context):
    
    read_bucket = 'reddit-text'
    write_bucket = 'processed-reddit-wordcount'
    
    fileName_read = 'reddit posts '+str(date.today())+'.txt'
    fileName_write = 'reddit posts wordcount '+str(date.today())+'.csv'

    response1 = client.get_object(Bucket=read_bucket, Key=fileName_read)
    response1_data = response1['Body'].read()
    
    with open('/tmp/test.txt', 'w', encoding='utf-8') as t:
        t.write(response1_data.decode('utf-8'))
    
    totals = {}
    punctuation = [',', '.', '?', ';', ':', '!', '/', '*', '$', '(', ')', '=', '+', '-', '_', '|']

    with open('/tmp/test.txt', 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for l in lines:
            l.encode('ascii', 'replace').decode()
            l = l.upper()
            l = l.replace('"', " ")
            for cha in punctuation:
                l = l.replace(cha, ' ')
            words = l.split()
            for w in words:
                w.upper()
                if w in totals:
                    totals[w] += 1
                else:
                    totals[w] = 1
                    
    with open('/tmp/test.csv', 'w', encoding='utf-8', newline='') as c:
        writer = csv.writer(c, delimiter=',')
        for key, value in totals.items():
            writer.writerow([key, value])
    
    data = open('/tmp/test.csv', 'rb')

    response2 = client.put_object(Bucket=write_bucket, Key=fileName_write, Body=data)