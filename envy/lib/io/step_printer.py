ENDC = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


class StepPrinter:
    """ Manages printing progress steps to stdout.
    """

    def __init__(self):
        self.current_step = ""

    def start_step(self, step: str):
        """ Start a new step, printing 'step ...'
        """

        self.current_step = step
        print("{}{} ...{}".format(YELLOW, self.current_step, ENDC))

    def end_step(self):
        """ End the most recently started step, printing 'step ✓'.
        """

        print("{}{} {}{}".format(GREEN, self.current_step, u"\u2713", ENDC))
        self.current_step = ""

    def error(self, code):
        """ Print the most recently started step with an error code
        """

        print(
            "{}{} exited with error code {} {}{}".format(
                RED, self.current_step, code, u"\u2717", ENDC
            )
        )
        self.current_step = ""
