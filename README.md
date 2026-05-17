# Music Structure Analysis API

A production-ready FastAPI service for analyzing music structure using the Allin1 library.

## Features

- Audio analysis for BPM, segments, beats, and downbeats
- Supports MP3, WAV, FLAC, OGG, and M4A
- CORS enabled
- Built-in health check at `/health`
- Swagger docs at `/docs`

## Installation

The package `madmom` requires `Cython` during its build step. Install `Cython` first, then install the rest of the dependencies:

```bash
./install.sh
```

If you prefer not to use the script, run:

```bash
python3 -m pip install --user "Cython>=0.29.35"
python3 -m pip install --user --no-build-isolation allin1==0.0.3
python3 -m pip install --user -r requirements.txt
```

## Run

```bash
python main.py
```

## Docker

```bash
docker compose up --build
```
