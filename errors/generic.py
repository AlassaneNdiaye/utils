def unsupported_option_for_function(function: str, option_name: str, option_value: str) -> ValueError:
    return ValueError(f"The function '{function}' doesn't support the option {option_name}={option_value}.")


def unsupported_value_for_variable(variable: str, value: str) -> ValueError:
    return ValueError(f"The variable '{variable}' doesn't support the value '{value}'.")
