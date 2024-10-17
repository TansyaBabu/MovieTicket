import speech_recognition as sr
from transformers import pipeline

def recognize_speech_and_analyze_sentiment():
    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for feedback...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's Speech Recognition API
            feedback = recognizer.recognize_google(audio)
            print(f"Feedback Received: {feedback}")
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

        # Sentiment Analysis
        sentiment_analysis = pipeline("sentiment-analysis")
        sentiment_result = sentiment_analysis(feedback)
        
        sentiment = sentiment_result[0]['label']
        confidence = sentiment_result[0]['score']

        return {
            'feedback': feedback,
            'sentiment': sentiment,
            'confidence': confidence
        }
