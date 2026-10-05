# =============================================================================
# Host check for the about page.
# requirement-python-oop — class CheckSystem.
# requirement-python-about — line text and the pyenv and conda path reads.
# requirement-python-cli-logging — in_venv, in_pyenv, and in_conda read the one logger.
# =============================================================================
from __future__ import print_function, unicode_literals

import datetime
import os
import platform
import shutil
import sys
import sysconfig




class CheckSystem:
    """Reads for the [CHECK SYSTEM] block. One class, one module.

    The about composer calls this object. It does not own the star box.
    """

    def __init__(self, logger=None, app_name="", version="", console_name=""):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="CheckSystem")
        self.app_name = app_name
        self.version = version
        self.console_name = console_name

    def parse_sys_version(self, version_text, python_version):
        """
        General Purpose: Python display and C library string from sys.version.
        The C library line is the compiler token, such as GCC 13.3.0.
        """
        gcc = version_text
        if "\n" in gcc:
            gcc = gcc.split("\n", 1)[1]
        elif "[" in gcc and "]" in gcc:
            gcc = gcc.split("[", 1)[1].split("]", 1)[0]
        if gcc == "GCC":
            gcc = "[GCC]"
        if " (Red Hat" in gcc:
            gcc = gcc.split(" (Red Hat", 1)[0] + "]"
        probe = gcc if "[PyPy " in gcc else version_text
        if "[PyPy " in probe and "with" in probe:
            extra = probe.split("with", 1)[0].split("[", 1)[1].strip()
            python_version = "{} ({})".format(python_version, extra)
            gcc = "[" + probe.split("with ", 1)[1]
        shown = gcc.strip()
        if shown.startswith("[") and shown.endswith("]"):
            shown = shown[1:-1].strip()
        return python_version, shown

    def arch_label(self, version_text, machine=None):
        """General Purpose: amd64 / arm64 / x86 style name for this host."""
        if "AMD64" in version_text:
            return "amd64"
        if "AMD32" in version_text:
            return "x86"
        if machine is None:
            machine = platform.machine()
        mapped = {
            "x86_64": "amd64",
            "amd64": "amd64",
            "aarch64": "arm64",
            "arm64": "arm64",
            "i386": "x86",
            "i686": "x86",
            "x86": "x86",
        }
        return mapped.get(machine.lower(), machine)

    def libc_label(self, version_text, shell, detected=None):
        """General Purpose: libc token used in the binary type, such as glibc."""
        if detected is None:
            try:
                detected = platform.libc_ver()[0] or ""
            except Exception:
                detected = "unknown"
        name = detected
        if ("AMD64" in version_text or "AMD32" in version_text) and "MSC" in version_text:
            name = "msc"
        if "clang" in version_text.lower():
            name = "clang"
        if name == "" and shell == "/bin/ash":
            name = "muslc"
        return name

    def binary_type(self, arch, libc):
        """General Purpose: arch-libc token, such as amd64-glibc."""
        if arch == "":
            return ""
        if libc == "":
            return "{}-".format(arch)
        return "{}-{}".format(arch, libc)

    def current_user(self):
        """General Purpose: Login name for the about system check."""
        user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
        if user:
            return user
        try:
            import getpass
            return getpass.getuser()
        except Exception:
            return ""

    def shell_text(self):
        """General Purpose: The shell path from the environment."""
        return os.environ.get("SHELL") or ""

    def python_executable_name(self):
        """General Purpose: Basename of the running Python executable."""
        exe = sys.executable or ""
        if "/" in exe:
            return exe.rsplit("/", 1)[-1]
        if "\\" in exe:
            return exe.rsplit("\\", 1)[-1]
        return exe

    def command_location(self, name):
        """General Purpose: PATH location of a tool, or an empty string."""
        found = shutil.which(name)
        return found or ""

    def _has_pyenv_launcher(self, root):
        """True when bin/pyenv exists. The launcher may be a symlink."""
        return os.path.lexists(os.path.join(root, "bin", "pyenv"))

    def _pyenv_version_token(self, token):
        """One version segment. system, blanks, and path tricks are skipped."""
        if token in ("", "system", ".", ".."):
            return False
        if "/" in token or "\\" in token:
            return False
        return True

    def _pyenv_version_file_lines(self, root):
        path = os.path.join(root, "version")
        if not os.path.isfile(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return []
        return text.splitlines()

    def pyenv_root(self):
        """
        General Purpose: Pyenv root when bin/pyenv is present, else empty.
        A non-empty PYENV_ROOT is the only candidate. Otherwise ~/.pyenv.
        """
        named = os.environ.get("PYENV_ROOT")
        if named is not None and named.strip() != "":
            root = os.path.abspath(os.path.expanduser(named.strip()))
            if self._has_pyenv_launcher(root):
                return root
            return ""
        home = os.path.expanduser("~")
        if home == "" or home == "~":
            return ""
        root = os.path.abspath(os.path.join(home, ".pyenv"))
        if self._has_pyenv_launcher(root):
            return root
        return ""

    def in_venv(self):
        """General Purpose: True when the process logger reports a venv."""
        if self.logger is None:
            return False
        return self.logger.inVenv()

    def in_pyenv(self):
        """General Purpose: True when the process logger reports pyenv."""
        if self.logger is None:
            return False
        return self.logger.inPyenv()

    def in_conda(self):
        """General Purpose: True when the process logger reports conda."""
        if self.logger is None:
            return False
        return self.logger.inConda()

    def under_pyenv(self):
        """General Purpose: True when this check has a pyenv root."""
        return self.pyenv_root() != ""

    def pyenv_location(self):
        """
        General Purpose: The pyenv launcher at bin/pyenv.
        This is not the libexec file that can appear first on PATH.
        """
        root = self.pyenv_root()
        if root == "":
            return ""
        return os.path.join(root, "bin", "pyenv")

    def pyenv_version_names(self, root):
        """
        General Purpose: Selected pyenv versions, skipping system and path tricks.
        PYENV_VERSION wins over the root version file.
        """
        raw = os.environ.get("PYENV_VERSION")
        if raw is not None and raw.strip() != "":
            parts = raw.split(":")
        else:
            parts = self._pyenv_version_file_lines(root)
        names = []
        for part in parts:
            token = part.strip()
            if self._pyenv_version_token(token):
                names.append(token)
        return names

    def pyenv_interpreter(self, name):
        """
        General Purpose: python2 or python3 inside the pyenv root, or empty.
        A selected version bin wins. Otherwise the shim.
        """
        root = self.pyenv_root()
        if root == "":
            return ""
        for version in self.pyenv_version_names(root):
            candidate = os.path.join(root, "versions", version, "bin", name)
            if os.path.lexists(candidate):
                return candidate
        shim = os.path.join(root, "shims", name)
        if os.path.lexists(shim):
            return shim
        return ""

    def _conda_name_token(self, token):
        """One environment segment. Blanks and path tricks are skipped."""
        if token in ("", ".", ".."):
            return False
        if "/" in token or "\\" in token:
            return False
        return True

    def _has_conda_launcher(self, root):
        """True when bin/conda exists. The launcher may be a symlink."""
        return os.path.lexists(os.path.join(root, "bin", "conda"))

    def _root_from_conda_exe(self, exe):
        """Root when CONDA_EXE lives in bin or condabin. Otherwise empty."""
        path = os.path.abspath(os.path.expanduser(exe.strip()))
        parent = os.path.dirname(path)
        if os.path.basename(parent) not in ("bin", "condabin"):
            return ""
        root = os.path.dirname(parent)
        if self._has_conda_launcher(root):
            return root
        return ""

    def _root_from_conda_prefix(self, prefix):
        """Root when the prefix is the base or one envs segment. Otherwise empty."""
        path = os.path.abspath(os.path.expanduser(prefix.strip()))
        if self._has_conda_launcher(path):
            return path
        name = os.path.basename(path)
        envs = os.path.dirname(path)
        if os.path.basename(envs) != "envs":
            return ""
        if not self._conda_name_token(name):
            return ""
        root = os.path.dirname(envs)
        if self._has_conda_launcher(root):
            return root
        return ""

    def _prefix_inside_conda(self, root, prefix):
        """The prefix when it is the root or root/envs/<name>. Otherwise empty."""
        path = os.path.abspath(os.path.expanduser(prefix.strip()))
        root_abs = os.path.abspath(root)
        if path == root_abs:
            return path
        envs = os.path.join(root_abs, "envs")
        marker = envs + os.sep
        if not path.startswith(marker):
            return ""
        if not self._conda_name_token(path[len(marker):]):
            return ""
        return path

    def conda_root(self):
        """
        General Purpose: Conda root when bin/conda is present, else empty.
        A non-empty CONDA_EXE is the only candidate. Otherwise a non-empty
        CONDA_PREFIX. Otherwise the first login install that has bin/conda.
        """
        exe = os.environ.get("CONDA_EXE")
        if exe is not None and exe.strip() != "":
            return self._root_from_conda_exe(exe)
        prefix = os.environ.get("CONDA_PREFIX")
        if prefix is not None and prefix.strip() != "":
            return self._root_from_conda_prefix(prefix)
        home = os.path.expanduser("~")
        if home == "" or home == "~":
            return ""
        for name in ("miniconda3", "anaconda3", "miniforge3", "mambaforge"):
            root = os.path.abspath(os.path.join(home, name))
            if self._has_conda_launcher(root):
                return root
        return ""

    def under_conda(self):
        """General Purpose: True when this check has a conda root."""
        return self.conda_root() != ""

    def conda_location(self):
        """
        General Purpose: The conda launcher at bin/conda.
        This is not the condabin file that can appear first on PATH.
        """
        root = self.conda_root()
        if root == "":
            return ""
        return os.path.join(root, "bin", "conda")

    def conda_prefix(self):
        """
        General Purpose: Active conda prefix inside the root, else the root.
        Empty when the check is not under conda.
        """
        root = self.conda_root()
        if root == "":
            return ""
        named = os.environ.get("CONDA_PREFIX")
        if named is not None and named.strip() != "":
            inside = self._prefix_inside_conda(root, named)
            if inside != "":
                return inside
        return root

    def conda_interpreter(self, name):
        """
        General Purpose: python2 or python3 inside the conda prefix, or empty.
        An active prefix does not borrow the base interpreter.
        """
        prefix = self.conda_prefix()
        if prefix == "":
            return ""
        candidate = os.path.join(prefix, "bin", name)
        if os.path.lexists(candidate):
            return candidate
        return ""

    def about_tool_location(self, name):
        """
        General Purpose: Location line for python2, python3, conda, or pyenv.
        Under conda, python2 and python3 stay inside the prefix and conda is bin/conda.
        Otherwise under pyenv, those interpreters stay inside the pyenv root.
        """
        if name == "conda" and self.under_conda():
            return self.conda_location()
        if name == "pyenv" and self.under_pyenv():
            return self.pyenv_location()
        if name in ("python2", "python3") and self.under_conda():
            return self.conda_interpreter(name)
        if name in ("python2", "python3") and self.under_pyenv():
            return self.pyenv_interpreter(name)
        return self.command_location(name)

    def os_text(self):
        """General Purpose: Pretty operating-system name, such as Ubuntu 24.04 LTS."""
        try:
            info = platform.freedesktop_os_release()
        except Exception:
            info = {}
        pretty = info.get("PRETTY_NAME") or ""
        if pretty:
            return pretty
        return platform.platform()

    def inside_docker(self, marker="/.dockerenv"):
        """General Purpose: True when the docker marker file is present."""
        return os.path.exists(marker)

    def cpython_soabi(self):
        """General Purpose: CPython ABI string shown as the Cython string."""
        value = sysconfig.get_config_var("SOABI") or ""
        return value

    def process_id(self):
        """General Purpose: This process id as decimal text."""
        return str(os.getpid())

    def _home_dir(self):
        """HOME when set. Otherwise an absolute expanduser result. Else empty."""
        home = os.environ.get("HOME") or ""
        if home.strip():
            return home
        try:
            expanded = os.path.expanduser("~")
        except Exception:
            return ""
        if expanded and os.path.isabs(expanded):
            return expanded
        return ""

    def _cache_leaf(self, username, pid_text):
        """Preferred leaf. No empty username segment."""
        if username:
            return "cache-{}-{}-{}".format(self.app_name, username, pid_text)
        return "cache-{}-{}".format(self.app_name, pid_text)

    def cache_folder_preferred(self):
        """General Purpose: RAM cache candidate under /dev/shm/cache."""
        leaf = self._cache_leaf(self.current_user(), self.process_id())
        return os.path.join("/dev/shm", "cache", leaf)

    def cache_folder_first_fallback(self):
        """General Purpose: First cache fallback under /tmp/cache."""
        leaf = self._cache_leaf(self.current_user(), self.process_id())
        return os.path.join("/tmp", "cache", leaf)

    def cache_folder_second_fallback(self):
        """General Purpose: Second cache fallback. The leaf has no username."""
        home = self._home_dir()
        if not home:
            return ""
        leaf = "cache-{}-{}".format(self.app_name, self.process_id())
        return os.path.join(home, ".cache", leaf)

    def cache_folder_used(self):
        """
        General Purpose: Which cache candidate this run would use.
        Directory existence only. This read does not create the folder.
        """
        if os.path.isdir("/dev/shm"):
            return self.cache_folder_preferred()
        if os.path.isdir("/tmp"):
            return self.cache_folder_first_fallback()
        return self.cache_folder_second_fallback()

    def persistence_storage(self):
        """General Purpose: Durable data directory under the login home."""
        home = self._home_dir()
        if not home:
            return ""
        return os.path.join(home, ".local", self.app_name)

    def tty_interactive(self, stream=None):
        """General Purpose: yes when stdout is a terminal, otherwise no."""
        target = sys.stdout if stream is None else stream
        try:
            interactive = bool(target.isatty())
        except Exception:
            interactive = False
        return "yes" if interactive else "no"

    def self_location(self):
        """
        General Purpose: Path of the running program.
        A console-script argv wins. Otherwise the CLI module file.
        The about page names that program file, so this read stays on it.
        """
        here = os.path.realpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli.py")
        )
        argv0 = sys.argv[0] if sys.argv else ""
        if argv0 and os.path.isfile(argv0):
            argv_real = os.path.realpath(argv0)
            base = os.path.basename(argv_real)
            if base in (self.console_name, self.app_name):
                return argv_real
            same_dir = os.path.dirname(argv_real) == os.path.dirname(here)
            if same_dir and base in ("cli.py", "__main__.py"):
                return argv_real
        return here

    def check_system_lines(self, now=None):
        """
        General Purpose: Host check block for the about page.
        The stamp is local time with microseconds.
        """
        when = now if now is not None else datetime.datetime.now()
        stamp = when.strftime("%Y-%m-%d %H:%M:%S.%f")
        version_text = sys.version
        py_text, c_library = self.parse_sys_version(
            version_text, platform.python_version()
        )
        arch = self.arch_label(version_text)
        shell = self.shell_text()
        libc = self.libc_label(version_text, shell)
        rows = [
            "{} {}(v{})  [CHECK SYSTEM]:".format(stamp, self.app_name, self.version),
            "  Now checking your operation system!",
            "    Python: {}".format(py_text),
            "    C Library: {}".format(c_library),
            "    Operation System: {}".format(self.os_text()),
            "    Architecture: {}".format(arch),
            "    Current User: {}".format(self.current_user()),
            "    Shell: {}".format(shell),
            "    Python Executable: {}".format(self.python_executable_name()),
            "    python2 location: {}".format(self.about_tool_location("python2")),
            "    python3 location: {}".format(self.about_tool_location("python3")),
            "    conda location: {}".format(self.about_tool_location("conda")),
            "    pyenv location: {}".format(self.about_tool_location("pyenv")),
            "    Inside docker container: {}".format(self.inside_docker()),
            "    Cython String: {}".format(self.cpython_soabi()),
            "    Binary Type: {}".format(self.binary_type(arch, libc)),
            "    Location: {}".format(self.self_location()),
            "    PID: {}".format(self.process_id()),
            "    Cache folder used: {}".format(self.cache_folder_used()),
            "    Cache folder (preferred): {}".format(self.cache_folder_preferred()),
            "    Cache folder (1st fallback): {}".format(
                self.cache_folder_first_fallback()
            ),
            "    Cache folder (2nd fallback): {}".format(
                self.cache_folder_second_fallback()
            ),
            "    Persistence storage: {}".format(self.persistence_storage()),
            "    TTY / Interactive: {}".format(self.tty_interactive()),
        ]
        return rows
