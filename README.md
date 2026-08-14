# SmallWorld Backend Engineer Technical Assessment

## Q8 implementation

The management command is implemented at:

`rewards/management/commands/audit_stale_rewards.py`

### Assumption

The supplied assessment does not specify the Django app label containing `Reward`, so the example imports:

```python
from rewards.models import Reward
```

If the actual project uses another app label, change that one import.

### Usage

Dry run (default; no database writes):

```bash
python manage.py audit_stale_rewards
```

Apply the fix:

```bash
python manage.py audit_stale_rewards --fix
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
