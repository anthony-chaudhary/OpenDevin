from pathlib import Path

import pytest

from opendevin import config
from opendevin.schema.config import ConfigType
from opendevin.action import fileop


def test_resolve_path():
    assert fileop.resolve_path('test.txt') == Path(config.get(ConfigType.WORKSPACE_BASE)) / 'test.txt'
    assert fileop.resolve_path('subdir/test.txt') == Path(config.get(ConfigType.WORKSPACE_BASE)) / 'subdir' / 'test.txt'
    assert fileop.resolve_path(Path(fileop.SANDBOX_PATH_PREFIX) / 'test.txt') == \
        Path(config.get(ConfigType.WORKSPACE_BASE)) / 'test.txt'
    assert fileop.resolve_path(Path(fileop.SANDBOX_PATH_PREFIX) / 'subdir' / 'test.txt') == \
        Path(config.get(ConfigType.WORKSPACE_BASE)) / 'subdir' / 'test.txt'
    assert fileop.resolve_path(Path(fileop.SANDBOX_PATH_PREFIX) / 'subdir' / '..' / 'test.txt') == \
        Path(config.get(ConfigType.WORKSPACE_BASE)) / 'test.txt'
    with pytest.raises(PermissionError):
        fileop.resolve_path(Path(fileop.SANDBOX_PATH_PREFIX) / '..' / 'test.txt')
    with pytest.raises(PermissionError):
        fileop.resolve_path(Path('..') / 'test.txt')
    with pytest.raises(PermissionError):
        fileop.resolve_path(Path('/') / 'test.txt')
