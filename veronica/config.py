from cmd import Cmd

class config(Cmd):
    def __init__(self, completekey: str = ..., stdin: IO[str] | None = ..., stdout: IO[str] | None = ...) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        