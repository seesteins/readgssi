import setuptools
import re
import os

# Function to read version from _version.py without importing the package
def find_version(*file_paths):
    """
    Reads the version string from the specified file path(s) relative to setup.py.
    Avoids importing the package.
    """
    base_dir = os.path.dirname(__file__)
    path_components = list(file_paths) # e.g., ["readgssi", "_version.py"]
    version_file_path = os.path.join(base_dir, *path_components)

    if not os.path.isfile(version_file_path):
        raise RuntimeError(f"Unable to find version file: {version_file_path}")

    try:
        with open(version_file_path, 'r') as f:
            version_file_content = f.read()
    except Exception as e:
        raise RuntimeError(f"Unable to read version file {version_file_path}: {e}")

    # Use regex to find the __version__ or version assignment
    version_match = re.search(r"^version\s*=\s*['\"]([^'\"]*)['\"]",
                              version_file_content, re.M)
    if version_match:
        return version_match.group(1)

    # Fallback check for __version__ (common practice)
    version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                              version_file_content, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError(f"Unable to find version string in {version_file_path}")


# Minimal setup.py focused on providing dynamic data (version)
# All static metadata should be in pyproject.toml
setuptools.setup(
    version=find_version("readgssi", "_version.py"),
    # Explicitly tell setuptools where to find the package if not using src-layout
    # Assumes 'readgssi' directory is at the same level as setup.py
    packages=setuptools.find_packages(where="."), # Or find_packages(include=['readgssi', 'readgssi.*'])
    package_dir={"": "."}, # Maps package name "" (root) to the current directory "."
)