import azure.cognitiveservices.speech as speechsdk
import os

# Azure Speech Service credentials
subscription_key = "<YOUR_AZURE_SUBSCRIPTION_KEY>"
region = "<YOUR_AZURE_REGION>"

# Create an instance of a speech configuration with subscription info
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

# Set up audio configuration (from microphone)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Create a speech recognizer instance
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Start speech recognition
print("Say something...")

# This will run once (recognizes speech only once)
result = speech_recognizer.recognize_once()

# Check the result of recognition
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
