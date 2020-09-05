import os

# Setting root path
ROOT = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(ROOT, "fixtures")
SANDBOX_PATH = os.path.join(ROOT, "sandbox")


def get_fixture_path(path):
    return os.path.join(FIXTURES_PATH, path)


def get_sandbox_path(path):
    return os.path.join(SANDBOX_PATH, path)


def safe_remove(path):
    if os.path.exists(path):
        os.remove(path)


def safe_rmdir(path):
    if os.path.exists(path):
        os.rmdir(path)
