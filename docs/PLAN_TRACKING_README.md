# IEOM Plan Tracking (SQLite)

This project now has a real SQLite tracker for the 24-task IEOM execution plan.

## Files

- `ieom_plan_tracking.sql`: schema + seed data
- `ieom_plan_tracking.db`: initialized database

## Initialize / Reinitialize

```bash
cd /Users/adijain/ENGINEERING/IEOM
sqlite3 ieom_plan_tracking.db < ieom_plan_tracking.sql
```

## Useful Queries

Show overall progress by phase:

```bash
sqlite3 ieom_plan_tracking.db "
SELECT p.code, p.name, t.status, COUNT(*)
FROM todos t
JOIN phases p ON p.id = t.phase_id
GROUP BY p.code, p.name, t.status
ORDER BY p.ordering, t.status;
"
```

Show remaining tasks in dependency order:

```bash
sqlite3 ieom_plan_tracking.db "
SELECT code, status, depends_on_code, owner, title
FROM todos
WHERE status != 'done'
ORDER BY phase_id, priority;
"
```

Mark a task in progress:

```bash
sqlite3 ieom_plan_tracking.db "
UPDATE todos
SET status='in_progress', updated_at=CURRENT_TIMESTAMP
WHERE code='p1-model-validation';
INSERT INTO status_log(todo_code, from_status, to_status, note)
VALUES('p1-model-validation', 'todo', 'in_progress', 'Started validation run');
"
```

Mark a task done:

```bash
sqlite3 ieom_plan_tracking.db "
UPDATE todos
SET status='done', updated_at=CURRENT_TIMESTAMP
WHERE code='p1-model-validation';
INSERT INTO status_log(todo_code, from_status, to_status, note)
VALUES('p1-model-validation', 'in_progress', 'done', 'Validation complete');
"
```
