from subprocess import run


def cmd(args: list[str]):
    result = run(args, capture_output=True, text=True)
    return result.stdout
