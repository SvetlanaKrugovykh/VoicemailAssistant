#voicemail_assistant.py
import time
import wave

def answer(call=None):
    try:
        print(f"Incoming call from {call.caller}")
        f = wave.open('prompt.wav', 'rb')
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        call.answer()
        call.write_audio(data)

        while call.state == CallState.ANSWERED:
            dtmf = call.get_dtmf()
            if dtmf == "1":
                # Do something
                call.hangup()
            elif dtmf == "2":
                # Do something else
                call.hangup()
            time.sleep(0.1)
    except InvalidStateError:
        pass
    except:
        call.hangup()

