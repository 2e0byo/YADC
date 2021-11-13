from yadc.humanlike import randsleep


def test_randsleep(mocker):
    slept = 0

    def mock_sleep(s):
        nonlocal slept
        slept = s

    mocker.patch("yadc.humanlike.sleep", mock_sleep)
    randsleep(20, 100)
    assert slept < 100
    assert abs(slept - 20) < 20
