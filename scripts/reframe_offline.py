"""Fail closed when a test reaches an unmocked provider process or network call.

Local Git stays available. The guard installs only while unittest is already loaded,
so the installed command is unchanged.
"""
import os
import re
import socket
import subprocess
from pathlib import Path

BLOCKED_PROGRAMS = {'aws', 'claude', 'codex', 'terraform', 'tofu', 'uvx', 'kiro', 'kiro-cli'}
BLOCKED_HOSTS = ('amazonaws.com', 'anthropic.com', 'openai.com')
SHELLS = {'sh', 'bash', 'zsh', 'dash', 'ksh'}
WRAPPERS = {'env', 'nohup', 'nice', 'timeout', 'time', 'stdbuf', 'xargs', 'exec', 'command'}


def words(text):
    """Every word of a shell script, including words inside quotes and $(...) substitutions."""
    return [word for word in re.split(r'[\s;&|()<>`$"\'{}!\\]+', text) if word]


def install():
    """Replace process and socket entry points for the rest of this test process."""
    if getattr(install, 'active', False):
        return
    install.active = True
    real_popen = subprocess.Popen
    real_run = subprocess.run

    def argv_of(command):
        if isinstance(command, (list, tuple)):
            return [os.fsdecode(part) if isinstance(part, bytes) else str(part) for part in command]
        # A string is a shell command line (shell=True); any word may start a program.
        text = os.fsdecode(command) if isinstance(command, bytes) else str(command)
        return ['sh', '-c', text]

    def refuse_program(word):
        name = Path(word).name
        if name in BLOCKED_PROGRAMS or name.startswith('claude'):
            raise AssertionError('unmocked provider process: ' + name)

    def refuse(argv):
        if not argv:
            return
        refuse_program(argv[0])
        text = ' '.join(argv)
        for host in BLOCKED_HOSTS:
            if host in text:
                raise AssertionError('unmocked provider network request: ' + host)
        name = Path(argv[0]).name
        if name in WRAPPERS:
            for word in argv[1:]:
                refuse_program(word)
        if name in SHELLS:
            for index, flag in enumerate(argv[1:-1], 1):
                if flag.startswith('-') and not flag.startswith('--') and 'c' in flag:
                    for word in words(argv[index + 1]):
                        refuse_program(word)

    class GuardedPopen(real_popen):
        """Refuse a provider command, then start the real process. Git stays allowed."""

        def __init__(self, command, *args, **kwargs):
            refuse(argv_of(command))
            super().__init__(command, *args, **kwargs)

    def run(command, *args, **kwargs):
        refuse(argv_of(command))
        return real_run(command, *args, **kwargs)

    subprocess.Popen = GuardedPopen
    subprocess.run = run

    def connect(self, address):
        raise AssertionError('unmocked network request')

    socket.socket.connect = connect

    def connect_ex(self, address):
        raise AssertionError('unmocked network request')

    socket.socket.connect_ex = connect_ex

    def create_connection(*args, **kwargs):
        raise AssertionError('unmocked network request')

    socket.create_connection = create_connection
