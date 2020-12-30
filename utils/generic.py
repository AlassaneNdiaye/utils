import collections.abc
import subprocess
from shlex import quote
from typing import Callable, Hashable, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Union


def debug_decorator(func: Callable[..., object]):
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
        command = quote(command)
        remote = quote(remote)
        if remote_key_path is not None:
            remote_key_path = quote(remote_key_path)
            command = f'ssh {remote} -i {remote_key_path} {command}'
        else:
            command = f'ssh {remote} {command}'

    completed_process = subprocess.run(command, shell=True, executable=executable,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result = {
        "exit-code": completed_process.returncode,
        "stdout": completed_process.stdout.decode("utf-8").strip(),
        "stderr": completed_process.stderr.decode("utf-8").strip()
    }

    return result


def get_nested_attribute(o: object, attributes: Sequence[str], default: object = None):
    return_value = o
    for attribute in attributes:
        if not hasattr(return_value, attribute):
            return default
        return_value = getattr(return_value, attribute)
    return return_value


def get_nested_value_from_dictionary(d: Mapping, keys: Sequence[Hashable], default: object = None):
    return_value = d
    for k in keys:
        if not isinstance(return_value, collections.abc.Mapping) or k not in return_value:
            return default
        return_value = return_value[k]
    return return_value


def is_iterable(o: object) -> bool:
    return isinstance(o, collections.abc.Iterable)


def is_mapping(o: object) -> bool:
    return isinstance(o, collections.abc.Mapping)


def recursive_replace(o: Union[MutableMapping, MutableSequence], variables: Mapping[str, str]) -> None:
    def recurse(nested_object):
        if isinstance(nested_object, collections.abc.MutableMapping):
            keys = nested_object.keys()
        else:
            keys = range(len(nested_object))
        for k in keys:
            v = nested_object[k]
            if isinstance(v, collections.abc.MutableMapping) or isinstance(v, collections.abc.MutableSequence):
                recurse(v)
            else:
                if isinstance(v, str):
                    nested_object[k] = v.format(**variables)
    recurse(o)
