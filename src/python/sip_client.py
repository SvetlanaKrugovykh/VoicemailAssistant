#sip_client.py
import os
import socket
from dotenv import load_dotenv
from pyVoIP.VoIP import VoIPPhone
from voicemail_assistant import answer  # import your voicemail assistant

load_dotenv()  # load variables from .env

def is_udp_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)  # two second timeout
    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except socket.error:
        return False

if __name__ == "__main__":
    SIP_SERVER_IP = os.getenv('SIP_SERVER_IP')
    SIP_SERVER_PORT = os.getenv('SIP_SERVER_PORT')
    SIP_AUTHORIZATION_USER = os.getenv('SIP_AUTHORIZATION_USER')
    SIP_PASSWORD = os.getenv('SIP_PASSWORD')
    LOCAL_IP = os.getenv('LOCAL_IP')

    if not all([SIP_SERVER_IP, SIP_SERVER_PORT, SIP_AUTHORIZATION_USER, SIP_PASSWORD, LOCAL_IP]):
        print("Environment variables are not set. Exiting.")
        exit(1)

    SIP_SERVER_PORT = int(SIP_SERVER_PORT)

    if not is_udp_open(SIP_SERVER_IP, SIP_SERVER_PORT):
        print(f"Cannot connect to {SIP_SERVER_IP}:{SIP_SERVER_PORT} over UDP. Exiting.")
        exit(1)

    phone = VoIPPhone(SIP_SERVER_IP, 
                      SIP_SERVER_PORT, 
                      SIP_AUTHORIZATION_USER, 
                      SIP_PASSWORD,
                      myIP=LOCAL_IP, 
                      callCallback=answer)

    try:
        phone.start()
        input('Press enter to disable the phone')
    except Exception as e:
        print(f"Registration failed: {e}")
    finally:
        phone.stop()



