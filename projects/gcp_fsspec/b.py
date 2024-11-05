import fsspec

import fsspec
from fsspec.spec import AbstractFileSystem
from fsspec.utils import infer_storage_options
import gcsfs
import os

class GCSSymlinkFileSystem(AbstractFileSystem):
    """
    A custom fsspec-compatible filesystem for GCS that supports symlinks.
    Symlinks are represented as files with a `.symlink` extension containing the target path.
    """

    def __init__(self, bucket_name, **kwargs):
        """
        Initialize the GCS Symlink Filesystem.

        Parameters:
            bucket_name (str): The name of the GCS bucket.
            **kwargs: Additional keyword arguments for gcsfs.GCSFileSystem.
        """
        self.bucket = bucket_name
        self.gcs_fs = gcsfs.GCSFileSystem(**kwargs)
        super().__init__(root_marker='/')

    def _symlink_path(self, path):
        """Convert a path to its corresponding symlink file path."""
        if path.endswith('/'):
            path = path.rstrip('/')
        return f"{path}.symlink"

    def _is_symlink(self, path):
        """Check if a path is a symlink."""
        symlink_blob = self._symlink_path(path)
        return self.gcs_fs.exists(symlink_blob)

    def _read_symlink(self, path):
        """Read the target path from a symlink."""
        symlink_blob = self._symlink_path(path)
        if not self.gcs_fs.exists(symlink_blob):
            raise FileNotFoundError(f"Symlink {path} does not exist.")
        with self.gcs_fs.open(symlink_blob, 'r') as f:
            target = f.read().strip()
        return target

    def _resolve_path(self, path, seen=None):
        """
        Resolve symlinks recursively.

        Parameters:
            path (str): The path to resolve.
            seen (set): Set of already seen paths to detect circular symlinks.

        Returns:
            str: The resolved path.
        """
        if seen is None:
            seen = set()
        if path in seen:
            raise RecursionError(f"Circular symlink detected at {path}")
        seen.add(path)

        if self._is_symlink(path):
            target = self._read_symlink(path)
            if not target.startswith('/'):
                # Relative symlink; resolve relative to the symlink's directory
                dir_path = os.path.dirname(path)
                target = os.path.normpath(os.path.join(dir_path, target))
            return self._resolve_path(target, seen)
        return path

    def ls(self, path, detail=True, **kwargs):
        """
        List directory contents, resolving symlinks.

        Parameters:
            path (str): The directory path to list.
            detail (bool): If True, return detailed info.

        Returns:
            list: A list of file or directory names or detailed dicts.
        """
        resolved_path = self._resolve_path(path.rstrip('/'))
        prefix = resolved_path + '/' if resolved_path else ''

        blobs = self.gcs_fs.ls(prefix, detail=detail, **kwargs)
        if detail:
            # Filter out symlink files
            blobs = [b for b in blobs if not b['name'].endswith('.symlink')]
        else:
            blobs = [b for b in blobs if not b.endswith('.symlink')]

        # If the original path was a symlink, include its target information
        if self._is_symlink(path.rstrip('/')):
            target = self._read_symlink(path.rstrip('/'))
            symlink_info = {
                'name': f"{path} -> {target}",
                'size': 0,
                'type': 'symlink'
            } if detail else f"{path} -> {target}"
            blobs.append(symlink_info)

        return blobs

    def ls_all(self, path_glob='**', detail=True, **kwargs):
        """
        List all directory contents using recursion.

        Parameters:
            path_glob (str): Glob pattern to match paths.
            detail (bool): If True, return detailed info.

        Returns:
            list: A list of file or directory names or detailed dicts.
        """
        return self.ls(path_glob, detail=detail, **kwargs)

    def open(self, path, mode='rb', **kwargs):
        """
        Open a file, resolving symlinks if necessary.

        Parameters:
            path (str): The file path to open.
            mode (str): The mode in which to open the file.

        Returns:
            file-like object: A file-like object for reading or writing.
        """
        resolved_path = self._resolve_path(path)
        if 'w' in mode:
            # When writing, ensure we're writing to the resolved path
            if self._is_symlink(path):
                print(f"Writing to symlink {path} -> {resolved_path}")
            return self.gcs_fs.open(resolved_path, mode, **kwargs)
        else:
            # Reading from the symlink target
            return self.gcs_fs.open(resolved_path, mode, **kwargs)

    def cat(self, path, **kwargs):
        """
        Concatenate and return file contents, resolving symlinks.

        Parameters:
            path (str): The file path to read.

        Returns:
            bytes or str: The contents of the file.
        """
        resolved_path = self._resolve_path(path)
        return self.gcs_fs.cat(resolved_path, **kwargs)

    def exists(self, path):
        """
        Check if a path exists, considering symlinks.

        Parameters:
            path (str): The path to check.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        try:
            self._resolve_path(path)
            return True
        except (FileNotFoundError, RecursionError):
            return False

    def makedir(self, path, **kwargs):
        """
        Create a directory. In GCS, directories are implicit, so this is a no-op.

        Parameters:
            path (str): The directory path to create.

        Returns:
            None
        """
        # GCS is a flat filesystem. Directories are inferred from object prefixes.
        # Optionally, you can create a zero-byte object with a trailing slash.
        if not path.endswith('/'):
            path += '/'
        self.gcs_fs.touch(path, **kwargs)

    def mkdirs(self, path, exist_ok=True, **kwargs):
        """
        Recursively create directories.

        Parameters:
            path (str): The directory path to create.
            exist_ok (bool): If False, raise an error if the directory exists.

        Returns:
            None
        """
        # Similar to makedir in GCS. Ensure all prefixes exist.
        parts = path.split('/')
        for i in range(1, len(parts)+1):
            sub_path = '/'.join(parts[:i]) + '/'
            if not self.gcs_fs.exists(sub_path):
                self.gcs_fs.touch(sub_path, **kwargs)
            elif not exist_ok:
                raise FileExistsError(f"Directory {sub_path} already exists.")

    def rm_file(self, path):
        """
        Remove a file, resolving symlinks.

        Parameters:
            path (str): The file path to remove.

        Returns:
            None
        """
        resolved_path = self._resolve_path(path)
        self.gcs_fs.rm(resolved_path)

    def rm_dir(self, path):
        """
        Remove a directory, resolving symlinks.

        Parameters:
            path (str): The directory path to remove.

        Returns:
            None
        """
        resolved_path = self._resolve_path(path)
        self.gcs_fs.rm(resolved_path, recursive=True)

    def symlink(self, source, target):
        """
        Create a symlink at `source` pointing to `target`.

        Parameters:
            source (str): The symlink path.
            target (str): The target path the symlink points to.

        Returns:
            None
        """
        with self.gcs_fs.open(self._symlink_path(source), 'w') as f:
            f.write(target)

    def unlink(self, path):
        """
        Remove a symlink or a file.

        Parameters:
            path (str): The path to remove.

        Returns:
            None
        """
        symlink_blob = self._symlink_path(path)
        if self.gcs_fs.exists(symlink_blob):
            self.gcs_fs.rm(symlink_blob)
        else:
            self.gcs_fs.rm(path)

    def get_symlink_target(self, path):
        """
        Get the target of a symlink.

        Parameters:
            path (str): The symlink path.

        Returns:
            str: The target path.
        """
        if self._is_symlink(path):
            return self._read_symlink(path)
        else:
            raise ValueError(f"Path {path} is not a symlink.")

    # Implement other necessary abstract methods or delegate to gcs_fs as needed.
    # For simplicity, many methods can be directly delegated to the underlying gcs_fs.

    def info(self, path, **kwargs):
        """
        Get information about a file or directory, resolving symlinks.

        Parameters:
            path (str): The path to inspect.

        Returns:
            dict: A dictionary with file information.
        """
        resolved_path = self._resolve_path(path)
        return self.gcs_fs.info(resolved_path, **kwargs)

    def cp_file(self, path1, path2):
        """
        Copy a file from path1 to path2, resolving symlinks.

        Parameters:
            path1 (str): Source path.
            path2 (str): Destination path.

        Returns:
            None
        """
        resolved_source = self._resolve_path(path1)
        self.gcs_fs.copy(resolved_source, path2)

    def mv_file(self, path1, path2):
        """
        Move a file from path1 to path2, resolving symlinks.

        Parameters:
            path1 (str): Source path.
            path2 (str): Destination path.

        Returns:
            None
        """
        resolved_source = self._resolve_path(path1)
        self.gcs_fs.move(resolved_source, path2)

    def __repr__(self):
        return f"GCSSymlinkFileSystem(bucket_name='{self.bucket}')"

# Register the filesystem with fsspec
fsspec.register_implementation("gcs_symlink", GCSSymlinkFileSystem)

def main(bucket_name: str):
    # Initialize the custom filesystem
    fs = fsspec.filesystem('gcs_symlink', bucket_name=bucket_name)

    # Create directories
    fs.makedirs('export/data/SZ.version12/data_1', exist_ok=True)
    fs.makedirs('export/data/SZ.version12/data_2', exist_ok=True)

    # Write files
    fs.write('export/data/SZ.version12/data_1/data_3.txt', 'Content of data_3')
    fs.write('export/data/SZ.version12/data_2/data_4.txt', 'Content of data_4')

    # Create a symlink: /export/data/SZ.prod -> /export/data/SZ.version12
    fs.symlink('export/data/SZ.prod', 'export/data/SZ.version12')

    # List contents of /export/data/
    print("Listing export/data/:")
    for item in fs.ls('export/data/', detail=True):
        print(item)

    # Read data via symlink
    data_path = 'export/data/SZ.prod/data_1/data_3.txt'
    with fs.open(data_path, 'r') as f:
        content = f.read()
        print(f"\nContent of {data_path}: {content}")

    # List contents via symlink
    print("\nListing export/data/SZ.prod/:")
    for item in fs.ls('export/data/SZ.prod/', detail=True):
        print(item)

    # Verify existence
    print("\nDoes 'export/data/SZ.prod/data_1/data_3.txt' exist?", fs.exists(data_path))
    print("Does 'export/data/SZ.prod.symlink' exist?", fs.exists('export/data/SZ.prod.symlink'))

    # Get symlink target
    target = fs.get_symlink_target('export/data/SZ.prod')
    print(f"\nSymlink 'export/data/SZ.prod' points to '{target}'")

if __name__ == '__main__':
    main('iamwrm1_cloudbuild')
