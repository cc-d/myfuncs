import subprocess as subproc
from typing import Optional, List, Union



def runcmd(cmd: str, output: bool = True, *args, **kwargs) -> Optional[List[str]]:
    """
    Run a command in the shell.

    Args:
        cmd (str): The command to be executed.
        output (bool, optional): Specifies whether to capture and return the output of the command.
            Defaults to True.
        *args: Additional positional arguments to be passed to subprocess.run().
        **kwargs: Additional keyword arguments to be passed to subprocess.run().

    Returns:
        Optional[List[str]]: The captured output of the command as a list of lines if `output` is True.
            None if `output` is False.

    Raises:
        CalledProcessError: If the command exits with a non-zero status and `check=True`.

    """
    if output:
        return subproc.run(
            [c for c in cmd.split()],
            check=True, text=True, capture_output=True, *args, **kwargs
        ).stdout.splitlines()
    else:
        subproc.run(
            [c for c in cmd.split()],
            check=False, text=False, capture_output=False, *args, **kwargs
        )

