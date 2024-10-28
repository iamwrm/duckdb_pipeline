# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fsspec",
#     "gcsfs",
# ]
# ///
import fsspec

fs = fsspec.filesystem('gcs')

print(fs.ls('gs://iamwrm1_cloudbuild/source'))