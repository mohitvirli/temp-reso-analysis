#!/bin/sh
set -e

# Install Cython first so madmom can build correctly.
python3 -m pip install --user "Cython>=0.29.35"

# Install allin1 with no build isolation so madmom sees Cython.
python3 -m pip install --user --no-build-isolation allin1==0.0.3

# Install the remaining requirements.
python3 -m pip install --user -r requirements.txt

echo "Installation complete. Run 'python main.py' to start the API."