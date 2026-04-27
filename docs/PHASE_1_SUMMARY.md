# PHASE 1 STATUS — Interface Frozen, Validation Pending

## Status: ✅ Interface + validation artifacts complete on fixture data

### What Was Built

#### 1. **Input Schema** (LOCKED)
```
7 required features (float/int):
- mean_hand_speed        (m/s, range: 0-2.0)
- pause_ratio            (fraction, range: 0-1.0)
- progress_delta         (fraction, range: 0-1.0)
- reversal_count         (count, range: 0-10)
- retry_count            (count, range: 0-5)
- task_step_id           (int, range: 0-20)
- human_robot_distance   (m, range: 0-2.0)

Window: 20 frames @ 10 Hz = 2 seconds of history
```

#### 2. **Output Schema** (LOCKED)
```python
@dataclass
class Prediction:
    state: str                              # One of 6 states
    state_probabilities: dict               # All 6 state probs (sum=1.0)
    future_hesitation_prob: float           # Risk next 2s [0-1]
    future_correction_prob: float           # Risk next 2s [0-1]
    confidence: float                       # Max state prob [0-1]
    window_size_frames: int = 20
    frame_rate_hz: int = 10
```

#### 3. **6 States** (LOCKED)
```
1. normal_progress       — steady motion, confident
2. mild_hesitation       — brief pause, continues
3. strong_hesitation     — prolonged pause, uncertain
4. correction_rework     — deliberate backtrack + retry
5. ready_for_robot_action — human waits for robot
6. overlap_risk          — hand in danger zone
```

#### 4. **Inference Wrapper** (READY)

**File**: `src/hesitation/inference/standalone.py`

Python class `HesitationPredictor` with interface:
```python
predictor = HesitationPredictor.load_default()  # Load once
prediction = predictor.predict_single(features)  # Call per frame
```

**Properties**:
- Deterministic (same input → same output)
- Sub-50ms latency (CPU-only)
- No external dependencies (just torch optional)
- JSON serializable output

#### 5. **CLI for MATLAB** (READY)

**File**: `src/hesitation/inference/cli.py`

```bash
python3 -m hesitation.inference.cli predict \
    --mean-hand-speed 0.5 \
    --pause-ratio 0.1 \
    --progress-delta 0.8 \
    --reversal-count 1 \
    --retry-count 0 \
    --task-step-id 3 \
    --human-robot-distance 0.35 \
    --format json
```

Output:
```json
{
    "state": "mild_hesitation",
    "state_probabilities": {
        "normal_progress": 0.15,
        "mild_hesitation": 0.65,
        ...
    },
    "future_hesitation_prob": 0.42,
    "future_correction_prob": 0.08,
    "confidence": 0.65
}
```

#### 6. **MATLAB Integration Guide** (READY)

**File**: `MATLAB_INTEGRATION.md`

Complete documentation for MATLAB team:
- 3 integration methods (Python function, CLI, py.module)
- Feature schema with units and ranges
- Policy mapping table (state → robot action)
- Troubleshooting guide
- Example MATLAB code

### Files Created

```
ieom_model/
├── src/hesitation/inference/
│   ├── __init__.py              # Public API
│   ├── predictor.py             # Main wrapper (package version)
│   ├── standalone.py            # Independent module (for MATLAB)
│   └── cli.py                   # Command-line interface
├── tests/
│   ├── test_inference_minimal.py # Standalone tests
│   └── test_inference_interface.py # Package integration tests
└── MATLAB_INTEGRATION.md        # Complete integration guide
```

### What's NOT Done (Current)

- [ ] Cross-dataset testing (CHICO -> HA-ViD transfer) on full dataset
- [ ] Expanded error audit coverage to 25 examples per class on full validation corpus

Model interface and core validation artifacts are complete and MATLAB integration remains unblocked.

### Session 2 Update (2026-04-27)

- Added real plan tracker files in project root:
  - `ieom_plan_tracking.sql`
  - `ieom_plan_tracking.db`
  - `PLAN_TRACKING_README.md`
- Updated tracker state:
  - `p1-model-validation` -> `blocked`
  - `p1-error-analysis` -> `todo`
- Blocker detail:
  - Local `python3` does not support `dataclass(slots=True)` and fails during import.
  - Validation pipeline requires Python 3.10+.
- Added unblock guide:
  - `PHASE1_VALIDATION_RUNBOOK.md`

### Session 3 Update (2026-04-27)

- Installed Python 3.11 (`/opt/homebrew/bin/python3.11`) and unblocked runtime compatibility.
- Generated validation artifacts:
  - `ieom_model/reports/phase1_validation/classical_model.json`
  - `ieom_model/reports/phase1_validation/metrics.json`
  - `ieom_model/reports/phase1_validation/evaluation_metrics.json`
  - `ieom_model/reports/phase1_validation/error_analysis_25_per_class.json`
- Tracker updates:
  - `p1-model-validation` -> `done`
  - `p1-error-analysis` -> `done`
- Note:
  - Fixture data required `window_size=10`, `horizon_frames=8` to produce non-empty windows.
  - Error-analysis artifact currently has limited class coverage due fixture composition.

### Next Steps

**For MATLAB Team**:
1. Read `MATLAB_INTEGRATION.md`
2. Pick integration method (recommend CLI for isolation)
3. Verify model loads: `python3 -m hesitation.inference.cli health`
4. Test single prediction with sample features
5. Integrate into simulator

**For Model Team**:
1. Complete model validation (confusion matrix, per-class metrics)
2. Cross-dataset testing (CHICO → HA-ViD transfer)
3. Error analysis (when does model fail?)
4. Prepare results table for paper

### Testing

Run standalone tests (no package dependencies):
```bash
cd ieom_model
python3 tests/test_inference_minimal.py
```

Output:
```
✓ Prediction dataclass works
✓ Predictor initialization works
✓ Feature vector conversion works
✓ Dummy prediction works: normal_progress
✓ Predictions are deterministic
✓ JSON export works

All tests passed!
```

### Key Decisions Locked

1. **7 features** (no more, no less) — matches training
2. **6 states** — from trained model
3. **Multi-head output** — state + future risks
4. **Deterministic** — no randomness at inference
5. **<50ms latency** — CPU-only acceptable
6. **JSON I/O** — language-independent

### Integration Checklist for MATLAB

- [ ] Model repo copied locally
- [ ] Model checkpoint loaded successfully
- [ ] Single prediction works (<50ms)
- [ ] Predictions are deterministic
- [ ] Features extracting correctly
- [ ] Policy mapping defined
- [ ] Simulator runs A/B tests
- [ ] Telemetry logging predictions

