import os
import shutil
import subprocess
import time
from multiprocessing import Process
from typing import Any, Callable

import uvicorn  # type: ignore
from watchdog.events import RegexMatchingEventHandler  # type: ignore
from watchdog.observers import Observer  # type: ignore


class Task:
    class _EventHandler(RegexMatchingEventHandler):
        def __init__(
            self,
            on_changed: Callable[[], Any],
            regexes: list[str] = None,
            ignore_regexes: list[str] = None,
            ignore_directories: bool = False,
            case_sensitive: bool = False,
        ):
            super().__init__(regexes, ignore_regexes, ignore_directories, case_sensitive)
            self._on_changed = on_changed

        def on_created(self, _):
            self._on_changed()

        def on_deleted(self, _):
            self._on_changed()

        def on_modified(self, _):
            self._on_changed()

        def on_moved(self, _):
            self._on_changed()

    def __init__(
        self,
        prepare: Callable[[], Any],
        run: Callable[[], Any],
        path: str,
        regexes: list[str] = None,
        ignore_regexes: list[str] = None,
        recursive: bool = False,
        ignore_directories: bool = False,
        case_sensitive: bool = False,
    ):
        self._prepare = prepare
        self._run = run
        self._observer = Observer()
        self._runner = Process()
        self._path = path
        self._regexes = regexes
        self._ignore_regexes = ignore_regexes
        self._recursive = recursive
        self._ignore_directories = ignore_directories
        self._case_sensitive = case_sensitive

    def __del__(self):
        self.stop()

    def stop(self):
        if self._runner is not None and self._runner.is_alive():
            self._runner.terminate()
        if self._observer is not None and self._observer.is_alive():
            self._observer.stop()

    def start(self):
        self._prepare()
        self._observer = Observer()
        self._observer.schedule(
            self._EventHandler(
                self.restart, self._regexes, self._ignore_regexes, self._ignore_directories, self._case_sensitive
            ),
            self._path,
            self._recursive,
        )
        self._observer.start()
        self._runner = Process(target=self._run)
        self._runner.start()
        self._observer.join()
        self._runner.join()

    def restart(self):
        self.stop()
        self.start()


def print_title(title: str):
    term_width, _ = shutil.get_terminal_size()
    print(title.center(len(title) + 2, ' ').center(term_width, '='), flush=True)


def print_horizontal():
    term_width, _ = shutil.get_terminal_size()
    print('=' * term_width, flush=True)


def print_empty_line():
    print(flush=True)


SOURCE_DIR = 'new_project_backend'


def lint():
    time.sleep(1)
    print_title('mypy')
    subprocess.run(['stubgen', SOURCE_DIR, '-o', 'stubs'], stderr=subprocess.STDOUT, check=False)
    subprocess.run(
        ['mypy', '-p', SOURCE_DIR],
        stderr=subprocess.STDOUT,
        env=dict(os.environ, MYPYPATH=f'{SOURCE_DIR}/stubs'),
        check=False,
    )
    print_empty_line()
    print_title('pylint')
    subprocess.run(['pylint', SOURCE_DIR], stderr=subprocess.STDOUT, check=False)
    print_empty_line()
    print_title('flake8')
    subprocess.run(['flake8', SOURCE_DIR], stderr=subprocess.STDOUT, check=False)
    print_empty_line()
    print_title('isort')
    subprocess.run(['isort', SOURCE_DIR], stderr=subprocess.STDOUT, check=False)
    print_empty_line()
    print_title('black')
    subprocess.run(['black', SOURCE_DIR], stderr=subprocess.STDOUT, check=False)
    print_empty_line()


def start():
    print_title('uvicorn')
    try:
        uvicorn.run('new_project_backend.app:app', host='0.0.0.0', port=8000)
    finally:
        print_horizontal()
        print_empty_line()


def watch():
    Task(lint, start, SOURCE_DIR, ignore_regexes=['.*__pycache__.*'], recursive=True).start()
