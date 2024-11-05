import sys
import os
import warnings

from loguru import logger

from google.cloud import storage

warnings.filterwarnings(
    "ignore", message="Your application has authenticated using end user credentials"
)

# add color to loguru
logger.add(
    sys.stderr, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)


class GCSSymlinkHandler:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self._symlink_cache = {}  # Cache to prevent infinite recursion

    def _is_symlink(self, blob_name):
        return blob_name.endswith(".symlink")

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
        parts = path.split("/")
        resolved_parts = []

        for i, part in enumerate(parts):
            # Construct the current path being checked
            current_path = "/".join(resolved_parts + [part])

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
                resolved_parts = target.split("/")
            else:
                resolved_parts.append(part)

        return "/".join(resolved_parts)

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

    def ls(self, path):
        """
        List objects in the given path, resolving symlinks.
        """
        # Clear cache for each new ls operation
        self._symlink_cache = {}

        # Resolve the path first
        resolved_path = self._resolve_symlink_path(path.rstrip("/"))
        logger.info(f"Resolved path: {resolved_path}")
        prefix = resolved_path + "/" if resolved_path else ""
        logger.info(f"Prefix: {prefix}")

        items = []

        # Check for direct symlinks in the directory
        blobs = list(self.client.list_blobs(self.bucket, prefix=path.rstrip("/") + "/", delimiter="/"))
        symlink_blobs = [blob for blob in blobs if self._is_symlink(blob.name)]

        for symlink_blob in symlink_blobs:
            # Extract the symlink name without the .symlink extension
            symlink_name = os.path.basename(symlink_blob.name)[:-8]  # Remove '.symlink'
            target = self._get_symlink_target(symlink_blob)
            items.append(f"{symlink_name} -> {target}")

        # List blobs and prefixes in the resolved path
        blobs = list(self.client.list_blobs(self.bucket, prefix=prefix, delimiter="/"))
        prefixes = list(
            self.client.list_blobs(self.bucket, prefix=prefix, delimiter="/").prefixes
        )

        # Add subdirectories
        for p in prefixes:
            relative_name = os.path.relpath(p, prefix).rstrip("/")
            if "/" not in relative_name:
                items.append(relative_name + "/")

        # Add files
        for blob in blobs:
            name = blob.name
            if self._is_symlink(name):
                continue  # Skip symlink files in listing

            relative_name = os.path.relpath(name, prefix)
            if "/" not in relative_name:
                items.append(relative_name)

        logger.info(f"Items: {items}")
        return items

# Example Usage
if __name__ == "__main__":

    def try_read(handler, path):
        try:
            data = handler.read(path)
            print(f"Data at {path}: {data.decode('utf-8')}")
        except FileNotFoundError as e:
            print(e)

    bucket_name = "iamwrm1_cloudbuild"
    handler = GCSSymlinkHandler(bucket_name)

    def a():
        # Create symlinks
        handler.write_symlink("export/data/SZ.prod", "export/data/SZ.version12")

        # Write data to nested paths
        handler.write("export/data/SZ.version12/data1.txt", "v12data1")
        handler.write("export/data/SZ.version12/data2.txt", "v12data2")

        handler.write("export/data/SZ.version13/data1.txt", "v13data1")
        handler.write("export/data/SZ.version13/data2.txt", "v13data2")

        # should print v12data
        try_read(handler, "export/data/SZ.version12/data1.txt")
        try_read(handler, "export/data/SZ.version12/data2.txt")

        handler.write_symlink("export/data/SZ.prod", "export/data/SZ.version13")

        try_read(handler, "export/data/SZ.version13/data1.txt")
        try_read(handler, "export/data/SZ.version13/data2.txt")

    def b():
        # List contents of /export/data/
        print("Listing export/data/:")
        items = handler.ls("export/data/")
        for item in items:
            print(item)
        print("------")

        items = handler.ls("export/data/SZ.prod/")
        for item in items:
            print(item)

    # a()
    b()
