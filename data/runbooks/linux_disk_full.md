# Linux Disk Full

## Symptoms
- Application cannot write files.
- Log messages mention no space left on device.
- Disk usage is above 90 percent.
- Services may fail to start.

## Likely Causes
- Large application logs.
- Backup files were not cleaned.
- Temporary files accumulated.
- A batch job generated unexpected output.

## Checks
- Run disk usage checks by mount point.
- Find large files and directories.
- Check application log growth.
- Verify whether cleanup jobs ran successfully.

## Fix Steps
- Compress or rotate logs.
- Remove approved temporary files.
- Move old backups to archive storage.
- Restart affected services only if required.

## Severity
High

