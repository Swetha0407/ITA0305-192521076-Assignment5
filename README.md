# Heritage Trails — ITA0305 Mobile Computing Assignment 5 (CO5)

This package contains the runnable Python/Tkinter desktop prototype, SQLite-backed local catalogue, deterministic two-device synchronization simulation, thumbnail worker-pool benchmark, test script, UI images, diagrams, and the assignment report.

## 1. Project structure

```text
assignment5/
├── README.md
├── docs/
│   ├── Assignment5_Report.docx
│   └── Assignment5_Report.pdf
├── screenshots/                 # Captured desktop prototype screens
├── assets/                      # Architecture, workflow, benchmark and UI design images
└── source/
    ├── app.py                    # Tkinter + SQLite prototype
    ├── sync_simulation.py        # Two-device version-conflict/idempotency simulation
    ├── thumbnail_benchmark.py    # Sequential vs four-worker image workload
    ├── test_prototype.py         # Automated repository and sync tests
    ├── requirements.txt
    └── results/
        ├── thumbnail_benchmark.csv
        ├── thumbnail_benchmark.json
        └── sync_trace.json
```

## 2. Requirements

- Python 3.10 or later
- Tkinter (usually included with the standard Python installation; on Ubuntu install `python3-tk` if missing)
- Pillow for the thumbnail benchmark

Install the benchmark dependency:

```bash
python3 -m pip install -r requirements.txt
```

## 3. Run the desktop prototype

From this folder:

```bash
cd source
python3 app.py
```

The app demonstrates Home, Explore/search, Monument Details, Preferences, a simulated optional location permission, and online/offline status. Catalogue content is read from a local SQLite database and remains available when the prototype is toggled offline.

## 4. Run the validation scripts

```bash
cd source
python3 test_prototype.py
python3 sync_simulation.py
python3 thumbnail_benchmark.py
```

`test_prototype.py` checks local catalogue seeding/search/empty results and synchronization acknowledgement, stale-version conflict detection, and duplicate-operation handling.

The benchmark compares sequential processing with a four-worker pool for 50, 200 and 1,000 image tasks, using three trials and median duration. The CSV/JSON files included here are the recorded run associated with the report; rerunning the benchmark on another machine or runtime may produce different timings.

## 5. Images included

- `screenshots/` contains actual captures of the running **desktop Tkinter prototype** (Home, Explore, Monument Details, Preferences and Offline state).
- `assets/ui_*.png` contains illustrative mobile-screen mockups used in the report. They are design mockups, not screenshots from a native Android/iOS build.
- Other `assets/*.png` files contain architecture, workflow and benchmark diagrams.

## 6. Evidence boundary and limitations

This is a desktop prototype and selected logic simulation, not a production mobile application. It does not include an APK/IPA, live GPS/geofencing, real map SDK, payment processing, push notification delivery, production cloud backend, or live cross-platform P2P transfer. The location permission is simulated. The sync server is deterministic and in-process. Benchmark values are specific to the recorded host run and must not be interpreted as mobile frame-rate or battery measurements.

The report documents the design decisions, implementation boundary, test evidence and recommended native Android/iOS pilot gates.
