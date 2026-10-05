#!/bin/sh
# requirement-python-packaging
# Maintainer verbs only. anime-dlp flags are not accepted here.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
cd "$ROOT"

PROJECT="AnimeDlp"

out_err() {
    printf '%s\n' "$1" >&2
}

read_version() {
    python3 - "$ROOT" <<'PY'
import os
import sys

root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "src"))
import AnimeDlp
sys.stdout.write(AnimeDlp.__version__)
PY
}

VERSION=$(read_version 2>/dev/null || true)

need_version() {
    if [ -z "$VERSION" ]; then
        out_err "ERROR: Cannot read the package version from src/AnimeDlp."
        out_err "   Next: set __version__ in src/AnimeDlp/__init__.py to match pyproject.toml, then ./build.sh version"
        exit 1
    fi
}

if [ -n "$VERSION" ]; then
    printf '%s\n' "$PROJECT build tool (v$VERSION)"
else
    printf '%s\n' "$PROJECT build tool (version unread)"
fi
printf '%s\n' "========================================"

show_help() {
    cat << EOF
Usage: ./build.sh <command>

Operational commands:
  help       Show this list (also: no command, -h, --help)
  version    Print the package version from this checkout
  setup      Install or upgrade build and twine for this python3
  clean      Remove build, dist, egg-info, and caches
  build      Build an sdist and a wheel into dist/
  upload     Upload dist/* . Does not build first
  git        Ask for one commit message, then stage, commit, and push
  tag        Create and push annotated tag v${VERSION:-unread}
  release    clean, then build, then upload, then tag
  all        Same chain as release
  test-install  Remove this project's pip install, then install this checkout

Test command:
  test       Run tests/run.sh. No extra arguments.

Examples:
  ./build.sh version
  ./build.sh build
  ./build.sh test
  ./build.sh test-install
  ./build.sh release
EOF
}

do_setup() {
    python3 -m pip install --upgrade build twine
}

do_clean() {
    rm -rf build dist .eggs .pytest_cache
    rm -rf AnimeDlp.egg-info src/AnimeDlp.egg-info src/*.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "._*" -delete 2>/dev/null || true
    printf '%s\n' "Clean complete"
}

do_build() {
    if ! python3 -m build --sdist --wheel --outdir dist/; then
        out_err "ERROR: Package build failed."
        out_err "   Next: ./build.sh setup"
        exit 1
    fi
    printf '%s\n' "Build complete -> dist/"
    ls -lh dist/
}

do_upload() {
    if ! python3 -m twine upload dist/*; then
        out_err "ERROR: Upload failed."
        out_err "   Next: ./build.sh build"
        exit 1
    fi
    printf '%s\n' "Upload finished for $PROJECT v$VERSION"
}

do_git() {
    if [ -t 0 ]; then
        printf '%s\n' "Enter commit message:"
        read -r message || message=""
    else
        IFS= read -r message || message=""
    fi
    if [ -z "$message" ]; then
        out_err "ERROR: Commit message is empty."
        out_err "   Next: ./build.sh git"
        exit 1
    fi
    git add .
    git commit -m "$message"
    git push
}

do_tag() {
    need_version
    TAG="v$VERSION"
    printf '%s\n' "Creating and pushing tag: $TAG"
    git tag -a "$TAG" -m "Release $TAG"
    git push origin "$TAG"
}

read_project_name() {
    python3 - "$ROOT" <<'PY'
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    sys.exit(1)

root = Path(sys.argv[1])
path = root / "pyproject.toml"
try:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
except OSError:
    sys.exit(1)
project = data.get("project")
if not isinstance(project, dict):
    sys.exit(1)
name = project.get("name")
if not isinstance(name, str) or not name.strip():
    sys.exit(1)
sys.stdout.write(name.strip())
PY
}

do_test_install() {
    name=$(read_project_name 2>/dev/null) || name=""
    if [ -z "$name" ]; then
        out_err "ERROR: Cannot read the project name from pyproject.toml."
        out_err "   Next: set [project].name, then ./build.sh test-install"
        exit 1
    fi
    if python3 -m pip show "$name" >/dev/null 2>&1; then
        printf '%s\n' "Removing previous install of $name"
        if ! python3 -m pip uninstall -y -- "$name"; then
            out_err "ERROR: Could not remove the installed copy."
            out_err "   Next: ./build.sh test-install"
            exit 1
        fi
    else
        printf '%s\n' "No previous install of $name"
    fi
    printf '%s\n' "Installing this checkout"
    if ! python3 -m pip install -- "$ROOT"; then
        out_err "ERROR: Local install failed."
        out_err "   Next: ./build.sh test-install"
        exit 1
    fi
}

cmd=${1:-}
case "$cmd" in
    -h|--help|help|"")
        show_help
        ;;
    version)
        need_version
        printf '%s\n' "$PROJECT build tool (v$VERSION)"
        ;;
    setup)
        do_setup
        ;;
    clean)
        do_clean
        ;;
    build)
        do_build
        ;;
    upload)
        do_upload
        ;;
    git)
        do_git
        ;;
    tag)
        do_tag
        ;;
    test)
        shift
        if [ "$#" -ne 0 ]; then
            out_err "ERROR: ./build.sh test takes no extra arguments."
            out_err "   Next: ./build.sh test"
            exit 1
        fi
        if [ ! -f ./tests/run.sh ]; then
            out_err "ERROR: tests/run.sh is not in this checkout."
            out_err "   Next: add the suite runner, then ./build.sh test"
            exit 1
        fi
        ./tests/run.sh
        ;;
    test-install)
        shift
        if [ "$#" -ne 0 ]; then
            out_err "ERROR: ./build.sh test-install takes no extra arguments."
            out_err "   Next: ./build.sh test-install"
            exit 1
        fi
        do_test_install
        ;;
    release|all)
        need_version
        do_clean
        do_build
        do_upload
        do_tag
        ;;
    *)
        out_err "ERROR: Unknown command: $cmd"
        show_help
        exit 1
        ;;
esac

printf '%s\n' "Done."
