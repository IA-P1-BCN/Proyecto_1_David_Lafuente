"""
Unit tests for the fare calculation logic (domain layer).

Each test builds a fixed sequence of states and durations — like a
script — and checks that the resulting fare matches what you'd get
calculating it by hand. Because Ride receives `now` as a parameter
instead of reading the system clock, there is no need to wait for
real seconds to pass: we control time explicitly.
"""

import unittest

from taximeter.domain.ride import Ride

MOVING_RATE = 0.05   # EUR/second
STOPPED_RATE = 0.02  # EUR/second


class TestRideFareCalculation(unittest.TestCase):

    def test_ride_starts_stopped_with_zero_fare(self):
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
        self.assertEqual(ride.state, "stopped")
        self.assertAlmostEqual(ride.current_fare(t0), 0.0)

    def test_only_stopped_for_10_seconds(self):
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
        total = ride.finish(t0 + 10)
        # 10s * 0.02 EUR/s = 0.20 EUR
        self.assertAlmostEqual(total, 0.20)

    def test_only_moving_for_10_seconds(self):
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
        ride.change_state("moving", t0)
        total = ride.finish(t0 + 10)
        # 10s * 0.05 EUR/s = 0.50 EUR
        self.assertAlmostEqual(total, 0.50)

    def test_mixed_states_sequence(self):
        # Script: 2s stopped -> 3s moving -> 1s stopped
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)

        ride.change_state("moving", t0 + 2)          # closes 2s stopped
        ride.change_state("stopped", t0 + 2 + 3)      # closes 3s moving
        total = ride.finish(t0 + 2 + 3 + 1)           # closes 1s stopped

        # (2s * 0.02) + (3s * 0.05) + (1s * 0.02) = 0.04 + 0.15 + 0.02
        self.assertAlmostEqual(total, 0.21)

    def test_repeating_same_state_does_not_reset_the_segment(self):
        # Pressing "p" twice in a row should not restart the clock
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)

        changed = ride.change_state("stopped", t0 + 5)  # already stopped
        total = ride.finish(t0 + 10)

        self.assertFalse(changed)
        # The whole 10s counted as stopped, uninterrupted
        self.assertAlmostEqual(total, 0.20)

    def test_finish_is_stable_if_called_again(self):
        # Calling current_fare() right after finish(), with the same
        # `now`, should return the same closed total
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
        ride.change_state("moving", t0 + 4)
        total = ride.finish(t0 + 6)

        self.assertAlmostEqual(ride.current_fare(t0 + 6), total)

    def test_fare_is_frozen_after_finish(self):
        # Even long after finishing, the fare should not keep growing
        t0 = 1000.0
        ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
        ride.change_state("moving", t0 + 4)
        total = ride.finish(t0 + 6)

        self.assertAlmostEqual(ride.current_fare(t0 + 60), total)


if __name__ == "__main__":
    unittest.main()