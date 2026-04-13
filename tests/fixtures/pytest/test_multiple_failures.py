def test_fail_one():
    assert False


def test_fail_two():
    assert 1 == 2


def test_error():
    raise ValueError("boom")
