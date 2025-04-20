import time
import argparse
import sys
import platform
from threading import Event

from pynput import keyboard
from Quartz.CoreGraphics import (
    CGEventCreate, CGEventCreateMouseEvent,
    CGEventGetLocation, CGEventPost,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGHIDEventTap, kCGMouseButtonLeft
)

# Get current mouse position
def get_mouse_position():
    event = CGEventCreate(None)
    return CGEventGetLocation(event)

# Click at the mouse's current position
def mouse_click(x, y):
    event_down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    event_up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event_down)
    CGEventPost(kCGHIDEventTap, event_up)

# Click exactly N times in a given duration
def fast_click(clicks, duration, delay, follow_mouse, abort_event):
    start_time = time.perf_counter()
    end_time = start_time + duration
    click_count = 0
    last_progress = 0

    while click_count < clicks:
        if abort_event.is_set():
            print("\nAborted by user.")
            break
        now = time.perf_counter()
        if now >= end_time:
            break
        if follow_mouse:
            pos = get_mouse_position()
            x, y = int(pos.x), int(pos.y)
        else:
            if click_count == 0:
                pos = get_mouse_position()
                x, y = int(pos.x), int(pos.y)
        mouse_click(x, y)
        click_count += 1

        # Progress feedback every 5%
        progress = int((click_count / clicks) * 100)
        if progress >= last_progress + 5 or click_count == clicks:
            print(f"\rProgress: {progress}% ({click_count}/{clicks})", end="", flush=True)
            last_progress = progress

        if delay > 0:
            time.sleep(delay / 1000.0)

    print(f"\nTotal Clicks: {click_count}")

# Wait for spacebar before starting
def wait_for_space(clicks, duration, delay, follow_mouse, abort_event):
    print(f"Press SPACE to start clicking up to {clicks} times in {duration} seconds...")
    print("Press ESC at any time to abort.")

    def on_press(key):
        if key == keyboard.Key.space:
            print("Starting fast click mode!")
            listener.stop()
        elif key == keyboard.Key.esc:
            print("Aborted before start.")
            abort_event.set()
            listener.stop()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    if not abort_event.is_set():
        fast_click(clicks, duration, delay, follow_mouse, abort_event)

# Print current mouse position
def print_mouse_position():
    pos = get_mouse_position()
    print(f"Current mouse position: x={int(pos.x)}, y={int(pos.y)}")

# Main function for CLI
def main():
    if platform.system() != "Darwin":
        print("Error: This script only works on macOS.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Fast mouse clicker for macOS using Quartz and pynput."
    )
    parser.add_argument(
        "--clicks", "-c", type=int, default=3000,
        help="Maximum number of clicks to perform (default: 3000)"
    )
    parser.add_argument(
        "--duration", "-d", type=float, default=7.0,
        help="Duration in seconds to perform clicks (default: 7.0)"
    )
    parser.add_argument(
        "--delay", "-l", type=int, default=0,
        help="Delay between clicks in milliseconds (default: 0)"
    )
    parser.add_argument(
        "--wait-for-space", "-w", action="store_true",
        help="Wait for spacebar before starting"
    )
    parser.add_argument(
        "--print-pos", "-p", action="store_true",
        help="Print current mouse position and exit"
    )
    parser.add_argument(
        "--follow-mouse", "-f", action="store_true",
        help="Click at the current mouse position each time (follows mouse)"
    )

    args = parser.parse_args()

    if args.print_pos:
        print_mouse_position()
        sys.exit(0)

    abort_event = Event()

    def on_press_abort(key):
        if key == keyboard.Key.esc:
            abort_event.set()
            return False

    # Start abort listener in background
    abort_listener = keyboard.Listener(on_press=on_press_abort)
    abort_listener.start()

    try:
        if args.wait_for_space:
            wait_for_space(args.clicks, args.duration, args.delay, args.follow_mouse, abort_event)
        else:
            print("Press ESC at any time to abort.")
            fast_click(args.clicks, args.duration, args.delay, args.follow_mouse, abort_event)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        abort_listener.stop()

if __name__ == "__main__":
    main()
