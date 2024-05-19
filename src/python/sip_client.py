import os
from dotenv import load_dotenv
from pyVoIP.VoIP import VoIPPhone, InvalidStateError
from voicemail_assistant import start_voicemail  # import your voicemail assistant

load_dotenv()  # load variables from .env

def answer(call):
    try:
        call.answer()
        print(f"Caller's phone number: {call.info().remote_info}")  # print the caller's phone number
        start_voicemail()  # start the voicemail assistant
        call.hangup()
    except InvalidStateError:
        pass

if __name__ == "__main__":
    phone = VoIPPhone(os.getenv('SIP_SERVER_IP'), 
                      int(os.getenv('SIP_SERVER_PORT')), 
                      os.getenv('SIP_AUTHORIZATION_USER'), 
                      os.getenv('SIP_PASSWORD'),
                      callCallback=answer, myIP=os.getenv('LOCAL_IP'),
                      rtpPortLow=10000, rtpPortHigh=20000)
    
    try:
        phone.register()
        reg_info = phone.account.info()  # get registration info
        print(f"Registration status: {reg_info.reg_status}")
        print(f"Registration reason: {reg_info.reg_reason}")
        print(f"Is account valid: {reg_info.is_valid}")
    except Exception as e:
        print(f"Registration failed: {e}")

    phone.start()
    input('ggg')
    phone.stop()