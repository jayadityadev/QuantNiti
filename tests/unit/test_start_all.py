import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from start_all import (
    find_android_tool,
    get_lan_ip,
    get_python_exe,
    get_running_devices,
    has_visible_emulator_window,
    is_server_ready,
    kill_process_on_port,
)


def test_get_lan_ip():
    ip = get_lan_ip()
    assert isinstance(ip, str)
    assert len(ip.split(".")) == 4


def test_get_python_exe():
    exe = get_python_exe()
    assert isinstance(exe, str)
    assert Path(exe).exists()


def test_find_android_tool():
    # adb should either be resolved or return None
    res = find_android_tool("adb")
    if res is not None:
        assert isinstance(res, Path)
        assert res.exists()


def test_is_server_ready_when_closed():
    # Arbitrary unopened high port should return False without exception
    assert is_server_ready(port=59999) is False


def test_get_running_devices_parsing():
    mock_res = MagicMock()
    mock_res.stdout = "List of devices attached\nemulator-5554\tdevice\noffline-device\toffline\n\n"
    with patch("subprocess.run", return_value=mock_res):
        devices = get_running_devices(Path("fake_adb"))
        assert devices == ["emulator-5554"]


def test_has_visible_emulator_window():
    # Calling has_visible_emulator_window should return a bool without exception
    result = has_visible_emulator_window()
    assert isinstance(result, bool)


def test_kill_process_on_port_safely():
    # Calling on an unused port should not throw
    kill_process_on_port(port=59998)
