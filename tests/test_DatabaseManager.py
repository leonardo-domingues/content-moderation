import pytest

from src.DatabaseManager import DatabaseManager

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
    assert ids == [1, 2, 3]

def test_get_post_ids_limit(test_manager):
    ids = test_manager.get_post_ids(limit=2)
    assert ids == [1, 2]

def test_get_post_ids_unverified(test_manager):
    # TODO: implement
    pass

def test_get_post_paragraphs(test_manager):
    post_id = 2
    paragraphs = test_manager.get_post_paragraphs(post_id)
    paragraphs_expected = {(post_id-1)*TEST_DB_NUM_PARAGRAPHS+i:f"Paragraph {post_id}.{i}." for i in range(1, TEST_DB_NUM_PARAGRAPHS+1)}
    assert paragraphs == paragraphs_expected

def test_get_post_paragraphs_unverified(test_manager):
    # TODO: implement
    pass