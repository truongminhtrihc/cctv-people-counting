from kafka import KafkaConsumer
import json
import sqlite3
from datetime import datetime
import sys

def main():
    if len(sys.argv) < 1:
        print("Missing argument")
        sys.exit(1)
    path = sys.argv[0][0:-13]
    con = sqlite3.connect(path + "db.sqlite3")
    cur = con.cursor()
    print("Making consumer")
    consumer = KafkaConsumer('quickstart-events', bootstrap_servers='172.30.63.34:9092')
    try:
        old = None
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
                cur.execute("INSERT INTO report_metadata (time, camera_id, people_in, people_out) VALUES (:time, :camera_id, :people_in, :people_out)", record)
                con.commit()
            old = data
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Closing consumer")

if __name__ == "__main__":
    main()