from datetime import datetime

class UpdateTimeDict(dict):
    """A dictionary that keeps track of when each of its values was last set."""
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.update_record: dict = {}

    def __setitem__(self, key, val):
        super().__setitem__(key, val)
        self.update_record[key] = datetime.utcnow().isoformat()