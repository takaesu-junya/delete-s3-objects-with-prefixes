
# How to use it


```bash
$ python3 delete-s3-objects-with-prefixes.py -h
usage: delete-s3-objects-with-prefixes.py [-h] [--live] bucket prefixes

Delete S3 objects with specific prefixes.

positional arguments:
  bucket      Target bucket
  prefixes    Target prefixes, comma-separated. Each prefix starts without a slash. Example: folder1/folder2,folder3/folder4

options:
  -h, --help  show this help message and exit
  --live      Enable live run
```
