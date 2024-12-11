import platform
import os
from enum import Enum

class OS(Enum):
    MACOS = 'macOS'
    WINDOWS = 'windows'
    LINUX = 'linux'

def get_OS()->OS:
    os_name = platform.system()
    if "windo" in os_name.lower():
        return OS.WINDOWS
    elif "dar" in os_name.lower():
        return OS.MACOS
    return OS.LINUX


def get_cache_path() -> str:
    os_type = get_OS()
    if os_type == OS.WINDOWS:
        # Use APPDATA for Windows
        cache_dir = os.getenv('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
    elif os_type == OS.MACOS:
        # Use ~/Library/Caches for macOS
        cache_dir = os.path.expanduser('~/Library/Caches')
    else:
        # Use ~/.cache for Linux
        cache_dir = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
    dockscribe_dir = os.path.join(cache_dir, 'dockscribe')
    os.makedirs(dockscribe_dir, exist_ok=True)
    return dockscribe_dir


def get_app_data_path() -> str:
    os_type = get_OS()
    if os_type == OS.WINDOWS:
        # Use APPDATA for Windows application data
        app_data_dir = os.getenv('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
    elif os_type == OS.MACOS:
        # Use ~/Library/Application Support for macOS application data
        app_data_dir = os.path.expanduser('~/Library/Application Support')
    else:
        # Use ~/.local/share for Linux application data
        app_data_dir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))

    dockscribe_dir = os.path.join(app_data_dir, 'dockscribe')
    os.makedirs(dockscribe_dir, exist_ok=True)
    return dockscribe_dir