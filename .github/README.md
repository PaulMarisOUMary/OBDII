# OBDII

A Python ≥3.8 library for interacting with OBDII.

## Installing

Python 3.8 or higher is required.

A [Virtual Environment](https://docs.python.org/3/library/venv.html) is recommended to install the library.

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -3 -m venv .venv
.venv\Scripts\activate
```

To install the development version, run:

```bash
# From Github
pip install git+https://github.com/PaulMarisOUMary/OBDII@main[dev,test]

# From local source
git clone https://github.com/PaulMarisOUMary/OBDII
cd OBDII
pip install .[dev,test]
```

## Usage Example

> [!IMPORTANT]
> This library is still in the design phase and may change in the future.

```python
from obdii import commands
from obdii.connection import Connection

conn = Connection("COM5")

conn.connect()
response = conn.query(commands.VEHICLE_SPEED)
print(f"Vehicle Speed: {response} km/h")

conn.close()
```

## Contributing & Development

The development of this library follows the [ELM327 PDF](/docs/ELM327.PDF) provided by Elm Electronics, with the goal of implementing most features and commands as outlined, starting from page 6 of the document.

This library aims to deliver robust error handling, comprehensive logging, complete type hinting support, and follow best practices to create a reliable tool.

Please, feel free to contribute and share your feedback !

## Support & Contact

For questions or support, open an issue or start a discussion on GitHub.
Your feedback and questions are greatly appreciated and will help improve this project !

- [Open an Issue](https://github.com/PaulMarisOUMary/OBDII/issues)
- [Join the Discussion](https://github.com/PaulMarisOUMary/OBDII/discussions)

---

Thank you for using or contributing to this project.
Follow our updates by leaving a star to this repository !