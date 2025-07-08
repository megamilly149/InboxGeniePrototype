# services/speech_service.py

import azure.cognitiveservices.speech as speechsdk
import appconfig.py

class SpeechToTextService:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=appconfig.AZURE_SPEECH_KEY, region=appconfig.AZURE_REGION)
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def recognize_speech(self):
        """Capture speech from the microphone and convert to text."""
        print("Say something...")
        result = self.speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return None
