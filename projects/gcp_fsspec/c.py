import os
import warnings

from google.cloud import storage

warnings.filterwarnings('ignore', message='Your application has authenticated using end user credentials')


class GCSSymlinkHandler:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self._symlink_cache = {}  # Cache to prevent infinite recursion

    def _is_symlink(self, blob_name):
        return blob_name.endswith('.symlink')

    def _get_symlink_target(self, symlink_blob):
        content = symlink_blob.download_as_text().strip()
        return content

    def _resolve_symlink_path(self, path):
        """
        Recursively resolve symlinks in the path, handling symlinks at any level.
        """
        # Prevent infinite recursion
        if path in self._symlink_cache:
            return path

        # Split the path into components
        parts = path.split('/')
        resolved_parts = []

        for i, part in enumerate(parts):
            # Construct the current path being checked
            current_path = '/'.join(resolved_parts + [part])
            
            # Check if the current path is a symlink
            symlink_blob = self.bucket.blob(f"{current_path}.symlink")
            
            if symlink_blob.exists():
                # Resolve the symlink
                target = self._get_symlink_target(symlink_blob)
                
                # Update the cache to prevent infinite recursion
                self._symlink_cache[current_path] = target
                
                # If this is the last part, return the full resolved path
                if i == len(parts) - 1:
                    return target
                
                # Otherwise, replace the current part with the symlink target
                # and continue resolving the rest of the path
                resolved_parts = target.split('/')
            else:
                resolved_parts.append(part)

        return '/'.join(resolved_parts)

    def ls(self, path):
        """
        List objects in the given path, resolving symlinks.
        """
        # Clear cache for each new ls operation
        self._symlink_cache = {}
        
        resolved_path = self._resolve_symlink_path(path.rstrip('/'))
        prefix = resolved_path + '/' if resolved_path else ''

        blobs = self.client.list_blobs(self.bucket, prefix=prefix, delimiter='/')
        items = []
        for blob in blobs:
            name = blob.name
            if self._is_symlink(name):
                continue  # Skip symlink files in listing
            relative_name = os.path.relpath(name, prefix)
            if '/' not in relative_name:
                items.append(relative_name)
        
        # Check for symlinks in the original path
        symlink_path = path.rstrip('/')
        symlink_blob = self.bucket.blob(f"{symlink_path}.symlink")
        if symlink_blob.exists():
            target = self._get_symlink_target(symlink_blob)
            items.append(f"{symlink_path} -> {target}")
        
        return items

    def read(self, path):
        """
        Read the content of the object at the given path, resolving symlinks.
        """
        # Clear cache for each new read operation
        self._symlink_cache = {}
        
        resolved_path = self._resolve_symlink_path(path)
        blob = self.bucket.blob(resolved_path)
        
        if not blob.exists():
            raise FileNotFoundError(f"Object {resolved_path} does not exist.")
        
        return blob.download_as_bytes()

    def write_symlink(self, symlink_path, target_path):
        """
        Create a symlink by writing a symlink file.
        """
        symlink_blob = self.bucket.blob(f"{symlink_path}.symlink")
        symlink_blob.upload_from_string(target_path)
        print(f"Symlink created: {symlink_path} -> {target_path}")

    def write(self, path, data, is_symlink=False, target_path=None):
        """
        Write data to the given path. If is_symlink is True, create a symlink.
        """
        if is_symlink:
            if not target_path:
                raise ValueError("Target path must be provided for symlinks.")
            self.write_symlink(path, target_path)
        else:
            blob = self.bucket.blob(path)
            blob.upload_from_string(data)
            print(f"Data written to {path}")


# Example Usage
if __name__ == "__main__":
    bucket_name = 'iamwrm1_cloudbuild'
    handler = GCSSymlinkHandler(bucket_name)

    # Create symlinks
    handler.write_symlink('export/data/SZ.prod', 'export/data/SZ.version12')

    # List contents of /export/data/
    print("Listing export/data/:")
    items = handler.ls('export/data/')
    for item in items:
        print(item)

    # Write data to nested paths
    handler.write('export/data/SZ.version12/data.txt', 'v12data')
    handler.write('export/data/SZ.version13/data.txt', 'v13data')

    # Read data through multiple levels of symlinks
    data_path = 'export/data/SZ.prod/data.txt'
    try:
        data = handler.read(data_path)
        print(f"Data at {data_path}: {data.decode('utf-8')}")
    except FileNotFoundError as e:
        print(e)

    handler.write_symlink('export/data/SZ.prod', 'export/data/SZ.version13')


    # Read data through multiple levels of symlinks
    data_path = 'export/data/SZ.prod/data.txt'
    try:
        data = handler.read(data_path)
        print(f"Data at {data_path}: {data.decode('utf-8')}")
    except FileNotFoundError as e:
        print(e)