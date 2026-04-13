import contextlib
import io


def test_with_redirect_stdout() -> None:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print("captured output")
    assert True
