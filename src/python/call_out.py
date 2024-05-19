# call_out.py

def call_out(phone, target_number):
    try:
        phone.call(target_number)
        input('Press enter to hang up')
    except Exception as e:
        print(f"Call failed: {e}")
    finally:
        input('Press enter to disable the phone')
        phone.stop()
        