#definitions.py
import socket
import logging
from pyVoIP.VoIP import VoIPPhone as BaseVoIPPhone

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    def start(self) -> None:
        logger.info("VoIPPhone start method called")
        super().start()
        logger.info("VoIPPhone start method finished") 

    def send_message(self, message):
        logger.debug(f"Sending SIP message: {message}")
        super().send_message(message)

    def receive_message(self):
        message = super().receive_message()
        logger.debug(f"Received SIP message: {message}")
        return message
    
    def stop(self, failed=False) -> None:
        logger.info("VoIPPhone stop method called")
        super().stop()
        logger.info("VoIPPhone stop method finished")

    def call_out(self, target_number):
        logger.info(f"call_out called with phone: {self} and target_number: {target_number}")
        self.dial(target_number)  # use self instead of phone        