# =============================================================================
# Run the text menu until Exit.
# requirement-python-oop — class MenuSession.
# MenuScreenError shares tui.py with class Tui.
# requirement-python-tui — one-second clock wait on the four boards.
# requirement-python-cli-language — a language pick writes the leaf.
# =============================================================================
from __future__ import annotations

from collections.abc import Callable

from .menu_model import MenuModel
from .menu_painter import MenuPainter



class MenuSession:
    """Run the text menu until row 9 Exit. Leaf commands return to the front board.

    on_kind returns "leave" to close the screen, a string to show a result page,
    or None to stay. This class does not draw the frame. MenuPainter does.
    """

    def __init__(
        self,
        app_name: str,
        version: str,
        on_version: Callable[[], str],
        on_about: Callable[[], str],
        boards: dict | None = None,
        on_kind: Callable[[str], str | None] | None = None,
        logger=None,
        painter=None,
    ) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuSession")
        self.app_name = app_name
        self.version = version
        self.on_version = on_version
        self.on_about = on_about
        self.on_kind = on_kind
        self.leave_kind = None
        if painter is None:
            self.painter = MenuPainter(logger=logger)
        else:
            self.painter = painter
        self.model = MenuModel(boards=boards, logger=logger, painter=self.painter)

    def leave_to_front(self) -> None:
        """Return the session to the front board. Does not leave the program."""
        self.model.show_front()

    def wait_key(self, screen):
        """One key, or None when the one-second clock wait ended with no key.

        A screen with no timeout keeps getch as it is. -1 stays end of input.
        requirement-python-tui rule 13. This wait is not a thread and not Esc.
        """
        arm = getattr(screen, "timeout", None)
        show_clock = (
            self.model.phase != "result"
            and self.model.layer in ("front", "self", "log", "lang")
        )
        if arm is not None:
            if show_clock:
                arm(1000)
            else:
                arm(-1)
        key = screen.getch()
        if key == -1 and show_clock and arm is not None:
            return None
        return key

    def run(self, screen) -> int:
        # Imported here so this module can load before tui.py finishes.
        from .tui import MenuScreenError

        screen.keypad(True)
        height, width = screen.getmaxyx()
        if not self.painter.screen_can_hold(height, width):
            raise MenuScreenError(
                "The text screen is too small for the menu and the input box.",
                logger=self.logger,
            )
        while True:
            self.painter.paint(screen, self.model, self.app_name, self.version)
            _height, _width = screen.getmaxyx()
            key = self.wait_key(screen)
            if key is None:
                continue
            action = self.model.apply_key(key, _height)
            if self.take_action(action) == "exit":
                return 0

    def take_action(self, action) -> str:
        """Run one committed kind. A language pick saves, then returns to the front board."""
        if action == "exit":
            return "exit"
        if isinstance(action, str) and action.startswith("set-"):
            message = self.painter.language.save(action[4:])
            self.model.show_front()
            self.model.notice = message
            return "stay"
        if action == "version":
            self.model.show_result(self.on_version())
            return "stay"
        if action == "about":
            self.model.show_result(self.on_about())
            return "stay"
        if action:
            outcome = self.on_kind(action) if self.on_kind is not None else None
            if outcome == "leave":
                self.leave_kind = action
                return "exit"
            if isinstance(outcome, str) and outcome:
                self.model.show_result(outcome)
        return "stay"
