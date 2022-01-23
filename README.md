# Reddit Word Tracker
This project is a data pipeline built in AWS which analyzes the frequency of all words used on specific subreddits, in my case financial subreddits and stores them in a database which can be easily queried to determine which words are being used frequently on specific days and over time
  
  
# The Architecture
![Architecture Design](Architecture.png)
A lambda function trigered by a daily time based cloudwatch event is used to retrieve data from Reddit's public API and to write the retrieved data an S3 bucket to await processing.
