"""
Entry point for the taximeter CLI (Phase 1).

Preferred way to run it: `python -m taximeter.main` from the src/
folder. The block below makes it also work if this file is run
directly (e.g. the "Run" button in an editor), which otherwise
fails with "ModuleNotFoundError: No module named 'taximeter'"
because Python only looks inside this file's own folder, not in
src/, unless we tell it to.
"""

import os
import sys

if __name__ == "__main__" and __package__ is None:
    # Add src/ (two levels up from this file) to the import path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taximeter.interfaces.cli import main

if __name__ == "__main__":
    main()