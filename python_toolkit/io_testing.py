
# `/dev/urandom` can be used to test IO operations without having to set up files.
with open('/dev/urandom', 'rb') as f:
    a = f.read(100000000)
