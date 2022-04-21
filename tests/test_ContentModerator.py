import json
import pytest
import responses

from src.ContentModerator import ContentModerator
from src.FoulLanguageStatus import FoulLanguageStatus

TEST_DB_NUM_POSTS = 3
TEST_DB_NUM_PARAGRAPHS = 3


def request_callback(request):
    payload = json.loads(request.body)
    has_foul_language = "****" in payload["fragment"]
    resp_body = { "hasFoulLanguage": has_foul_language }
    headers = { "Content-Type": "application/json" }
    return (200, headers, json.dumps(resp_body))

@pytest.fixture
def test_moderator(tmp_path):
    moderator = ContentModerator(tmp_path/'database.db')
    return moderator

@pytest.fixture
def test_moderator_db(tmp_path):
    moderator = ContentModerator(tmp_path/'database.db')
    for i in range(1, TEST_DB_NUM_POSTS+1):
        paragraphs = [f"Paragraph {i}.{j}." for j in range(1, TEST_DB_NUM_PARAGRAPHS+1)]
        moderator.database_manager.insert_post(f"Post {i}", paragraphs)
    return moderator

@responses.activate
def test_validate_sentence_no_foul(test_moderator):
    responses.add(method=responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE, json={"hasFoulLanguage": False }, status=200)
    status = test_moderator.validate_sentence("Test sentence.")
    assert status == FoulLanguageStatus.NO_FOUL_LANGUAGE

@responses.activate
def test_validate_sentence_has_foul(test_moderator):
    responses.add(method=responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE, json={"hasFoulLanguage": True }, status=200)
    status = test_moderator.validate_sentence("Test sentence.")
    assert status == FoulLanguageStatus.HAS_FOUL_LANGUAGE

@responses.activate
def test_validate_sentence_api_error(test_moderator):
    responses.add(method=responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE, status=404)
    status = test_moderator.validate_sentence("Test sentence.")
    assert status == FoulLanguageStatus.UNVERIFIED

@responses.activate
def test_validate_paragraph_no_foul(test_moderator):
    responses.add_callback(
        responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE,
        callback=request_callback,
        content_type="application/json",
    )
    status = test_moderator.validate_paragraph("This is sentence 1. This is sentence 2.")
    assert status == FoulLanguageStatus.NO_FOUL_LANGUAGE

@responses.activate
def test_validate_paragraph_has_foul(test_moderator):
    responses.add_callback(
        responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE,
        callback=request_callback,
        content_type="application/json",
    )
    status = test_moderator.validate_paragraph("This is sentence 1. This is ****.")
    assert status == FoulLanguageStatus.HAS_FOUL_LANGUAGE

@responses.activate
def test_validate_paragraph_api_error(test_moderator):
    responses.add(method=responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE, status=404)
    status = test_moderator.validate_paragraph("This is sentence 1. This is ****.")
    assert status == FoulLanguageStatus.UNVERIFIED

@responses.activate
def test_validate_post_no_foul(test_moderator_db):
    responses.add_callback(
        responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE,
        callback=request_callback,
        content_type="application/json",
    )
    status = test_moderator_db.validate_post(1)
    assert status == FoulLanguageStatus.NO_FOUL_LANGUAGE

@responses.activate
def test_validate_post_has_foul(test_moderator_db):
    responses.add_callback(
        responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE,
        callback=request_callback,
        content_type="application/json",
    )
    post_id = test_moderator_db.database_manager.insert_post("Foul post", ["This paragraph is nice. It has two sentences", "This paragraph is not so much. He calls people ****."])
    status = test_moderator_db.validate_post(post_id)
    assert status == FoulLanguageStatus.HAS_FOUL_LANGUAGE

@responses.activate
def test_validate_post_api_error(test_moderator_db):
    responses.add(method=responses.POST, url=ContentModerator.URL_VALIDATE_SENTENCE, status=404)
    status = test_moderator_db.validate_post(1)
    assert status == FoulLanguageStatus.UNVERIFIED