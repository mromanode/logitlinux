# Panoramica di Journalctl

systemd ha il proprio sistema di logging chiamato journal; non è necessario eseguire un daemon di logging separato.

1. Assicurarsi che il servizio systemd journald sia in esecuzione e che non ci siano errori:
```
# systemctl status systemd-journald.service

● systemd-journald.service - Journal Service
     Loaded: loaded (/usr/lib/systemd/system/systemd-journald.service; static)
     Active: active (running) since Wed 2025-01-15 11:03:16 CET; 1min 44s ago

    ......
```

## Spiegazione del comando journalctl

journalctl viene utilizzato per stampare le voci di log memorizzate nel journal da systemd-journald.service(8) e systemd-journal-remote.service(8).

```
# journalctl -u sshd.service
```

- journalctl
    - journalctl viene utilizzato per stampare le voci di log memorizzate nel journal.
    - Opzione preferita per interrogare le voci di log memorizzate nel journal.
<br>

- /usr/sbin/sshd
    - <Inserire spiegazione qui>
<br>


## Output previsto

```
Feb 13 16:40:13 splunkLAB06-sh-es-01 sshd[658356]: Accepted password for labneo from 192.168.200.101 port 51960 ssh2
Feb 13 16:40:13 splunkLAB06-sh-es-01 sshd[658356]: pam_unix(sshd:session): session opened for user labneo(uid=1000) by labneo(uid=0)
Feb 13 18:55:19 splunkLAB06-sh-es-01 sshd[658356]: pam_unix(sshd:session): session closed for user labneo
```

# Riferimenti

https://man.archlinux.org/man/journalctl.1.en
https://wiki.archlinux.org/title/OpenSSH
