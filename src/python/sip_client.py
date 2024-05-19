# sip_client.py
from dotenv import load_dotenv
import os
import pjsua as pj
import sys

# Load .env file
load_dotenv()

# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

# Callback to receive events from Account
class MyAccountCallback(pj.AccountCallback):
    def __init__(self, acc):
        pj.AccountCallback.__init__(self, acc)

def log_cb(level, str, len):
    print(str),

try:
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP)

    # Start the library
    lib.start()

    # Set SIP server, user and password from environment variables
    SIP_SERVER_IP = os.getenv('SIP_SERVER_IP')
    SIP_SERVER_PORT = os.getenv('SIP_SERVER_PORT')
    SIP_PROTOCOL = os.getenv('SIP_PROTOCOL')
    SIP_USER = os.getenv('SIP_AUTHORIZATION_USER')
    SIP_PASSWORD = os.getenv('SIP_PASSWORD')

    # Combine protocol, IP and port
    SIP_SERVER = f"{SIP_PROTOCOL}://{SIP_SERVER_IP}:{SIP_SERVER_PORT}"

    # Create SIP account
    acc_cfg = pj.AccountConfig(domain=SIP_SERVER, username=SIP_USER, password=SIP_PASSWORD)
    acc = lib.create_account(acc_cfg)

    # Make call
    destination = "sip:destination@ip_address"  # Replace with actual destination
    call = acc.make_call(destination, MyCallCallback())

    # Wait for ENTER before quitting
    print("Press <ENTER> to quit")
    input = sys.stdin.readline().rstrip("\r\n")

    # We're done, shutdown the library
    lib.destroy()
    lib = None

except pj.Error as e:
    print("Exception: " + str(e))
    lib.destroy()
    lib = None