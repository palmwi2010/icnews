# Tests to query the API

from app import process_query


def test_pi():
    assert process_query("pi") == "i is an irrational number"  # Should fail


def test_knows_lotr():
    query = "Who is the author of LOTR"
    assert process_query(query) == "JRR Tolkein"  # Should pass


api = 0
expected_format = 0


def test_book_api():
    assert process_query(api) == expected_format
