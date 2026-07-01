# Oracle TEMP Tablespace Exhaustion

## Symptoms
- ORA-01652 unable to extend temp segment.
- Batch jobs or reports fail during sorting.
- Queries using large joins or order by operations become slow.

## Likely Causes
- TEMP tablespace is full.
- A long-running SQL query is consuming temporary space.
- A batch process started a large sort operation.

## Checks
- Check TEMP tablespace usage.
- Identify sessions consuming temporary space.
- Review recently started batch jobs.
- Find SQL statements with large sort operations.

## Fix Steps
- Confirm the offending session or SQL.
- Add a tempfile only after approval.
- Tune the SQL query if the same issue repeats.
- Stop a runaway session only after business validation.

## Severity
High

