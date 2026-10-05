# =============================================================================
# Pip lifecycle for the self-management verbs.
# requirement-python-oop — class SelfManage.
# requirement-python-cli-interface — version-check and self-update call pip.
# =============================================================================
from __future__ import annotations

import subprocess
import sys




class SelfManage:
    """Local version plus the pip commands for this package.

    Shell products keep a download channel. This class is the Python path:
    version-check and self-update call pip, and so do self-install and
    self-uninstall. It does not call sudo and it does not use curl.
    """

    DISTRIBUTION = "AnimeDlp"

    def __init__(self, app_name: str, version: str, runner=None, logger=None) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="SelfManage")
        self.app_name = app_name
        self.version = version
        self.runner = runner or self._subprocess_runner

    def local_version(self) -> str:
        """General Purpose: Installed name and version. No network."""
        return "{} {}".format(self.app_name, self.version)

    def argv_for(self, verb: str) -> list:
        """General Purpose: The pip command for one self-management verb."""
        py = sys.executable
        dist = self.DISTRIBUTION
        if verb == "version-check":
            return [py, "-m", "pip", "index", "versions", dist]
        if verb == "self-update":
            return [py, "-m", "pip", "install", "--upgrade", dist]
        if verb == "self-install":
            return [py, "-m", "pip", "install", dist]
        if verb == "self-uninstall":
            return [py, "-m", "pip", "uninstall", "-y", dist]
        raise ValueError(verb)

    def run_pip(self, verb: str) -> tuple:
        """General Purpose: Run that pip command and return the exit code and text."""
        argv = self.argv_for(verb)
        code, out, err = self.runner(argv)
        chunks = ["$ {}".format(" ".join(argv))]
        if verb == "version-check":
            chunks.insert(0, self.local_version())
        if out and out.strip():
            chunks.append(out.strip())
        if err and err.strip():
            chunks.append(err.strip())
        if code != 0 and not (out and out.strip()) and not (err and err.strip()):
            chunks.append("pip exited {}".format(code))
        return code, "\n".join(chunks)

    def emit(self, verb: str) -> int:
        """General Purpose: Print the pip result on the console. Does not open the menu."""
        code, text = self.run_pip(verb)
        print(text)
        return code

    def _subprocess_runner(self, argv: list) -> tuple:
        """General Purpose: One pip child. stdin is closed so the child cannot wait."""
        done = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        return done.returncode, done.stdout or "", done.stderr or ""
