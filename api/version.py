import subprocess  # noqa: S404
from collections import namedtuple


Version = namedtuple("Version", ["commit", "branch", "description"])

cmd = "(git rev-parse HEAD && (git symbolic-ref --short HEAD || echo) && git describe --tags --always) 2> /dev/null"


def get_version() -> Version:
    output = subprocess.getoutput(cmd + " || cat VERSION").splitlines()
    commit = output[0] if len(output) > 0 else "unknown"
    branch = output[1] if len(output) > 1 else "unknown"
    description = output[2] if len(output) > 2 else "unknown"
    return Version(commit, branch, description)


if __name__ == "__main__":
    print(subprocess.getoutput(cmd + " | tee VERSION"))
