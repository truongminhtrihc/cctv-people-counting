import os
import sys
import shutil
import subprocess
import json
import sqlite3
from time import sleep
from datetime import datetime, timedelta, timezone
from kafka import KafkaConsumer
from multiprocessing import Process


def check_stream(video_ip: str) -> bool:
    command = ['ffprobe', '-timeout', '10000000', '-loglevel', 'quiet', video_ip]
    process = subprocess.run(command)
    return process.returncode == 0

def make_stream_converter(cameras, storage):
    print("Making stream to stream converter process")
    proccesses: dict[str, subprocess.Popen] = {}
    while True:
        for camera in cameras:
            available = check_stream(camera[4])
            if available and proccesses.get(str(camera[0]), None) is None:
                shutil.rmtree(storage + str(camera[0]), ignore_errors=True)
                os.makedirs(storage + str(camera[0]))
                proccesses[str(camera[0])] = subprocess.Popen([
                    'ffmpeg',
                    '-i', camera[4],
                    '-vf', 'select=concatdec_select',
                    '-af', 'aselect=concatdec_select,aresample=async=1',
                    '-c:a', 'aac',
                    '-f', 'hls',
                    '-hls_time', '10',
                    '-hls_list_size', '6',
                    '-hls_flags', 'delete_segments',
                    '-loglevel', 'quiet',
                    storage + str(camera[0]) + '/output.m3u8'
                ])
                print("Connected to camera " + str(camera[0]) + ", HLS stream available")
            if not available:
                if proccesses.get(str(camera[0]), None) is not None:
                    proccesses[str(camera[0])].terminate()
                print("Failed to connect to " + str(camera[1]) + ", retry in 30s")
        sleep(30)

def seconds_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return int((next_hour - now).total_seconds())
    
def make_video_recorder(cameras, storage):
    print("Making stream to video converter process")
    proccesses: dict[str, subprocess.Popen] = {}
    while True:
        for camera in cameras:
            remain_time = seconds_until_next_hour()
            available = check_stream(camera[4])
            if available and proccesses.get(str(camera[0]), None) is None:
                if not os.path.exists(storage + "Video/" + str(camera[0])):
                    os.makedirs(storage + "Video/" + str(camera[0]))
                name = str(datetime.now().date()) + '_' + str(datetime.now().hour)
                proccesses[str(camera[0])] = subprocess.Popen([
                    'ffmpeg',
                    '-i', camera[4],
                    '-c', 'copy',
                    '-t', str(remain_time),
                    '-strftime', '1',
                    '-loglevel', 'quiet',
                    storage + "Video/" + str(camera[0]) + '/' + name +'.mp4'
                ])
                print("Connected to camera " + str(camera[0]) + ", recording video")
            if not available:
                if proccesses.get(str(camera[0]), None) is not None:
                    proccesses[str(camera[0])].terminate()
                print("Failed to connect to " + str(camera[1]) + ", retry next hour")
        sleep(remain_time)

def main():
    if len(sys.argv) < 2:
        print("Missing argument")
        sys.exit(1)
    # Reading arguments
    storage = sys.argv[1]

    # Create database connection
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * from api_camera")
    cameras = cur.fetchall()
    consumer = None
    try:
        sc_process = Process(target=make_stream_converter, args=(cameras, storage))
        vr_process = Process(target=make_video_recorder, args=(cameras, storage))
        sc_process.start()
        vr_process.start()

        print("Making kafka consumer")
        while not consumer:
            try:
                consumer = KafkaConsumer('quickstart-events', bootstrap_servers='172.30.63.34:9092')
            except:
                print("Can't connect to kafka server, retry in 30s")
                sleep(30)
        
        old = None
        print("Kafka consumer made, reading data")
        for message in consumer:
            data = json.loads(message.value.decode('utf-8'))['analyticsModule']
            if old == None or data['Entry'] != old['Entry'] or data['Exit'] != old['Exit']:
                record = {
                    'camera_id': data['source_id'],
                    'hour': datetime.now(timezone.utc).hour,
                    'date': datetime.now(timezone.utc).date(),
                    'people_in': data['Entry'],
                    'people_out': data['Exit']
                }
                res = cur.execute("SELECT * FROM api_latestmetadata WHERE camera_id = :camera_id", record)
                row = res.fetchone()
                if row is None:
                    cur.execute("INSERT INTO api_latestmetadata (camera_id, people_in, people_out) VALUES (:camera_id, :people_in, :people_out)", record)
                else:
                    cur.execute("UPDATE api_latestmetadata SET people_in = :people_in, people_out = :people_out WHERE camera_id = :camera_id", record)
                    if row[1] < record['people_in'] and row[2] < record['people_out']:
                        record['people_in'] -= row[1]
                        record['people_out'] -= row[2]
                con.commit()
                res = cur.execute("SELECT * FROM api_metadata WHERE camera_id = :camera_id AND hour = :hour AND date= :date", record)
                print("Inserting record: " + str(record))
                if res.fetchone() is None:
                    cur.execute("INSERT INTO api_metadata (camera_id, hour, date, people_in, people_out) VALUES (:camera_id, :hour, :date, :people_in, :people_out)", record)
                else:
                    cur.execute("UPDATE api_metadata SET people_in = :people_in, people_out = :people_out WHERE camera_id = :camera_id AND hour = :hour AND date= :date", record)
                con.commit()
            old = data

    except KeyboardInterrupt:
        sc_process.terminate()
        vr_process.terminate()
    finally:
        if consumer:
            consumer.close()
            print("Closing consumer")
        

if __name__ == "__main__":
    main()