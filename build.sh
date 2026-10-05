#!/bin/sh
set -eu

# =============================================
# AnimeDlp build & release script
# Pure POSIX sh — by Wong Chun Fai (wilgat)
# =============================================

PROJECT="AnimeDlp"

# Get version from pyproject.toml (reliable for [project] table)
VERSION=$(python3 -c '
import tomllib
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data.get("project", {}).get("version", "unknown"))
' 2>/dev/null) || VERSION="unknown"

echo "AnimeDlp build tool (v$VERSION)"
echo "========================================"

show_help() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  setup      Install/update build tools (build, twine, pytest)
  clean      Remove ALL build artifacts, caches, and egg-info
  build      Build sdist + wheel
  upload     Upload to PyPI using twine
  git        git add . → commit → push
  tag        Create and push git tag v\$VERSION
  release    Full release: clean → build → upload → tag
  test       Run pytest (extra args passed through)

Examples:
  ./build.sh release
  ./build.sh test -v -k "download"
  ./build.sh test test/specific_test.py
EOF
}

do_setup() {
    echo "Installing/upgrading build tools..."
    pip3 install --upgrade build twine pytest tomli
}

do_clean() {
    echo "Cleaning project (including all egg-info)..."
    rm -rf build dist .eggs .pytest_cache __pycache__
    rm -rf "${PROJECT}.egg-info" "src/${PROJECT}.egg-info" "src/${PROJECT}.*.egg-info" 2>/dev/null || true
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "._*" -delete 2>/dev/null || true
    echo "Clean complete."
}

do_build() {
    echo "Building sdist and wheel..."
    python3 -m build --sdist --wheel --outdir dist/
    echo "Build successful → dist/"
    ls -lh dist/
}

do_upload() {
    echo "Uploading to PyPI..."
    twine upload dist/*
    echo ""
    echo "SUCCESS: $PROJECT v$VERSION is now on PyPI!"
    echo "→ https://pypi.org/project/$PROJECT/$VERSION/"
}

do_git() {
    git add .
    echo "Enter commit message:"
    read -r message
    git commit -m "$message"
    git push
    echo "Changes pushed."
}

do_tag() {
    if [ "$VERSION" = "unknown" ]; then
        echo "ERROR: Could not determine version from pyproject.toml"
        exit 1
    fi
    TAG="v$VERSION"
    echo "Creating and pushing tag: $TAG"
    git tag -a "$TAG" -m "Release $TAG"
    git push origin "$TAG"
    echo "Tag $TAG pushed successfully!"
}

do_test() {
    echo "Running test suite..."
    if ! command -v pytest >/dev/null 2>&1; then
        echo "Installing pytest temporarily..."
        python3 -m pip install --quiet pytest
    fi
    export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/src"
    python3 -m pytest test/ "$@"
}

# Main dispatcher
case "${1:-}" in
    setup)     do_setup ;;
    clean)     do_clean ;;
    build)     do_build ;;
    upload)    do_upload ;;
    git)       do_git ;;
    tag)       do_tag ;;
    test)      shift; do_test "$@" ;;
    release|all)
        do_clean
        do_build
        do_upload
        do_tag
        ;;
    -h|--help|"") show_help ;;
    *) echo "Unknown command: $1"; show_help; exit 1 ;;
esac

echo "Done."