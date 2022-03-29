import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions
from dotenv import load_dotenv
load_dotenv()


class Emotions:
    def __init__(self, string):
        self.string = string
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=IAMAuthenticator(os.getenv('NLU_API')))
        self.natural_language_understanding.set_service_url(os.getenv('NLU_URL'))

    def getText(self):
        return self.string

    def getAllEmotions(self):
        response = self.natural_language_understanding.analyze(text=self.string,
                                                               features=Features(
                                                                   emotion=EmotionOptions())).get_result()
        return response["emotion"]["document"]["emotion"]

    def getSentiment(self):
        response = self.natural_language_understanding.analyze(text=self.string,
                                                               features=Features(
                                                                   sentiment=SentimentOptions())).get_result()
        return float(response['sentiment']['document']['score'])

    def getMaxEmotion(self):
        emotions = self.getAllEmotions()
        return max(emotions, key=emotions.get)

