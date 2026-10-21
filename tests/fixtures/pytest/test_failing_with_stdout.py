def test_will_fail_after_printing():
    print("printed by the failing test")
    assert False
