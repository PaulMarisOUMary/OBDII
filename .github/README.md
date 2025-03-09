# OBDII

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