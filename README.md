# SmallWorld Backend Engineer Technical Assessment

## Q8 implementation

The management command is implemented at:

`rewards/management/commands/audit_stale_rewards.py`

## Runnable Django assessment harness

The original assessment specifies the `Reward` model fields required for Q8 but does not provide the actual SmallWorld Django project or app label. To make the submitted management command independently reviewable, this repository includes a minimal Django project and `rewards` app containing only the fields specified by the assessment.

This harness is **for assessment demonstration only**. It is not intended to represent SmallWorld's production project structure.

### Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -r requirements.txt
python manage.py migrate
```

### Usage

Dry run (default; no database writes):

```bash
python manage.py audit_stale_rewards
```

Apply the fix:

```bash
python manage.py audit_stale_rewards --fix
```

Run tests:

```bash
python manage.py test
```

The command:

- finds `Reward` rows with `status='claimed'` and `claimed_at` older than seven days;
- prints the total and a breakdown by `reward_type`;
- makes no database changes unless `--fix` is supplied;
- uses Python logging at INFO level for each expired reward ID;
- uses `iterator()` and batched `bulk_update()` so the full result set is not cached in application memory.

## Integration note

The command uses `timezone.now()` for `expires_at` when the remediation is applied. If the application's business definition of `expires_at` is specifically "the scheduled expiry moment", use `claimed_at + timedelta(days=7)` instead.

## Submission

The assessment document contains the written answers and the same Q8 implementation for easy review.
