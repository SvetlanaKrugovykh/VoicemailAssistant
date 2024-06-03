#sip_client.py
import os
import time
import hashlib
from dotenv import load_dotenv
from definitions import is_udp_open, logger   # import from definitions.py
from voicemail_assistant import answer  
from call_out import call_out
from pyVoIP.VoIP import VoIPPhone 

load_dotenv()  # load variables from .env

if __name__ == "__main__":
    SIP_SERVER_IP = os.getenv('SIP_SERVER_IP')
    SIP_SERVER_PORT = int(os.getenv('SIP_SERVER_PORT'))
    SIP_AUTHORIZATION_USER = os.getenv('SIP_AUTHORIZATION_USER')
    SIP_PASSWORD = os.getenv('SIP_PASSWORD')
    LOCAL_IP = os.getenv('LOCAL_IP')

    if not all([SIP_SERVER_IP, SIP_SERVER_PORT, SIP_AUTHORIZATION_USER, SIP_PASSWORD, LOCAL_IP]):
        logger.error("Environment variables are not set. Exiting.")
        exit(1)

    if not is_udp_open(SIP_SERVER_IP, SIP_SERVER_PORT):
        logger.error(f"Cannot connect to {SIP_SERVER_IP}:{SIP_SERVER_PORT} over UDP. Exiting.")
        exit(1)

    try:
        phone = VoIPPhone (SIP_SERVER_IP, 
                          SIP_SERVER_PORT, 
                          SIP_AUTHORIZATION_USER, 
                          SIP_PASSWORD,
                          LOCAL_IP,   
                          callCallback=answer)

        phone.start()
        logger.info(f"VoIPPhone start method finished with answer: {phone._status}")

        time.sleep(3)
        print(phone.get_status())

        target_number = "sip:0442202020"  # replace with the number you want to call
        logger.info(f"Calling {target_number}")
        call_out(phone, target_number)

    except Exception as e:
        logger.error(f"Registration failed: {e}")
    finally:
        logger.info("Stopping the phone")
        phone.stop()
        logger.info("Phone stopped successfully")



