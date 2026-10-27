# InputMapper

A configurable numpad input mapper written in Python.

InputMapper uses `pynput` to capture numpad input and convert encoded sequences into characters, modifier keys, function keys, and media keys.

## Requirements

- Python 3.11 or later
- `pynput`

## Usage

1. Install the dependency:

   ```bash
   pip install pynput
   ```

2. Configure the mappings in `numpad_config.toml`.
3. Run the program:

   ```bash
   python numpad.py
   ```

4. Enter a sequence using the numpad and press `+` to confirm.

## Configuration

Mappings are defined in `numpad_config.toml`.

- `General`: General settings, including debug output.
- `CharMapping`: Maps pairs of digits to characters.
- `FunctionMapping`: Maps encoded sequences to function or media keys.
- `ModifierMapping`: Maps single digits to modifier or special keys.

## Notes

- The program is designed for numpad input.
- Debug output can be enabled or disabled in the configuration file.
