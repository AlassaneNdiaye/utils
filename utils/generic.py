import subprocess
from collections.abc import Iterable, Mapping
from typing import Any, Callable, Optional


def debug_decorator(func: Callable[..., Any]):
    def wrapper(*args, **kwargs):
        parameters = [str(arg) for arg in args]
        parameters.extend(
            [f"{k}={v}" for k, v in kwargs.items()]
        )
        parameters = ", ".join(parameters)

        print(f"Calling {func.__name__}({parameters})")
        return_value = func(*args, **kwargs)
        print(f"{func.__name__} returned {return_value}")

        return return_value
    return wrapper


def execute_command(command: str, remote: Optional[str] = None, remote_key_path: Optional[str] = None,
                    executable: str = "/bin/bash"):
    if remote is not None:
        if remote_key_path is not None:
            command = f'ssh {remote} -i {remote_key_path} "{command}"'
        else:
            command = f'ssh {remote} "{command}"'

    completed_process = subprocess.run(command, shell=True, executable=executable,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result = {
        "exit-code": completed_process.returncode,
        "stdout": completed_process.stdout.decode("utf-8").strip(),
        "stderr": completed_process.stderr.decode("utf-8").strip()
    }
    return result


def is_iterable(o: Any):
    return isinstance(o, Iterable)


def is_mapping(o: Any):
    return isinstance(o, Mapping)
