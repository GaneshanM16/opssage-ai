# Incident 001 - TEMP Tablespace Failure

## Incident
Nightly report failed with ORA-01652 during a large sorting operation.

## Resolution
The team identified a long-running SQL query consuming TEMP space. A tempfile
was added after approval, and the SQL was later tuned to reduce sort usage.

## Category
Oracle database storage

## Severity
High

