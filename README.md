Project summary
1. Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project, we are building an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for our analytics team to continue finding insights in what songs their users are listening to.

2. File Description 
In this repository, you will see Test.ipynb, create_tables.py, dwh.cfg, etl.py, README.md, sql_queries.py
Test.ipynb: This provides a script that you can use to run this project.
create_tables.py: provides functions that create table in the database.
dwh.cfg: a basic config file, includes all the basic configuration.
etl.py: provides the function that run the query to insert data into the table. 
README.md: a description of this project.
sql_queries.py: all queries that we used for creating, deleting and inserting data into the tables.

3. Project Description
The database we created for this project has 5 tables: 1 fact table and 4 dimension tables
Fact table: 
songplays - records in event data associated with song plays i.e. records with page NextSong, columns have songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
Dimension tables: 
users - users in the app, columns have user_id, first_name, last_name, gender, level
songs - songs in music database, columns have song_id, title, artist_id, year, duration
artists - artists in music database, columns have artist_id, name, location, lattitude, longitude
time - columns have timestamps of records in songplays broken down into specific units, start_time, hour, day, week, month, year, weekday

4. ETL Pipeline 
For the ETL pipeline, there are 3 phrases and 10 steps:
A.Creating and managing a redshift cluster within a script(step 1-7,10).
B.Creating tables by running script(step 8).
C.Executing SQL statements that create the staging tables from S3 and creating analytics tables from these staging tables(step 9).

To start review this project, please open and run Test.ipynb step by step.

A: First, run step 1-7 will create a cluster on AWS and please wait until it is available to run the rest commands. After all tasks are completed, you can run step 10 to delete the cluster.

B: Run step 8 to create tables

C: run step 9 to load the data from staging table to target table
1.By looking into this script, you will see that function load_staging_tables(cur, conn) is loading JSON file in 2 ways, first one is using JSONPATH method and second is using AUTO method.

staging_events_copy = ("""copy staging_events from {}
credentials 'aws_iam_role={}'
region 'us-west-2'
json {};
""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE','ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs from {}
credentials 'aws_iam_role={}'
region 'us-west-2'
json 'auto';
""").format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE','ARN'))

2.function insert_tables(cur, conn) will run each statement in insert_table_queries to load data from staging table to target table.
3.After all above, you can run some analytic queries to check the results.
