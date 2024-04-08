import os
import sys
import shutil
import subprocess
import json
import sqlite3
from time import sleep
from datetime import datetime
from kafka import KafkaConsumer
from multiprocessing import Process


def check_stream(ip: str) -> bool:
    command = ['ffprobe', '-timeout', '10000000', '-loglevel', 'quiet', ip]
    process = subprocess.run(command)
    return process.returncode == 0

def make_stream_converter(cameras, storage):
    print("Making stream to stream converter process")
    while (cameras):
        for camera in cameras:
            if check_stream(camera[3]):
                shutil.rmtree(storage + str(camera[0]), ignore_errors=True)
                os.makedirs(storage + str(camera[0]))
                subprocess.Popen([
                    'ffmpeg',
                    '-i', camera[3],
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
                cameras.remove(camera)
                print("Connected to camera " + str(camera[0]) + ", HLS stream available")
            else:
                print("Failed to connect to camera " + str(camera[0]) + ", retry in 30s")
        sleep(30)
    

def main():
    if len(sys.argv) < 3:
        print("Missing argument")
        sys.exit(1)

    # Reading arguments
    path = sys.argv[1]
    storage = sys.argv[2]

    # Create database connection
    con = sqlite3.connect(path + "db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT * from api_camera")
    cameras = cur.fetchall()
    consumer = None
    try:
        sc_process = Process(target=make_stream_converter, args=(cameras, storage))
        sc_process.start()

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
                    'time': datetime.now(),
                    'camera_id': 1,
                    'people_in': data['Entry'],
                    'people_out': data['Exit']
                }
                print("Inserting record: " + str(record))
                cur.execute("INSERT INTO api_metadata (time, camera_id, people_in, people_out) VALUES (:time, :camera_id, :people_in, :people_out)", record)
                con.commit()
            old = data

    except KeyboardInterrupt:
        sc_process.terminate()
    finally:
        if consumer:
            consumer.close()
            print("Closing consumer")
        

if __name__ == "__main__":
    main()