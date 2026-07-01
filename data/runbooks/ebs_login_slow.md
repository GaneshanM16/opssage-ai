# Oracle EBS Login Slow

## Symptoms
- Users report slow login.
- Login page loads but authentication takes too long.
- Application tier response time increases.
- Database sessions may increase.

## Likely Causes
- Database connection pool pressure.
- Application tier service degradation.
- Slow SQL during authentication.
- Recent configuration or patching changes.

## Checks
- Check active database sessions.
- Review application tier logs.
- Check CPU and memory on application nodes.
- Review recent deployments or configuration changes.

## Fix Steps
- Validate whether the issue is isolated or system-wide.
- Restart affected application service after approval.
- Tune slow authentication SQL if identified.
- Increase connection pool settings only after capacity review.

## Severity
Medium

