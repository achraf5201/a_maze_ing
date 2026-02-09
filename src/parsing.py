class Mazeconfig:
    """Loads maze configuration from a file into a parameter dictionary.

    Attributes:
        param (dict): Dictionary storing maze configuration parameters.
    """
    def __init__(self) -> None:
        """
        Initializes the Mazeconfig object with an empty parameter dictionary.
        """
        self.param: dict = {}

    def load_config(self, filename: str) -> dict:
        """Loads configuration parameters from a file.

        The configuration file should have lines in the format `KEY=VALUE`.
        Supports the following keys (case-insensitive):
            - WIDTH (int)
            - HEIGHT (int)
            - ENTRY (comma-separated integers)
            - EXIT (comma-separated integers)
            - OUTPUT_FILE (string)
            - PERFECT (TRUE/FALSE)

        Lines starting with `#` or empty lines are ignored.

        Args:
            filename (str): Path to the configuration file.

        Returns:
            dict: Dictionary containing parsed configuration parameters.
                  Returns an empty dictionary if the file cannot be read
                  or a line fails to parse.
        """
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        try:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()

                            if key.upper() in ("WIDTH", "HEIGHT"):
                                self.param[key] = int(value)
                            elif key.upper() in ("ENTRY", "EXIT"):
                                self.param[key] = [
                                    int(x.strip()) for x in value.split(",")]
                            elif key.upper() == "OUTPUT_FILE":
                                self.param[key] = value
                            elif key.upper() == "PERFECT":
                                self.param[key] = value.upper() == "TRUE"
                        except Exception as e:
                            print(f"Error parsing line '{line}': {e}")
                            return {}
            return self.param
        except Exception:
            print("ERROR: cannot open the file")
            return {}
