import pytest

from src.DatabaseManager import DatabaseManager
from src.FoulLanguageStatus import FoulLanguageStatus

TEST_DB_NUM_POSTS = 3
TEST_DB_NUM_PARAGRAPHS = 3

@pytest.fixture
def test_manager(tmp_path):
    manager = DatabaseManager(tmp_path/'database.db')
    for i in range(1, TEST_DB_NUM_POSTS+1):
        paragraphs = [f"Paragraph {i}.{j}." for j in range(1, TEST_DB_NUM_PARAGRAPHS+1)]
        manager.insert_post(f"Post {i}", paragraphs)
    return manager

def test_empty_database(tmp_path):
    manager = DatabaseManager(tmp_path/'empty.db')
    assert not manager.get_post_ids()

def test_insert_post(tmp_path):
    manager = DatabaseManager(tmp_path/'empty.db')
    post_id = manager.insert_post("Post 1", ["Paragraph 1.", "Paragraph 2."])
    assert post_id == 1

def test_get_post_ids(test_manager):
    ids = test_manager.get_post_ids()
    assert ids == [i for i in range(1, TEST_DB_NUM_POSTS+1)]

def test_get_post_ids_limit(test_manager):
    ids = test_manager.get_post_ids(limit=2)
    assert ids == [1, 2]

def test_get_post_paragraphs(test_manager):
    post_id = 2
    paragraphs = test_manager.get_post_paragraphs(post_id)
    paragraphs_expected = {(post_id-1)*TEST_DB_NUM_PARAGRAPHS+i:f"Paragraph {post_id}.{i}." for i in range(1, TEST_DB_NUM_PARAGRAPHS+1)}
    assert paragraphs == paragraphs_expected

def test_update_post_status_no_foul(test_manager):
    post_id = 2
    test_manager.update_post_status(post_id, FoulLanguageStatus.NO_FOUL_LANGUAGE)
    ids = test_manager.get_post_ids(only_unverified=True)
    assert ids == [i for i in range(1, TEST_DB_NUM_POSTS+1) if i != post_id]

def test_update_post_status_has_foul(test_manager):
    post_id = 2
    test_manager.update_post_status(post_id, FoulLanguageStatus.HAS_FOUL_LANGUAGE)
    ids = test_manager.get_post_ids(only_unverified=True)
    assert ids == [i for i in range(1, TEST_DB_NUM_POSTS+1) if i != post_id]

def test_update_paragraph_status_no_foul(test_manager):
    post_id = 2
    test_manager.update_paragraphs_status({(post_id-1)*TEST_DB_NUM_PARAGRAPHS+i:FoulLanguageStatus.NO_FOUL_LANGUAGE for i in range(1, TEST_DB_NUM_PARAGRAPHS+1)})
    paragraphs = test_manager.get_post_paragraphs(post_id, only_unverified=True)
    assert paragraphs == {}

def test_update_paragraph_status_has_foul(test_manager):
    post_id = 2
    test_manager.update_paragraphs_status({(post_id-1)*TEST_DB_NUM_PARAGRAPHS+i:FoulLanguageStatus.HAS_FOUL_LANGUAGE for i in range(1, TEST_DB_NUM_PARAGRAPHS+1)})
    paragraphs = test_manager.get_post_paragraphs(post_id, only_unverified=True)
    assert paragraphs == {}

def test_check_post_has_foul_paragraph(test_manager):
    post_id = 2
    paragraph_id = (post_id-1)*TEST_DB_NUM_PARAGRAPHS+1
    test_manager.update_paragraphs_status({paragraph_id: FoulLanguageStatus.HAS_FOUL_LANGUAGE})
    assert test_manager.check_post_has_foul_paragraph(post_id) == True

def test_check_post_has_foul_paragraph_false(test_manager):
    post_id = 2
    assert test_manager.check_post_has_foul_paragraph(post_id) == False
