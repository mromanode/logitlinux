# Ausearch overview

The Linux audit framework provides a CAPP-compliant (Controlled Access Protection Profile) auditing system that reliably collects information about any security-relevant (or non-security-relevant) event on a system.

1. Ensure the Auditd service is running and there is not any errors:
```
# systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```

## Ausearch command explanation

ausearch is a tool that can query the audit daemon logs based for events based on different search criteria.

```
# ausearch --key auditcmd --checkpoint /etc/audit/auditd_checkpoint --start checkpoint --interpret
```

- ausearch
   - a tool to query audit daemon logs
   - Preferred option to query the auditd daemon.
<br>

- --key auditcmd
   - Search for an event based on the given key string.
   - Preferred option to selectively filter based on the keyword.
<br>

- --checkpoint /etc/audit/auditd_checkpoint
   - Checkpoint the output between successive invocations of ausearch such that only - - events not previously output will print in subsequent invocations.
   <br>
   - Should the file or the last checkpointed event not be found, one of a number of errors will result and ausearch will terminate and fail 
   with an exit status of 10, 11 or 12.

      - 10 = invalid checkpoint data found in checkpoint file
      - 11 = checkpoint processing error
      - 12 = checkpoint event not found in matching log file
   - Preferred option to filter out duplicated events.
<br>

- --start
   - Start from the checkpoint.
<br>

- --interpret
   - Interpret numeric entities into text. For example, uid is converted to account name.
   - Preferred option to make the output more human-readable.

## Expected output

```
type=PROCTITLE msg=audit(14/02/25 15:46:55.278:2440872) : proctitle=cat /etc/shadow
type=PATH msg=audit(14/02/25 15:46:55.278:2440872) : item=1 name=/lib64/ld-linux-x86-64.so.2 inode=100671005 dev=fd:00 mode=file,755 ouid=root ogid=root rdev=00:00 obj=system_u:object_r:ld_so_t:s0 nametype=NORMAL cap_fp=none cap_fi=none cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(14/02/25 15:46:55.278:2440872) : item=0 name=/bin/cat inode=67162934 dev=fd:00 mode=file,755 ouid=root ogid=root rdev=00:00 obj=system_u:object_r:bin_t:s0 nametype=NORMAL cap_fp=none cap_fi=none cap_fe=0 cap_fver=0 cap_frootid=0
type=CWD msg=audit(14/02/25 15:46:55.278:2440872) : cwd=/root
type=EXECVE msg=audit(14/02/25 15:46:55.278:2440872) : argc=2 a0=cat a1=/etc/shadow
type=SYSCALL msg=audit(14/02/25 15:46:55.278:2440872) : arch=x86_64 syscall=execve success=yes exit=0 a0=0x55acb331b400 a1=0x55acb33205a0 a2=0x55acb331ea40 a3=0x8 items=2 ppid=659457 pid=1507439 auid=labneo uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=pts0 ses=2967 comm=cat exe=/usr/bin/cat subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 key=auditcmd
```


# References

https://man.archlinux.org/man/ausearch.8.en