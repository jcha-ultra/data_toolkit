# generate a filename-safe timestamp id
from datetime import datetime
def generate_timestamp_id():
    return datetime.utcnow().strftime('%Y-%m-%d_%H%M-%S-%f')
