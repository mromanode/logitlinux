# Enable auditing guide

## Audit Package

1. Audit should already be installed on the system, check by running:
```
# rpm -q audit

audit-x.x.x...x86_64
```
If the package is installed, no action is required. <a href="#auditd-service">Proceed to enabling the service.</a>
<br>

If audit is not installed, rpm returns the following:
```
# rpm -q audit

package audit is not installed
```

To resolve the missing package, install Audit:
```
# dnf -y install audit

Dependencies resolved.
====================================================================
 Package                Arch       Version              Repository       Size
====================================================================
Installing:
 audit                  x86_64     3.0.9-1.fc36         updates          362 k

......
```
<br>

## Auditd Service

2. Ensure the Auditd service is running:
```
# systemctl status auditd

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago

   ......
```

If the Audit service is not active, enable it:
```
# service auditd start

Redirecting to /bin/systemctl start auditd.sevrice
```

Enable the Auditd service to start on boot:
```
# systemctl enable auditd.service

Returns nothing if it was already enabled at startup...
```

If the Auditd service was not enabled at startup, systemctl returns:
```
# systemctl enable auditd.service

Created symlink /etc/systemd/system/multi-user.target.wants/auditd.service → /usr/lib/systemd/system/auditd.service.
```

Check again if the Auditd service is active and running correctly and there is not any errors:
```
# systemctl status auditd.service

● auditd.service - Security Auditing Service
   Loaded: loaded (/usr/lib/systemd/system/auditd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-09-06 12:39:22 EDT; 38min ago
```

# References

https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening
