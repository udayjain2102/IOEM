# Phase 1 Validation Runbook

This runbook closes:

- `p1-model-validation` (confusion matrix + per-class F1 + macro F1)
- `p1-error-analysis` (sample failure audit)

## Runtime Status

Resolved in this session by installing Python 3.11 (`/opt/homebrew/bin/python3.11`).

Original issue was:

- `TypeError: dataclass() got an unexpected keyword argument 'slots'`

which requires Python 3.10+.

## 1) Create compatible Python env

```bash
cd /Users/adijain/ENGINEERING/IEOM
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

Install project deps (minimal):

```bash
pip install pytest
```

If deep pipeline is needed later:

```bash
pip install torch
```

## 2) Train + evaluate classical baseline on CHICO fixture

```bash
cd /Users/adijain/ENGINEERING/IEOM
mkdir -p ieom_model/reports/phase1_validation
PYTHONPATH=ieom_model/src python ieom_model/scripts/phase2_cli.py train-classical \
  --input ieom_model/merged_database/sample_outputs/chico_model_input_fixture.jsonl \
  --output-dir ieom_model/reports/phase1_validation \
  --window-size 20 \
  --pause-speed-threshold 0.03 \
  --horizon-frames 20

PYTHONPATH=ieom_model/src python ieom_model/scripts/phase2_cli.py evaluate-classical \
  --input ieom_model/merged_database/sample_outputs/chico_model_input_fixture.jsonl \
  --model-path ieom_model/reports/phase1_validation/classical_model.json \
  --output ieom_model/reports/phase1_validation/evaluation_metrics.json
```

Expected artifact:

- `ieom_model/reports/phase1_validation/evaluation_metrics.json`

Contains:

- `current_state_classical.confusion_matrix`
- `current_state_classical.per_class[*].f1`
- `current_state_classical.macro_f1`

## 3) Error analysis sample extraction (25 per state)

Run sequence inference:

```bash
PYTHONPATH=ieom_model/src python ieom_model/scripts/phase2_cli.py infer-sequence \
  --input ieom_model/merged_database/sample_outputs/chico_model_input_fixture.jsonl \
  --model-path ieom_model/reports/phase1_validation/classical_model.json \
  --output ieom_model/reports/phase1_validation/infer_sequence.jsonl
```

Then compare predicted vs latent labels and sample errors per class into:

- `ieom_model/reports/phase1_validation/error_analysis_25_per_class.json`

## 4) Update tracker after successful run

```bash
cd /Users/adijain/ENGINEERING/IEOM
sqlite3 ieom_plan_tracking.db "
UPDATE todos SET status='done', updated_at=CURRENT_TIMESTAMP WHERE code='p1-model-validation';
INSERT INTO status_log(todo_code, from_status, to_status, note)
VALUES('p1-model-validation','blocked','done','Validation artifacts generated');
"
```

For error analysis:

```bash
sqlite3 ieom_plan_tracking.db "
UPDATE todos SET status='in_progress', updated_at=CURRENT_TIMESTAMP WHERE code='p1-error-analysis';
INSERT INTO status_log(todo_code, from_status, to_status, note)
VALUES('p1-error-analysis','todo','in_progress','Starting per-class failure sampling');
"
```
