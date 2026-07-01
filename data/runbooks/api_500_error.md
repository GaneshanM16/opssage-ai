# API HTTP 500 Error

## Symptoms
- API returns HTTP 500.
- Users see failed requests.
- Application logs show unhandled exceptions.
- Error rate increases after a deployment.

## Likely Causes
- Code exception.
- Downstream service failure.
- Invalid configuration.
- Database connection failure.

## Checks
- Check application logs around the timestamp.
- Review recent deployment changes.
- Verify database and downstream service health.
- Check environment variables and secrets.

## Fix Steps
- Roll back if the issue started after deployment.
- Fix the exception and add validation.
- Restore downstream dependency if unavailable.
- Add monitoring for the failed path.

## Severity
High

