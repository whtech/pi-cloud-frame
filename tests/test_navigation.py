from gui.photo_app import PhotoFrame
from utils.config import Config


def test_next():
    """
    Test that 'next' navigation in non-shuffle mode moves from one photo to the next.
    """
    frame = PhotoFrame(Config("tests/test_navigation.yml"))
    player = frame.get_current_player()
    num_photos = len(player.get_playlist())

    assert player.current_media_index is None

    for i in range(num_photos * 2): #  loop past the end
        player.next()
        assert player.current_media_index == i % num_photos

def test_next_shuffle():
    """
    Test that 'next' navigation in shuffle mode does not give sequential photos.
    This tests uses a random shuffle which may occasionally match the sequential order and fail.
    May need to run the test again.
    """
    frame = PhotoFrame(Config("tests/test_navigation_shuffle.yml"))
    player = frame.get_current_player()
    num_photos = len(player.get_playlist())

    assert player.current_media_index is None

    for i in range(min(4, num_photos)):  #  keep the number of transitions small to reduce the probabilty of this failing
        player.next()
        assert player.current_media_index != i

def test_prev():
    """
    Test that 'prev' navigation in non-shuffle mode moves from one photo to the next.
    """
    _prev_test_with_config(PhotoFrame(Config("tests/test_navigation.yml")))

def test_prev_shuffle():
    """
    Test that 'prev' navigation in non-shuffle mode moves backwards through the browsing history.
    """
    _prev_test_with_config(PhotoFrame(Config("tests/test_navigation_shuffle.yml")))

def _prev_test_with_config(frame):
    player = frame.get_current_player()
    num_photos = len(player.get_playlist())

    assert player.current_media_index is None

    browsing_history = []
    # generate a browsing history
    for i in range(num_photos * 2):
        player.next()
        browsing_history.append(player.current_media_index)

    # back-track with prev and compare to the browsing history
    for j in reversed(browsing_history):
        assert player.current_media_index == j
        player.prev()

def test_prev_no_history():
    frame = PhotoFrame(Config("tests/test_navigation.yml"))
    player = frame.get_current_player()

    # generate a short browsing history
    for i in range(4):
        player.next()
        player.next()
        player.next()

    # try to back-track with a longer browsing history
    # back-track with prev and compare to the browsing history
    for i in range(4):
        player.prev()
        player.prev()
        player.prev()

    # current media should be None when history is empty
    player.prev()
    assert player.current_media_index is None

    player.prev()
    assert player.current_media_index is None