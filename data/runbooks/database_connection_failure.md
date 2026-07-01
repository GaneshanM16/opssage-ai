# Database Connection Failure

## Symptoms
- Application cannot connect to database.
- Error mentions connection timeout.
- Login or API requests fail.

## Likely Causes
- Database listener is down.
- Wrong database credentials.
- Network issue between app and database.
- Connection pool is exhausted.

## Checks
- Check database listener status.
- Verify database host and port.
- Check application connection pool.
- Review database alert logs.

## Fix Steps
- Restart listener after approval.
- Correct connection string if misconfigured.
- Scale or reset connection pool if exhausted.
- Escalate to DBA team if database is unavailable.

## Severity
High