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
    result: dict[str, str] = {}
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigSyntaxError(f"line {lineno}: missing '='", line_number=lineno)
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            raise ConfigSyntaxError(f"line {lineno}: empty key", line_number=lineno)
        if key in result:
            raise ConfigDuplicateKeyError(f"duplicate key: {key}", key=key)
        result[key] = value
    return result
