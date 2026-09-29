def test_fare_is_frozen_after_finish(self):
    t0 = 1000.0
    ride = Ride(MOVING_RATE, STOPPED_RATE, now=t0)
    ride.change_state("moving", t0 + 4)
    total = ride.finish(t0 + 6)
    self.assertAlmostEqual(ride.current_fare(t0 + 60), total)