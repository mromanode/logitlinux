# Audit rules configuration guide

## Auditd Service

1. Ensure the Auditd service is running and there is not any error:
```
# systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```

## Apply audit rules (RHEL 7 and later)

To keep the rules persistent after reboot or service restart, 
add the following rules to file `/etc/audit/rules.d/audit.rules`:

```
-a exit,always -F arch=b32 -S execve -k auditcmd
-a exit,always -F arch=b64 -S execve -k auditcmd
```

Remember to verify changes (fix as necessary) 
and regenerate `/etc/audit/rules.d/audit.rules` as root as follows:

```
# augenrules --check
# augenrules --load
```

If you only want to apply the rules temporarily, run following commands as root:

```
# auditctl -a exit,always -F arch=b32 -S execve -k auditcmd
# auditctl -a exit,always -F arch=b64 -S execve -k auditcmd
```

To verify the current rules, run:

```
# auditctl -l
```

N.B: `-k auditcmd` is a keyword to search the audit event in the audit log.

To verify audit logs for a specific keyword (in this case auditcmd), run:

```
# ausearch -k auditcmd
```
Notes: In RHEL 7 and later, to stop/start/restart auditd service,
run `service auditd stop|start|restart`.

# References

https://access.redhat.com/solutions/49257
https://access.redhat.com/solutions/7086214
https://wiki.archlinux.org/title/Audit_framework