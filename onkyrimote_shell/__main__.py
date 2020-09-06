from kien import CommandError, create_commander
from kien.command import help, set
from kien.runner import ConsoleRunner
from onkyrimote.backend.pigpio import PiGPIOBackend
from onkyrimote.device.onkyo import TXSR304

from onkyrimote_shell.commands import onkyo, repeat


class Runner(ConsoleRunner):
    def __init__(self) -> None:
        super().__init__()
        self.onkyo = None

    def get_arg_parser(self):
        parser = super().get_arg_parser()
        parser.add_argument("--gpio", type=int, default=17)
        return parser

    def prompt(self):
        if self.console and self.console._last_status != 0:
            trailing = "!"
        else:
            trailing = "#"
        try:
            leading = "onkyrimote "
        except (OSError, CommandError):
            leading = ""
        return "{}{} ".format(leading, trailing)

    def configure(self) -> None:
        super().configure()
        commander = create_commander("onkyrimote")
        commander.compose(help.command, set.command, repeat.command, onkyo.command)
        commander.provide("onkyo", TXSR304(PiGPIOBackend(self.cli_args.gpio)))
        commander.provide("dispatch", commander.dispatch)
        self.commander = commander


def main():
    runner = Runner()
    runner.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
