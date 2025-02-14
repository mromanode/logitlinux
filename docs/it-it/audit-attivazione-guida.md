# Installazione e abilitazione Audit

## Pacchetto Audit

1. Audit dovrebbe essere già installato nel sistema, controlla eseguendo:
```
$ sudo rpm -q audit

audit-3.0...x86_64
``` 
Se il pacchetto è installato, nessuna operazione è richiesta. <a href="#servizio-auditd">Passare all'abilitazione del servizio.</a>
<br>

Se audit non è installato, rpm ritorna il seguente:
```
$ sudo rpm -q audit

package audit is not installed
```

Per risolvere la mancanza del pacchetto, installare Audit:
```
$ sudo dnf -y install audit

Dependencies resolved.
====================================================================
 Package                Arch       Version              Repository       Size
====================================================================
Installing:
 audit                  x86_64     3.0.9-1.fc36         updates          362 k

......
```
<br>

## Servizio auditd

2. Assicurare che il servizio Auditd è in esecuzione e non presentano errori:
```
$ sudo systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```

Se il servizio Audit non è attivo, abilitarlo:
```
$ sudo service auditd start

Redirecting to /bin/systemctl start auditd.sevrice
```

Abilitare il servizio Auditd all'avvio:
```
$ sudo systemctl enable auditd.service

Ritorna nulla se già era abilitato all'avvio...
```

Se il servizio Auditd non era abilitato all'avvio, systemctl ritorna:
```
$ sudo systemctl enable auditd.service

Created symlink /etc/systemd/system/multi-user.target.wants/auditd.service → /usr/lib/systemd/system/auditd.service.
```

Controlla nuovamente se il servizio Auditd è attivo e stia funzionando correttamente:
```
$ sudo systemctl status auditd.service

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago
```

# Referenze

https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening