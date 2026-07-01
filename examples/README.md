# OpsSage AI Examples

These examples show what the project does without needing a UI.

## Example 1: Database Connection Failure

Request:

```json
{
  "incident": "Application cannot connect to database and connection timeout error is showing"
}
```

What it proves:

- custom runbook retrieval works
- response is grounded on a matching knowledge source
- root cause is presented as possible, not confirmed

See:

```txt
database_connection_request.json
database_connection_response.json
```

## Example 2: Oracle TEMP Tablespace

Request:

```json
{
  "incident": "ORA-01652 unable to extend temp segment in tablespace TEMP"
}
```

What it proves:

- Oracle error retrieval works
- system can connect incident text to database runbooks
- output includes checks and fix steps

See:

```txt
oracle_temp_request.json
oracle_temp_response.json
```

