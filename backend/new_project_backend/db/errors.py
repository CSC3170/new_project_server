from typing import Optional


class NotExistsError(Exception):
    pass


class DuplicateRecordError(Exception):
    def __init__(self, record: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record = record
