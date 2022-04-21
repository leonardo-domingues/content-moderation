from nltk import tokenize
from typing import List

import requests
import time

from src.DatabaseManager import DatabaseManager
from src.FoulLanguageStatus import FoulLanguageStatus


class ContentModerator:
    URL_VALIDATE_SENTENCE = "http://127.0.0.1:5000/sentences/"
    SLEEP_TIMER = 50.0 / 1000.0 # in seconds

    def __init__(self, database_path):
        self.database_manager = DatabaseManager(database_path)


    def validate_sentence(self, sentence: str) -> FoulLanguageStatus:
        try:
            response = requests.post(ContentModerator.URL_VALIDATE_SENTENCE, json={ "fragment": sentence })
            if response.ok:
                has_foul_language = response.json()["hasFoulLanguage"]
                return FoulLanguageStatus.HAS_FOUL_LANGUAGE if has_foul_language else FoulLanguageStatus.NO_FOUL_LANGUAGE
        except:
            return FoulLanguageStatus.UNVERIFIED

        return FoulLanguageStatus.UNVERIFIED


    def validate_paragraph(self, paragraph: str) -> FoulLanguageStatus:
        sentences = tokenize.sent_tokenize(paragraph)
        sentences_status = [self.validate_sentence(sentence) for sentence in sentences]
        if FoulLanguageStatus.UNVERIFIED in sentences_status:
            return FoulLanguageStatus.UNVERIFIED
        elif FoulLanguageStatus.HAS_FOUL_LANGUAGE in sentences_status:
            return FoulLanguageStatus.HAS_FOUL_LANGUAGE
        else:
            return FoulLanguageStatus.NO_FOUL_LANGUAGE


    def validate_post(self, post_id: int) -> FoulLanguageStatus:
        paragraphs = self.database_manager.get_post_paragraphs(post_id, only_unverified=True)
        new_paragraphs_status = {}
        for id, paragraph in paragraphs.items():
            status = self.validate_paragraph(paragraph)
            if status != FoulLanguageStatus.UNVERIFIED:
                new_paragraphs_status[id] = status

        self.database_manager.update_paragraphs_status(new_paragraphs_status)

        # If all unverified paragraphs were modified in this iteration, update post
        if len(paragraphs) == len(new_paragraphs_status):
            has_foul_paragraph = self.database_manager.check_post_has_foul_paragraph(post_id)
            new_post_status = FoulLanguageStatus.HAS_FOUL_LANGUAGE if has_foul_paragraph else FoulLanguageStatus.NO_FOUL_LANGUAGE
            self.database_manager.update_post_status(post_id, new_post_status)
            return new_post_status

        return FoulLanguageStatus.UNVERIFIED


    def run(self):
        while True:
            post_ids = self.database_manager.get_post_ids(only_unverified=True, limit=1)
            for post_id in post_ids:
                print(f"[ContentModerator] Verifying post {post_id}")
                self.validate_post(post_id)

            time.sleep(ContentModerator.SLEEP_TIMER)
