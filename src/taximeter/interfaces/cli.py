"""
Taximeter CLI interface (frontend)
------------------------------------
Everything related to the terminal lives here: instructions, reading
driver commands, and the live fare display. All fare rules live in
the domain layer (taximeter.domain.ride.Ride); this module only
reaches it through the application layer, so it could be swapped for
a GUI or a web frontend in later phases without touching the
calculation logic.
"""

import threading
import time

from taximeter.application.ride_service import start_new_ride

REFRESH_SECONDS = 1


def show_instructions():
    print("=" * 50)
    print("  TAXIMETER - console mode")
    print("=" * 50)
    print("Available commands:")
    print("  s -> START the ride (fare starts counting)")
    print("  m -> vehicle switches to MOVING")
    print("  p -> vehicle switches to STOPPED (waiting)")
    print("  f -> FINISH the ride and show the total fare")
    print("  q -> QUIT the program")
    print("-" * 50)


def live_display(ride, stop_event):
    """Background thread: reprints the current fare on the same
    line every second until the ride is finished."""
    while not stop_event.is_set():
        fare = ride.current_fare(time.time())
        state_label = "MOVING  " if ride.state == "moving" else "STOPPED "
        print(f"\r[{state_label}] Current fare: {fare:.2f} EUR   ", end="", flush=True)
        time.sleep(REFRESH_SECONDS)


def wait_for_start():
    """Blocks until the driver presses 's'. Nothing is counted yet
    at this point — the Ride doesn't even exist."""
    print("\nPress 's' to START the ride (fare is not counting yet).")
    while True:
        command = input(">> ").strip().lower()
        if command == "s":
            return "start"
        elif command == "q":
            return "quit"
        else:
            print("Unknown command. Press 's' to start or 'q' to quit.")


def run_ride():
    ride = start_new_ride()
    stop_event = threading.Event()

    print("\nRide started. The vehicle begins STOPPED.")
    print("Type a command (m / p / f) and press Enter.\n")

    display_thread = threading.Thread(target=live_display, args=(ride, stop_event))
    display_thread.daemon = True
    display_thread.start()

    while True:
        command = input("\n>> ").strip().lower()

        if command == "m":
            if ride.change_state("moving", time.time()):
                print("State: MOVING")
            else:
                print("The vehicle was already moving.")

        elif command == "p":
            if ride.change_state("stopped", time.time()):
                print("State: STOPPED")
            else:
                print("The vehicle was already stopped.")

        elif command == "f":
            total = ride.finish(time.time())
            stop_event.set()
            display_thread.join()
            print(f"\nRide finished. Total fare: {total:.2f} EUR\n")
            return "ride_finished"

        elif command == "q":
            stop_event.set()
            display_thread.join()
            print("\nProgram closed.")
            return "quit"

        else:
            print("Unknown command. Use m, p, f or q.")


def main():
    show_instructions()
    while True:
        choice = wait_for_start()
        if choice == "quit":
            print("\nProgram closed.")
            break

        result = run_ride()
        if result == "quit":
            break
        answer = input("Press Enter to start another ride, or 'q' to quit: ").strip().lower()
        if answer == "q":
            print("\nProgram closed.")
            break


if __name__ == "__main__":
    main()