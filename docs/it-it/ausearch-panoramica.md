# Panoramica ausearch

## auditd dovrebbe essere installato ed in esecuzione.

Assicurarsi che il servizio Auditd sia in esecuzione e che non ci siano errori:
```
# systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```

## Analisi del comando Ausearch

```
# ausearch --key auditcmd --checkpoint /etc/audit/auditd_checkpoint --start checkpoint --interpret
```

- ausearch
   - uno strumento per interrogare i log del daemon di audit
   - Preferito per filtrare dettagli non necessari.
<br>

- --key auditcmd
   - Cerca un evento in base alla stringa chiave fornita.
   - Opzione preferita per filtrare selettivamente in base alla parola chiave.
<br>

- --checkpoint /etc/audit/auditd_checkpoint
   - Effettua un checkpoint dell'output tra successive invocazioni di ausearch in modo che solo gli eventi non precedentemente emessi vengano stampati nelle invocazioni successive.
   <br>
   - Se il file o l'ultimo evento con checkpoint non vengono trovati, si verificheranno una serie di errori e ausearch terminerà e fallirà
   con un codice di uscita pari a 10, 11 o 12.

      - 10 = dati checkpoint non validi trovati nel file checkpoint
      - 11 = errore di elaborazione checkpoint
      - 12 = evento checkpoint non trovato nel file di log corrispondente
   - Opzione preferita per filtrare eventi duplicati.
<br>

- --start
   - Parte dal checkpoint.

- --interpret
   - Interpreta le entità numeriche in testo. Ad esempio, uid viene convertito nel nome dell'account.
   - Opzione preferita per rendere l'output più leggibile.

## Output previsto

```
type=PROCTITLE msg=audit(14/02/25 15:46:55.278:2440872) : proctitle=cat /etc/shadow
type=PATH msg=audit(14/02/25 15:46:55.278:2440872) : item=1 name=/lib64/ld-linux-x86-64.so.2 inode=100671005 dev=fd:00 mode=file,755 ouid=root ogid=root rdev=00:00 obj=system_u:object_r:ld_so_t:s0 nametype=NORMAL cap_fp=none cap_fi=none cap_fe=0 cap_fver=0 cap_frootid=0
type=PATH msg=audit(14/02/25 15:46:55.278:2440872) : item=0 name=/bin/cat inode=67162934 dev=fd:00 mode=file,755 ouid=root ogid=root rdev=00:00 obj=system_u:object_r:bin_t:s0 nametype=NORMAL cap_fp=none cap_fi=none cap_fe=0 cap_fver=0 cap_frootid=0
type=CWD msg=audit(14/02/25 15:46:55.278:2440872) : cwd=/root
type=EXECVE msg=audit(14/02/25 15:46:55.278:2440872) : argc=2 a0=cat a1=/etc/shadow
type=SYSCALL msg=audit(14/02/25 15:46:55.278:2440872) : arch=x86_64 syscall=execve success=yes exit=0 a0=0x55acb331b400 a1=0x55acb33205a0 a2=0x55acb331ea40 a3=0x8 items=2 ppid=659457 pid=1507439 auid=labneo uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=pts0 ses=2967 comm=cat exe=/usr/bin/cat subj=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023 key=auditcmd
```


# Riferimenti

https://man.archlinux.org/man/ausearch.8.en
