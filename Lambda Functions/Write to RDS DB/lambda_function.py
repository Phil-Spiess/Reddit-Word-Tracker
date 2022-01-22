import sys
import logging
import rds_config
import pymysql
import boto3
import io
from datetime import date
import codecs

def lambda_handler(event, context):
    
    rds_host  = "put your AWS endpoint for the RDS here"
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=20)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    
    client = boto3.client('s3')

    key = 'reddit posts wordcount '+str(date.today())+'.csv'
    bucket = 'processed-reddit-wordcount'
    
    data_dict = {}
    
    data = client.get_object(Bucket=bucket, Key=key)
    
    logger.info("SUCCESS: Got data from s3")
    
    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"]), fieldnames=('words', 'counts')):
        data_dict[row['words']] = row['counts']

    logger.info("SUCCESS: Stored data in dict")

    with conn.cursor() as cur:
        for key, value in data_dict:
            sql = 'insert into WordFrequency (Word, Date, Count) VALUES (%s %s %s)'
            cur.execute(sql, (key, str(date.today()), value))       
    conn.commit()
    
    return 'Success'



