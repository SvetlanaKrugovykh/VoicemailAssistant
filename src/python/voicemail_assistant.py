#voice_mail_assistant.py

import time
from pydub import AudioSegment
from caller_number_processor import process_caller_number
from local_enumerators import CallState

def answer(call=None):
    try:
        greeting_audio_path = 'assets/audio/greeting.mp3'
        
        greeting_audio = AudioSegment.from_mp3(greeting_audio_path)
        greeting_audio_data = greeting_audio.raw_data
        
        if greeting_audio_data is None:
            print("Error: Failed to load greeting audio data.")
            return

        if call is None:
            print("Call is None/ Test mode. Exiting.")
            return

        call.answer()
        print(f"Incoming call from {call.caller}")

        caller_audio_path = process_caller_number(call.caller)
        caller_audio = AudioSegment.from_mp3(caller_audio_path)
        caller_audio_data = caller_audio.raw_data

        call.write_audio(greeting_audio_data)
        call.write_audio(caller_audio_data)

        while call.state == CallState.ANSWERED:
            dtmf = call.get_dtmf()
            if dtmf == "1":
                recorded_audio = call.record_audio()
                recorded_audio.export("recorded_call.mp3", format="mp3")
                call.hangup()
            elif dtmf == "2":
                # TODO 
                call.hangup()
            time.sleep(0.1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if call is not None:
            call.hangup()

answer()