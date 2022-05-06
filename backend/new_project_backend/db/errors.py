from typing import Optional


class NotExistsError(Exception):
    def __init__(self, name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name


class DuplicateRecordError(Exception):
    def __init__(self, name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
