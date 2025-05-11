# ClickScript

ClickScript is a Python CLI tool that simulates mouse clicks on macOS. It automates clicking tasks with flexible options for number of clicks, duration, delay, and more.

## Features

- Simulates mouse clicks at the current or live mouse position.
- Configurable number of clicks and duration.
- Optional delay between clicks.
- Option to follow the mouse or click at a fixed position.
- Initiate clicking with the spacebar or immediately.
- Print current mouse position.
- Progress feedback and ESC to abort at any time.
- macOS only.

## Typical Use Case: Walt Food Ordering

**ClickScript was designed to help automate rapid clicking in the Walt food ordering app (https://walt.co.il/) for Israel.**  
This can be useful for quickly securing limited-availability food orders or deals that require fast, repeated clicks on a specific button in the Walt web or desktop app.

**How to use with Walt:**
1. Open the Walt app or website and navigate to the order or deal you want.
2. Move your mouse cursor over the button you want to click (e.g., "Order", "Get Deal", etc.).
3. Run ClickScript with your desired options (see below).
4. Use `--wait-for-space` to prepare and start clicking at the right moment.
5. The script will rapidly click at the mouse position, helping you secure your order faster.

> **Note:** Use this tool responsibly and only where permitted by Walt's terms of service.

## Installation

Make sure you have Python 3 and pip installed.

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python clickOn.py [OPTIONS]
```

### Options

- `-c`, `--clicks N` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Maximum number of clicks to perform (default: 3000)
- `-d`, `--duration SECONDS` &nbsp; Duration in seconds to perform clicks (default: 7.0)
- `-l`, `--delay MS` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Delay between clicks in milliseconds (default: 0)
- `-w`, `--wait-for-space` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Wait for spacebar before starting
- `-p`, `--print-pos` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Print current mouse position and exit
- `-f`, `--follow-mouse` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Click at the current mouse position each time (follows mouse)

### Examples

Click up to 1000 times in 5 seconds, with 10ms delay between clicks:
```bash
python clickOn.py --clicks 1000 --duration 5 --delay 10
```

Wait for spacebar, then click up to 5000 times in 10 seconds, following the mouse:
```bash
python clickOn.py -c 5000 -d 10 -w -f
```

Print current mouse position:
```bash
python clickOn.py --print-pos
```

## Notes

- Press ESC at any time to abort clicking.
- The actual number of clicks may be less than requested if the duration is too short.
- This script only works on macOS.
- For Walt, it's recommended to use `--wait-for-space` so you can start clicking at the exact right moment.

## License

This project is licensed under the MIT License.
