"""
Infrastructure layer: reads external configuration so values like
fare rates don't live hardcoded inside the business logic.
"""

import json
import os

# Resolves to <project_root>/config/tarifas.json regardless of the
# working directory the program is run from.
DEFAULT_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "tarifas.json")
)


def load_rates(config_path=None):
    """Returns (moving_rate, stopped_rate) in EUR/second, read from
    the JSON config file."""
    path = config_path or DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as config_file:
        data = json.load(config_file)
    return data["moving_rate"], data["stopped_rate"]
