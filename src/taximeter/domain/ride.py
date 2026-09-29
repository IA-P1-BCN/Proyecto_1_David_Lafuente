"""
Domain layer: Ride entity and fare calculation rules.
No print/input, no file access, and no clock reading of its own —
it receives "now" as a parameter. That keeps it decoupled from any
interface (CLI today, GUI/API in later phases) and easy to unit
test in Phase 2.
"""


class Ride:
    """A single ride: tracks the vehicle's state and the fare
    accumulated so far (in EUR)."""

    def __init__(self, moving_rate, stopped_rate, now):
        self.moving_rate = moving_rate
        self.stopped_rate = stopped_rate
        self.state = "stopped"          # initial vehicle state
        self.accumulated = 0.0          # fare from already-closed segments
        self.segment_start = now        # start time of the still-open segment
        self.finished = False

    def _rate_for_current_state(self):
        return self.moving_rate if self.state == "moving" else self.stopped_rate

    def current_fare(self, now):
        """Live fare = accumulated total + amount generated in the
        still-open segment. Frozen once the ride has finished."""
        if self.finished:
            return self.accumulated
        elapsed = now - self.segment_start
        return self.accumulated + elapsed * self._rate_for_current_state()

    def change_state(self, new_state, now):
        """Closes the current segment and switches to a new state.
        Returns False (and changes nothing) if the state is already
        `new_state`."""
        if new_state == self.state:
            return False
        self.accumulated = self.current_fare(now)
        self.state = new_state
        self.segment_start = now
        return True

def finish(self, now):
    """Closes the ride and returns the final fare. Freezes the fare
    so later reads don't double-count the last segment."""
    self.accumulated = self.current_fare(now)
    self.finished = True
    return self.accumulated
