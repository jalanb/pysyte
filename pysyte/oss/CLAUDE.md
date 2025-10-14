# pysyte.oss

## Package Overview

The `pysyte.oss` package provides Operating System Specific functionality within the pysyte library. It abstracts platform differences to allow the rest of pysyte to work consistently across different operating systems (macOS, Linux, and others).

## Architecture

### Core Module (`platforms.py`)
- **platforms.py:8**: Dynamically imports the appropriate OS-specific module based on `platform.system()`
- Provides unified clipboard operations (`put_clipboard_data`, `get_clipboard_data`)
- Acts as the main entry point for OS-specific functionality

### Platform-Specific Modules

#### Darwin (macOS) - `darwin.py`
- **darwin.py:3-4**: Defines clipboard commands using macOS's `pbpaste` and `pbcopy`
- Minimal implementation focused on clipboard operations

#### Linux - `linux.py`
- **linux.py:6-11**: XDG Base Directory specification support via `xdg_home()`
- **linux.py:14-19**: Configuration file path utilities with `xdg_home_config()`
- **linux.py:31-32**: Clipboard operations using `xclip`
- More comprehensive than Darwin module, handling Linux-specific configuration patterns

### Input/Output Modules

#### Terminal Input - `getch.py`
- **getch.py:31-33**: Single character input without waiting for carriage returns
- **getch.py:36-50**: Terminal context management for proper termios handling
- Cross-platform terminal input abstraction adapted from ActiveState recipes

#### Keyboard Utilities - `keyboard.py`
- **keyboard.py:20-21**: Digit input filtering with `get_digit()`
- **keyboard.py:24-25**: Letter input filtering with `get_letter()`
- **keyboard.py:28-35**: Application quit handling with `quit_on_q()`
- Higher-level keyboard interaction patterns built on `getch`

## Dependencies

- **Standard Library**: `importlib`, `platform`, `subprocess`, `sys`, `termios`, `tty`, `curses`, `signal`, `getpass`, `re`
- **pysyte Internal**: `pysyte.types.paths`, `pysyte.os.EX_CTRL_C`

## Usage Patterns

The package follows a layered approach:
1. **Platform Detection**: Automatic OS detection and module loading
2. **Abstraction Layer**: Unified API for cross-platform operations
3. **Specialized Utilities**: Higher-level keyboard and input handling

## Testing

Comprehensive doctest coverage in `test/` directory with platform-specific conditional testing for clipboard operations and XDG path handling.

## Development Context

Part of the pysyte foundational library's OS abstraction layer, enabling consistent behavior across different development environments while providing access to platform-specific features when needed.