import sys
import logging
import rds_config
import pymysql

rds_host  = "put your AWS endpoint for the RDS here"
name = rds_config.db_username
password = rds_config.db_password

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, connect_timeout=20)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):
    with conn.cursor() as cur:
        cur.execute("create database RedditWords")
        cur.execute("use RedditWords")
        cur.execute("create table WordFrequency ( Word varchar(255) NOT NULL, Date varchar(255) NOT NULL, Count Int NOT NULL, PRIMARY KEY (Word, Date))")
    conn.commit()
    
    return 'Success'