from yadc.humanlike import randsleep
import pytest

sleeps = (0.01, 0.1, 1, 2, 5, 7, 10, 20, 100)


@pytest.mark.parametrize("s", sleeps)
def test_randsleep(s, mocker):
    slept = 0

    def mock_sleep(s):
        nonlocal slept
        slept = s

    mocker.patch("yadc.humanlike.sleep", mock_sleep)
    randsleep(s)
    assert abs(slept - s) < s / 5
