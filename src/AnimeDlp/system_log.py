# =============================================================================
# Log folder actions for the system-log board.
# requirement-python-oop — class SystemLog.
# The menu picture stays on requirement-python-tui.
# =============================================================================
from __future__ import annotations

from pathlib import Path



class SystemLog:
    """List, read, and empty the daily log files under logDir()."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="SystemLog")

    def log_dir(self) -> str:
        """General Purpose: The absolute log folder this logger already resolved."""
        if self.logger is None:
            return ""
        return str(self.logger.logDir())

    def log_files(self) -> list:
        """General Purpose: Regular .log files whose parent is that folder."""
        folder = self.log_dir()
        if not folder:
            return []
        root = Path(folder).resolve()
        if not root.is_dir():
            return []
        found = []
        for path in root.iterdir():
            owned = self._owned(path)
            if owned is not None:
                found.append(owned)
        found.sort(key=lambda item: item.name)
        return found

    def read_log(self, path):
        """General Purpose: Text of one owned log file. None when the path is refused."""
        owned = self._owned(path)
        if owned is None:
            return None
        self._note("read log", owned)
        return owned.read_text(encoding="utf-8", errors="replace")

    def clear_log(self, path) -> bool:
        """General Purpose: Empty one owned log file. The file stays on disk."""
        owned = self._owned(path)
        if owned is None:
            return False
        self._note("clear log", owned)
        with owned.open("w", encoding="utf-8"):
            pass
        return True

    def folder_text(self) -> str:
        """General Purpose: The result page for log-folder."""
        folder = self.log_dir()
        if not folder:
            return "No log folder."
        return "Log folder: {0}".format(folder)

    def _owned(self, path):
        """A regular .log file whose resolved parent is the log folder."""
        folder = self.log_dir()
        if not folder:
            return None
        root = Path(folder).resolve()
        try:
            candidate = Path(path).resolve()
        except OSError:
            return None
        if candidate.parent != root:
            return None
        if candidate.suffix != ".log":
            return None
        if not candidate.is_file():
            return None
        return candidate

    def _note(self, operation: str, path: Path) -> None:
        """One status line before the read or the empty. component menu."""
        if self.logger is None:
            return
        self.logger.log_message(
            "{0} path={1}".format(operation, path),
            component="menu",
        )
