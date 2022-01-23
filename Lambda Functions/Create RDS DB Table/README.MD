# Create RDS DB Table
This folder contains a Lambda function that when run connects to a MySQL database hosted on AWS and creates a table in it. If you are adding this to your own AWS account you need to include the rds_config file with the correct credentials as well as the pymysql folder as it does not come with the EC2 python environment that Lambda functions are run on.
