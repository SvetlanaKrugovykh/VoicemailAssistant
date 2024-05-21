#sip_client.py
import os
import socket
import logging
from dotenv import load_dotenv
from pyVoIP.VoIP import VoIPPhone as BaseVoIPPhone
from voicemail_assistant import answer  
from call_out import call_out

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()  # load variables from .env

def is_udp_open(ip, port):
    logger.debug(f"Checking UDP connection to {ip}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)  # two second timeout
    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except socket.error as e:
        logger.error(f"Failed to connect to {ip}:{port} over UDP: {e}")
        return False

class VoIPPhone(BaseVoIPPhone):
    def send_message(self, message):
        logger.debug(f"Sending SIP message: {message}")
        super().send_message(message)

    def receive_message(self):
        message = super().receive_message()
        logger.debug(f"Received SIP message: {message}")
        return message

if __name__ == "__main__":
    SIP_SERVER_IP = os.getenv('SIP_SERVER_IP')
    SIP_SERVER_PORT = os.getenv('SIP_SERVER_PORT')
    SIP_AUTHORIZATION_USER = os.getenv('SIP_AUTHORIZATION_USER')
    SIP_PASSWORD = os.getenv('SIP_PASSWORD')
    LOCAL_IP = os.getenv('LOCAL_IP')

    if not all([SIP_SERVER_IP, SIP_SERVER_PORT, SIP_AUTHORIZATION_USER, SIP_PASSWORD, LOCAL_IP]):
        logger.error("Environment variables are not set. Exiting.")
        exit(1)

    SIP_SERVER_PORT = int(SIP_SERVER_PORT)

    if not is_udp_open(SIP_SERVER_IP, SIP_SERVER_PORT):
        logger.error(f"Cannot connect to {SIP_SERVER_IP}:{SIP_SERVER_PORT} over UDP. Exiting.")
        exit(1)

    try:
        phone = VoIPPhone(SIP_SERVER_IP, 
                          SIP_SERVER_PORT, 
                          SIP_AUTHORIZATION_USER, 
                          SIP_PASSWORD,
                          myIP=LOCAL_IP, 
                          callCallback=answer)

        logger.info("Starting the phone")
        phone.start()
        logger.info("Phone started successfully")

        target_number = input('Enter the number to call: ')
        logger.info(f"Calling {target_number}")
        call_out(phone, target_number)

        input('Press enter to disable the phone')
    except Exception as e:
        logger.error(f"Registration failed: {e}")
    finally:
        logger.info("Stopping the phone")
        phone.stop()
        logger.info("Phone stopped successfully")



