"""
Application layer: use cases that coordinate the domain with the
outside world. In Phase 1 there is a single use case — start a ride
with the rates loaded from configuration — but this layer is what
lets future interfaces (GUI in Phase 3, API in Phase 4) reuse the
exact same logic as the CLI without duplicating it.
"""

import time

from taximeter.domain.ride import Ride
from taximeter.infrastructure.config_loader import load_rates


def start_new_ride():
    """Creates a new Ride using the rates from config/tarifas.json."""
    moving_rate, stopped_rate = load_rates()
    return Ride(moving_rate, stopped_rate, now=time.time())
