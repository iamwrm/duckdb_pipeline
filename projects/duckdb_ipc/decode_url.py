from urllib.parse import urlparse

def parse_gs_path(gs_url):
    parsed = urlparse(gs_url)
    bucket = parsed.netloc
    prefix = parsed.path.lstrip('/')
    return bucket, prefix

# Example usage
gs_path1 = "gs://a/b/c.txt"
gs_path2 = "gs://a/b/d/"

bucket1, prefix1 = parse_gs_path(gs_path1)
bucket2, prefix2 = parse_gs_path(gs_path2)

print(f"Path 1: bucket={bucket1}, prefix={prefix1}")
print(f"Path 2: bucket={bucket2}, prefix={prefix2}")