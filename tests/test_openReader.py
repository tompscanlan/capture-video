import sys
sys.path.append(".")

import pytest
import mock
import motioncapture

@mock.patch('motioncapture.cv2.VideoCapture')
def test_called_openReader(mock_capture):
    url = "http://some.url"
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)
    mock_capture.assert_called_with(url)

def test_openReader_exception_on_bad_domain():
    url = "http://some.urlx-with.bad.domain"
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)

@mock.patch('motioncapture.cv2.VideoCapture.isOpened')
@mock.patch('motioncapture.cv2.VideoCapture')
def test_openReader_isOpened_handler(mock_capture, mock_isOpened):
    url = "http://some.url"

    mock_capture.return_value = mock.Mock()
    mock_capture.return_value.isOpened.return_value = False
    reader = None
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)
    assert(reader is None)

    mock_capture.return_value = mock.Mock()
    mock_capture.return_value.isOpened.return_value = True
    reader = None
    reader = motioncapture.openReader(url)
    assert(reader is not None)


@mock.patch('motioncapture.cv2.VideoCapture')
def test_bad_VideoCapture(mock_capture):
    url = "http://some.url"

    mock_capture.return_value = None

    mock_capture.isOpened.return_value = None
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)

    mock_capture.isOpened.return_value = False
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)

    mock_capture.isOpened.return_value = True
    with pytest.raises(Exception) as e_info:
        reader = motioncapture.openReader(url)

