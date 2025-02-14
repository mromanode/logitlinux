# Configurazione regole audit

## auditd dovrebbe essere installato e in esecuzione.

1. Assicurarsi che il servizio Auditd sia in esecuzione e che non ci siano errori:
```
# systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```
<br>

## Applica le regole di audit (RHEL 7 e versioni successive)

Per mantenere le regole persistenti dopo il riavvio o il riavvio del servizio,
aggiungere le seguenti regole al file `/etc/audit/rules.d/audit.rules`:

```
-a exit,always -F arch=b32 -S execve -k auditcmd
-a exit,always -F arch=b64 -S execve -k auditcmd
```

Ricorda di verificare le modifiche (correggendo se necessario)
e rigenerare `/etc/audit/rules.d/audit.rules` come root come segue:

```
$ sudo augenrules --check (opzionale)
$ sudo augenrules --load
```

Se si desidera applicare le regole solo temporaneamente, eseguire i seguenti comandi come root:

```
$ sudo auditctl -a exit,always -F arch=b32 -S execve -k auditcmd
$ sudo auditctl -a exit,always -F arch=b64 -S execve -k auditcmd
```

Per verificare le regole correnti, eseguire:

```
$ sudo auditctl -l
```

N.B: `-k auditcmd` è una parola chiave per cercare l'evento di audit nel registro di audit.

Per verificare i registri di audit per una parola chiave specifica (in questo caso auditcmd), eseguire:

```
$ sudo ausearch -k auditcmd
```
Note: In RHEL 7 e versioni successive, per arrestare/avviare/riavviare il servizio auditd,
eseguire `service auditd stop|start|restart`.

# Riferimenti

https://access.redhat.com/solutions/49257
https://access.redhat.com/solutions/7086214
https://wiki.archlinux.org/title/Audit_framework
