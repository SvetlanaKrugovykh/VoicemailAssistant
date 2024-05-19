# test_sip_client.py
import sys
sys.path.append('src/python') 
from sip_client import answer

class MockVoIPPhone:
    def __init__(self, callback):
        self.callback = callback

    def simulate_call(self):
        # Simulate a call
        print("Simulating a call...")
        self.callback()

# Create a mock VoIPPhone object
mock_phone = MockVoIPPhone(answer)

# Simulate a call
mock_phone.simulate_call()