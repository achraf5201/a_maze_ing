class Mazeconfig:
    """Loads maze configuration from a file into a parameter dictionary."""
    
    def __init__(self) -> None:
        self.param: dict = {}

    def load_config(self, filename: str) -> dict:
        """Loads configuration parameters from a file."""
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        try:
                            key, value = line.split("=", 1)
                            key = key.strip().upper()
                            value = value.strip()

                            if key in ("WIDTH", "HEIGHT"):
                                self.param[key] = int(value)
                            elif key in ("ENTRY", "EXIT"):
                                # Convert to tuple for consistency with type hints
                                coords = [int(x.strip()) for x in value.split(",")]
                                if len(coords) == 2:
                                    self.param[key] = tuple(coords)
                                else:
                                    print(f"Warning: Invalid coordinates for {key}")
                            elif key == "OUTPUT_FILE":
                                self.param[key] = value
                            elif key == "PERFECT":
                                self.param[key] = value.upper() == "TRUE"
                        except ValueError as ve:
                            print(f"Value error parsing line '{line}': {ve}")
                            return {}
                        except Exception as e:
                            print(f"Error parsing line '{line}': {e}")
                            return {}
            
            # Validation check
            required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"]
            missing = [req for req in required if req not in self.param]
            
            if missing:
                print(f"ERROR: Missing required parameters in config file: {', '.join(missing)}")
                return {}

            # Set default for optional parameters
            if "PERFECT" not in self.param:
                self.param["PERFECT"] = False
                    
            return self.param
        except FileNotFoundError:
            print("ERROR: Configuration file not found")
            return {}
        except Exception as e:
            print(f"ERROR: {e}")
            return {}