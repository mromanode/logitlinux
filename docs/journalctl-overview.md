# Jorunalctl overview

systemd has its own logging system called the journal; running a separate logging daemon is not required.

1. Ensure the systemd journald service is running and there is not any errors:
```
# systemctl status systemd-journald.service

● systemd-journald.service - Journal Service
     Loaded: loaded (/usr/lib/systemd/system/systemd-journald.service; static)
     Active: active (running) since Wed 2025-01-15 11:03:16 CET; 1min 44s ago

    ......
```

## journalctl command explanation

journalctl is used to print the log entries stored in the journal by systemd-journald.service(8) and systemd-journal-remote.service(8).

```
# journalctl /usr/sbin/sshd
```

- journalctl
    - journalctl is used to print the log entries stored in the journal.
    - Preferred option to query log entries stored in the journal.
<br>

- /usr/sbin/sshd
    - <insert explanation here>
<br>

## Expected output

```
Feb 13 16:40:13 splunkLAB06-sh-es-01 sshd[658356]: Accepted password for labneo from 192.168.200.101 port 51960 ssh2
Feb 13 16:40:13 splunkLAB06-sh-es-01 sshd[658356]: pam_unix(sshd:session): session opened for user labneo(uid=1000) by labneo(uid=0)
Feb 13 18:55:19 splunkLAB06-sh-es-01 sshd[658356]: pam_unix(sshd:session): session closed for user labneo
```


# References

https://man.archlinux.org/man/journalctl.1.en
https://wiki.archlinux.org/title/OpenSSH