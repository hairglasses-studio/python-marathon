class ConfigError(Exception):
    """Base for config parsing errors."""

class ConfigSyntaxError(ConfigError):
    def __init__(self, message: str, line_number: int) -> None:
        super().__init__(message)
        self.line_number = line_number

class ConfigDuplicateKeyError(ConfigError):
    def __init__(self, message: str, key: str) -> None:
        super().__init__(message)
        self.key = key


def parse_config(text: str) -> dict[str, str]:
    raise NotImplementedError("fill me in")
