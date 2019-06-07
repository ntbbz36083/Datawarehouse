import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""create table if not exists staging_events (
artist VARCHAR(300), 
auth VARCHAR(300), 
firstName VARCHAR(300), 
gender VARCHAR(300), 
itemInSession INTEGER, 
lastName VARCHAR(300), 
length DOUBLE PRECISION, 
level VARCHAR(300), 
location VARCHAR(300), 
method VARCHAR(300),
page VARCHAR(300), 
registration VARCHAR(300), 
sessionId INTEGER, 
song VARCHAR(300), 
status VARCHAR(300), 
ts VARCHAR(300), 
userAgent VARCHAR(300), 
userId INTEGER
);
""")

staging_songs_table_create = ("""create table if not exists staging_songs (
num_songs INTEGER,
artist_id VARCHAR(300),
artist_latitude FLOAT,
artist_longitude FLOAT,
artist_location VARCHAR(300),
artist_name VARCHAR(300),
song_id VARCHAR(300),
title VARCHAR(300),
duration FLOAT,
year INTEGER);
""")

songplay_table_create = ("""create table if not exists songplays (
songplay_id INTEGER IDENTITY(0, 1) PRIMARY KEY, 
start_time TIMESTAMP NOT NULL, 
user_id INTEGER NOT NULL, 
level VARCHAR(300), 
song_id VARCHAR(300), 
artist_id VARCHAR(300), 
session_id INTEGER, 
location VARCHAR(300), 
user_agent VARCHAR(300),
artist_name VARCHAR(300),
song_name VARCHAR(300) NOT NULL,
duration DOUBLE PRECISION NOT NULL
);
""")

user_table_create = ("""create table if not exists users (
user_id INTEGER PRIMARY KEY, 
first_name VARCHAR(300) NOT NULL, 
last_name VARCHAR(300), 
gender VARCHAR(300), 
level VARCHAR(300));
""")

song_table_create = ("""create table if not exists song (
song_id VARCHAR(300) PRIMARY KEY, 
song_name VARCHAR(300), 
artist_id VARCHAR(300) NOT NULL, 
year INTEGER NOT NULL, 
duration DOUBLE PRECISION);
""")

artist_table_create = ("""create table if not exists artist (
artist_id VARCHAR(300) PRIMARY KEY, 
artist_name VARCHAR(300), 
location VARCHAR(300), 
lattitude VARCHAR(300), 
longitude VARCHAR(300));
""")

time_table_create = ("""create table if not exists time (
start_time TIMESTAMP PRIMARY KEY, 
hour INTEGER NOT NULL, 
day INTEGER NOT NULL, 
week INTEGER NOT NULL, 
month INTEGER NOT NULL, 
year INTEGER NOT NULL, 
weekday INTEGER NOT NULL);
""")

# STAGING TABLES

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

# FINAL TABLES

songplay_table_insert = ("""insert into songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent, artist_name, song_name, duration) 
select timestamp 'epoch' + cast(ts as numeric) / 1000  * interval '1 second' as start_time, userId, level,
song_id, artist_id, sessionId, location, userAgent, artist, song, length from staging_events left join staging_songs on staging_events.artist= staging_songs.artist_name and staging_events.song= staging_songs.title and staging_events.length= staging_songs.duration where staging_events.page = 'NextSong'
""")

user_table_insert = ("""insert into users(user_id,first_name, last_name, gender,level) select userid, firstname, lastname, gender, level from staging_events where page = 'NextSong'
""")

song_table_insert = ("""insert into song (song_id, song_name, artist_id, year, duration) select song_id, title, artist_id, year, duration from staging_songs
""")

artist_table_insert = ("""insert into artist(artist_id, artist_name, location, lattitude, longitude) select distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude from staging_songs
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
                    select start_time, extract(hour from start_time) as hour, 
                    extract(day from start_time) as day, extract(week from start_time) as week, 
                    extract(month from start_time) as month, extract(year from start_time), 
                    extract(dow from start_time) as dow from songplays;""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]