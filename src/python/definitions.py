#definitions.py
import socket
import logging

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
    