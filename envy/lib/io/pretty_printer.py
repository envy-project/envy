import curses
import sys


class PrettyPrinter:
    """ Manages pretty printing to stdout using curses.
    """

    def __init__(self):
        self.screen = curses.initscr()
        self.steps = []
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.old_stdout = sys.stdout
        self.lines = []
        sys.stdout = self

    def end(self):
        """ End the curses window, return stdout to its initial state and print any final output.
        """

        curses.endwin()
        sys.stdout = self.old_stdout
        print(self.__get_final_step_text())

    def write(self, text: str):
        """ Override the default stdout write implementation.
        """

        text = text.rstrip()
        if text:
            self.lines.append(text)

    def isatty(self):
        """ Override the default stdout isatty implementaiton.
        """

        return False

    def fileno(self):
        """ Override the default stdout fileno implementaiton.
        """

        return 1

    def start_step(self, text: str):
        """ Start a new step. This step will be displayed as '. text' until end_step is called
        """

        self.steps.append({"text": text, "ended": False})
        self.__refresh()

    def end_step(self):
        """ End the most recently started step. Change that step's display from '. text' to '✓ text'.
        """

        self.steps[-1]["ended"] = True
        self.lines = []
        self.__refresh()

    def __refresh(self):
        """ Output the current steps and lines to curses, then refresh the curses window.
        """

        self.screen.clear()

        for i, step in enumerate(self.steps):
            if step.get("ended", False):
                self.screen.addch(i, 0, u"\u2713", curses.color_pair(1))
                self.screen.addstr(i, 2, step.get("text", ""), curses.color_pair(1))
            else:
                self.screen.addch(i, 0, ".", curses.color_pair(0))
                self.screen.addstr(i, 2, step.get("text", ""), curses.color_pair(0))

        for i, line in enumerate(self.lines[-10:]):
            self.screen.addstr(len(self.steps) + i, 0, line)

        self.screen.refresh()

    def __get_final_step_text(self):
        """ Combine steps for final output after ending hte curses window.
        """

        return "\n".join(
            ["{} {}".format(u"\u2713", step.get("text", "")) for step in self.steps]
        )
