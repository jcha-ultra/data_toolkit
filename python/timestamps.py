from datetime import datetime

def generate_timestamp_id():
    """
    Generate a timestamp ID in the format of YYYY-MM-DD-HHMM-SS-NNNNNN.
    """
    return datetime.utcnow().strftime('%Y-%m-%d_%H%M-%S-%f')
