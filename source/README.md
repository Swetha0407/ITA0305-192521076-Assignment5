# Heritage Trails — Assignment 5 Python Prototype

## Scope
Tkinter + SQLite visitor-guide prototype, deterministic offline sync simulation,
and a sequential/worker-pool thumbnail experiment. This is a desktop prototype,
not a native Android/iOS build.

## Setup (WSL Ubuntu)
```bash
sudo apt update
sudo apt install -y python3 python3-tk python3-venv
cd assignment5/source
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
In separate runs:
```bash
python sync_simulation.py
python thumbnail_benchmark.py
```
Outputs are written to `results/`. The UI includes Home, Explore, Detail and
Preferences screens, a network toggle, cached local catalogue, optional simulated
location permission, and empty-search handling.
