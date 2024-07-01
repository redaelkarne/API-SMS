import os
import sys
import time
import signal
import mysql.connector
from multiprocessing import Process

def daemon_task(last_processed_row_id):
    
    while True:
        try:
            print("Starting loop iteration...")
            start_time = time.time()

            # Connection DB 
            connection = mysql.connector.connect(
                host='******',
                port=******,
                database='*****',
                user='****',
                password='****'
            )
            cursor = connection.cursor()

            query = "SELECT * FROM `traitementsms` WHERE ID_sms > %s"
            cursor.execute(query, (last_processed_row_id,))
            new_rows = cursor.fetchall()

            if new_rows:
                print("New rows found:")
                for row in new_rows:
                    print(row)

                # Maj last_processed_row_id au dernier lignes trouvé
                last_processed_row_id = max(row[0] for row in new_rows)
                exec(open(r".................................").read())

        except mysql.connector.Error as err:
            print("Error querying database:", err)
        finally:
            # Fermer le  cursor et la connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

            end_time = time.time()
            print(f"Loop iteration completed in {end_time - start_time} seconds.")

        time.sleep(10)


def main():
    def sigterm_handler(signum, frame):
        print("Terminating daemon...")
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    last_processed_row_id = 0
    daemon_task(last_processed_row_id)
    # Lancement the daemon 
    daemon_process = Process(target=daemon_task)
    daemon_process.daemon = True
    daemon_process.start()
    daemon_process.join()

if __name__ == "__main__":
    main()
