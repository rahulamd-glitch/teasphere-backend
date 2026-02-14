import hashlib

def generate_hash(prev_hash: str, data: str):
    raw = prev_hash + data
    return hashlib.sha256(raw.encode()).hexdigest()
