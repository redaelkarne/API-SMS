import mysql.connector
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
# Establishing database connection
connection = mysql.connector.connect(
    host='192.168.0.12',
    port=3366,
    database='dick',
    user='astus',
    password='123456'
)
cursor = connection.cursor()

# Defining API credentials
username = "******"
password = "******"

# API endpoint URL
url = "https://sms.virgopass.com/d2/multipush"
def send_email(subject, body):
    sender_email = "relkarne@astus.fr"  
    recipient_email = "relkarne@astus.fr"  
    password = "289ga69LY"  

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("Mail1.sfrbusinessteam.fr") as server:
        server.sendmail(sender_email, recipient_email, message.as_string())

# Retrieving SMS messages from the database
query = "SELECT Corps_sms, Destinataire_sms, ID_sms, Client_sms,`check` FROM `traitementsms` WHERE `check` <> 1"
cursor.execute(query)
rows = cursor.fetchall()

# Iterating through each SMS message
for row in rows:
    phone_number = row[1]
    if phone_number.startswith("0") or phone_number.startswith("+"):
        phone_number = phone_number.replace(" ", "")
        if phone_number.startswith("0"):
            phone_number = "+33" + phone_number[1:]

    message = row[0]
    client_sms = row[3]
    check = row[4]

    message_sent_successfully = False

    # If message length is greater than 160 characters, split into chunks
    if len(message) > 160:
        message_chunks = [message[i:i+160] for i in range(0, len(message), 160)]
        update_query1 = f"UPDATE `traitementsms` SET `NB_sms` = 2 WHERE ID_sms = {row[2]}"
        cursor.execute(update_query1)
        connection.commit()

        # Sending each chunk of the message
        for idx, chunk in enumerate(message_chunks):
            payload = {
                "tpl": {
                    "a": {
                        "text": chunk,
                        "app_address": "ASTUS",
                    }
                },
                "msg": [
                    {
                        "tpl": "a",
                        "ope_address": phone_number,
                        "app_msgid": f"{row[2]}_{idx+1}",
                        "ope_channel": "38979",
                        "tag": client_sms
                    }
                ]
            }

            # Sending the chunk via API request
            response = requests.post(url, json=payload, auth=(username, password))

            # Handling API response
            if response.status_code == 200:
                print(f"Chunk {idx+1} of SMS sent successfully.")
            else:
                print(f"Failed to send SMS chunk {idx+1}. Status code: {response.status_code}")
                print(response.text)
                break
        else:
            message_sent_successfully = True

    # If message length is not greater than 160 characters
    else:
        payload = {
            "tpl": {
                "a": {
                    "text": message,
                    "app_address": "ASTUS",
                }
            },
            "msg": [
                {
                    "tpl": "a",
                    "ope_address": phone_number,
                    "app_msgid": str(row[2]),
                    "ope_channel": "38979",
                    "tag": client_sms
                }
            ]
        }

        # Sending the message via API request
        response = requests.post(url, json=payload, auth=(username, password))

        # Handling API response
        if response.status_code == 200:
            print("JSON data sent successfully.")
            message_sent_successfully = True
            update_query2 = f"UPDATE `traitementsms` SET `AC_sms` = 'Envoye' WHERE ID_sms = {row[2]}"
            cursor.execute(update_query2)
            connection.commit()
        elif check != 2:
            print(f"Failed to send JSON data. Status code: {response.status_code}")
            print(response.text)
            sujet = "Échec d'envoi du SMS"
            corps = f"Échec de l'envoi du SMS : {row[0]} envoyé a {row[1]} {row[3]} dont l'ID est {row[2]}. Code d'état : {response.status_code}. Réponse : {response.text}"
            send_email(sujet, corps)
            update_query = f"UPDATE `traitementsms` SET `check` = 2 WHERE ID_sms = {row[2]}"
            cursor.execute(update_query)
            connection.commit()
            

    
    if message_sent_successfully:
        update_query = f"UPDATE `traitementsms` SET `check` = 1 WHERE ID_sms = {row[2]}"
        cursor.execute(update_query)
        connection.commit()
now = datetime.datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
update_query = f"UPDATE `log` SET `dateLastMaj` = '{formatted_date}' WHERE `process` = 'ACCUSE SMS'"
cursor.execute(update_query)
connection.commit()
# Closing database connection
cursor.close()
connection.close()
