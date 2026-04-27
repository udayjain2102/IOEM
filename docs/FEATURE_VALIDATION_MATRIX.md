# Feature Validation Matrix (MATLAB -> Model)

Use this matrix to complete `p3-validate-features` with evidence.

## Range/Type checks

| Feature | Expected Type | Expected Range | Unit | Pass/Fail | Notes |
|---|---|---|---|---|---|
| `mean_hand_speed` | float | [0.0, 2.0] | m/s | ✓ PASS | Values: 0.0-0.023 m/s |
| `pause_ratio` | float | [0.0, 1.0] | ratio | ✓ PASS | Values: 0.0-0.333 (from CSV) |
| `progress_delta` | float | [0.0, 1.0] | ratio | ✓ PASS | Values: 0.0-0.333 (from CSV) |
| `reversal_count` | int | [0, 10] | count | ✓ PASS | Values: 0 (from CSV, NA_fixture treated as 0) |
| `retry_count` | int | [0, 5] | count | ✓ PASS | Values: 0 (from CSV, NA_fixture treated as 0) |
| `task_step_id` | int | [0, 20] | index | ✓ PASS | Values: 0-1 (from CSV) |
| `human_robot_distance` | float | [0.0, 2.0] | m | ✓ PASS | Values: 1.358-1.482 m (from CSV) |

## Spot-check samples (manual)

Capture at least 10 sampled frames:

| Trial | Frame | mean_hand_speed | pause_ratio | progress_delta | reversal_count | retry_count | task_step_id | human_robot_distance | Reviewer |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| chico_s0 | 0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 1.482 | auto |
| chico_s0 | 1 | 0.0189 | 0.0 | 0.037 | 0 | 0 | 0 | 1.466 | auto |
| chico_s0 | 2 | 0.0185 | 0.0 | 0.074 | 0 | 0 | 0 | 1.450 | auto |
| chico_s0 | 3 | 0.0205 | 0.0 | 0.111 | 0 | 0 | 0 | 1.431 | auto |
| chico_s0 | 4 | 0.0230 | 0.0 | 0.148 | 0 | 0 | 0 | 1.412 | auto |
| chico_s0 | 5 | 0.0205 | 0.0 | 0.185 | 0 | 0 | 0 | 1.395 | auto |
| chico_s0 | 6 | 0.0227 | 0.0 | 0.222 | 0 | 0 | 0 | 1.374 | auto |
| chico_s0 | 7 | 0.0202 | 0.0 | 0.259 | 0 | 0 | 1 | 1.358 | auto |
| chico_s0 | 8 | 0.0 | 0.0 | 0.296 | 0 | 0 | 1 | 1.358 | auto |
| chico_s0 | 9 | 0.0 | 0.0 | 0.333 | 0 | 0 | 1 | 1.358 | auto |

## Consistency checks

- [ ] 7 features are present on every predictor call
- [ ] no NaN/Inf values observed
- [ ] deterministic inputs produce deterministic outputs
- [ ] units are consistent (meters, seconds, frame counts)

## Sign-off

- MATLAB reviewer:
- Model reviewer:
- Date:
- Result:
  - [ ] PASS (ready for `p3-verify-outputs`)
  - [ ] FAIL (needs fixes)
