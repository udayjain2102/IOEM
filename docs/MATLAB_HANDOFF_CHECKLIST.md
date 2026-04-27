# MATLAB Integration Handoff Checklist

## Pre-Integration (For MATLAB Team)

### Setup
- [ ] Clone or copy `/Users/adijain/ENGINEERING/IEOM/ieom_model/`
- [ ] Install Python 3.10+ (3.11 recommended)
- [ ] (Optional) Install PyTorch: `pip install torch`
- [ ] Read `MATLAB_INTEGRATION.md` (full documentation)
- [ ] Read `QUICK_REFERENCE_MATLAB.md` (quick start)

### Verification
- [ ] Run: `python3 -m hesitation.inference.cli health` → ✓ `{"model_loaded": true}`
- [ ] Run test prediction: see QUICK_REFERENCE_MATLAB.md → ✓ get JSON output
- [ ] Verify Python version: `python3 --version` → ✓ 3.10+

## Integration (For MATLAB Team)

### Choose Integration Method
- [ ] Method A: Python function (recommended if MATLAB has py.module support)
- [ ] Method B: CLI via subprocess (recommended for robustness)
- [ ] Method C: REST API (if needed)

### Implement Feature Extraction (Per Frame)
- [ ] Extract `mean_hand_speed` from kinematic history
- [ ] Compute `pause_ratio` as fraction of near-zero frames
- [ ] Calculate `progress_delta` = (current_step - prev_step) / total_steps
- [ ] Count `reversal_count` from direction sign flips
- [ ] Track `retry_count` for current step
- [ ] Get `task_step_id` from state machine
- [ ] Calculate `human_robot_distance` as min hand-TCP distance

### Implement Predictor Call
- [ ] Create features dict with all 7 keys
- [ ] Call predictor (Python function or CLI)
- [ ] Parse output JSON
- [ ] Extract `state` (string)
- [ ] Extract `confidence` (float)
- [ ] Extract `future_hesitation_prob` (float)
- [ ] Extract `future_correction_prob` (float)

### Implement Policy Mapping
- [ ] Map `state` → `speed_factor` using policy table:
  - `normal_progress` → 1.0
  - `mild_hesitation` → 0.8
  - `strong_hesitation` → 0.5
  - `correction_rework` → 0.0
  - `ready_for_robot_action` → 1.0
  - `overlap_risk` → 0.3
- [ ] Apply `speed_factor` to base robot velocity
- [ ] For some states, add delay (see MATLAB_INTEGRATION.md)

### Telemetry Logging (Important!)
- [ ] Log each prediction to file/database
- [ ] Include: timestamp, state, confidence, features
- [ ] Use for debugging and A/B comparison

## Testing (For MATLAB Team)

### Unit Tests
- [ ] Feature extraction produces correct ranges
- [ ] 7 features are provided on every call
- [ ] Predictor returns valid JSON
- [ ] `state` is one of 6 valid values
- [ ] Probabilities sum to ~1.0
- [ ] Confidence ∈ [0, 1]
- [ ] Future risk probs ∈ [0, 1]

### Integration Tests
- [ ] Single prediction <50ms
- [ ] Same input gives same output (determinism)
- [ ] Robot speed changes with state changes
- [ ] Simulator runs 1 full trial without crashes

### A/B Test Setup
- [ ] Baseline policy: no hesitation model (constant speed)
- [ ] Hesitation-aware policy: uses predictions + policy mapping
- [ ] Same random seed for both (reproducible)
- [ ] At least 10 trials per scenario before comparing

## Metrics Collection (For A/B Trials)

### Safety Metrics
- [ ] Count unsafe hand-robot contact events
- [ ] Track min hand-TCP distance per trial
- [ ] Record collision risk score

### Efficiency Metrics
- [ ] Measure task completion time (seconds)
- [ ] Calculate robot idle time (%)
- [ ] Calculate human wait time (%)

### Quality Metrics
- [ ] Count rework/correction cycles
- [ ] Track first-pass success rate
- [ ] Count unnecessary slowdowns

### Results Format
```csv
trial_id,policy,scenario,completion_time,unsafe_events,min_distance,robot_idle_pct,corrections,success_on_first_try
1,baseline,normal_operator,45.2,0,0.42,15.0,0,true
2,hesitation_aware,normal_operator,46.1,0,0.51,18.0,0,true
...
```

## Debugging Guide

### Issue: Model not loading
- [ ] Check file exists: `ls -la src/hesitation/inference/standalone.py`
- [ ] Verify PyTorch installed: `python3 -c "import torch; print(torch.__version__)"`
- [ ] Check Python version: `python3 --version` (must be 3.10+)

### Issue: CLI returns error
- [ ] Verify all 7 feature args provided
- [ ] Check ranges: speed ∈ [0-2.0], pause ∈ [0-1.0], etc.
- [ ] Run sanity check: `python3 -m hesitation.inference.cli health`

### Issue: Feature extraction seems wrong
- [ ] Print feature values per frame
- [ ] Compare against ranges in MATLAB_INTEGRATION.md
- [ ] Verify pause_ratio = (# frames with v<0.1) / 20
- [ ] Verify reversal_count is counting direction sign flips

### Issue: Policy not being applied
- [ ] Print predicted state for each frame
- [ ] Verify state maps to correct speed_factor
- [ ] Check robot velocity actually changes with speed_factor

### Issue: Same prediction every frame
- [ ] Verify features are changing
- [ ] Print feature vector to see if it's updating
- [ ] Check 20-frame window is sliding (not static)

## Sign-Off

When ready to run A/B experiments:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Baseline policy runs 5+ trials without error
- [ ] Hesitation-aware policy runs 5+ trials without error
- [ ] Features are in valid ranges
- [ ] Predictions are deterministic
- [ ] Policy mapping produces expected robot speed changes
- [ ] Metrics are being logged correctly

**Status: ✅ READY TO INTEGRATE**

Once sign-off complete:
1. Run 100-200 trials per scenario per policy
2. Collect all metrics
3. Analyze results (mean, distribution, statistical significance)
4. Report findings to model team

---

**Contact**: Check MATLAB_INTEGRATION.md for troubleshooting or QUICK_REFERENCE_MATLAB.md for quick ref.
