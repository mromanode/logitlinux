# Audit rules overview

## Environment

- Red Hat Enterprise Linux 7
- Red Hat Enterprise Linux 8
- Red Hat Enterprise Linux 9
- auditd

## Resolution

The audit package ties in to the Linux kernel audit subsystem. The audit system audits system calls and other kernel level events, 
not user-space events, so we need to audit the `execve()` system call which is what starts executing new programs.

## Audit rules

```
-a exit,always -F arch=b32 -S execve -k auditcmd
-a exit,always -F arch=b64 -S execve -k auditcmd
```
Define a system call to call rules that are loaded into a matching engine that intercepts each syscall that all programs on the system makes.

The `-a` option tells the kernel's rule matching engine that we want to append a rule at the end of the rule list. 
But we need to specify which rule list it goes on and what action to take when it triggers. 

The `exit` filter is the place where all syscall and file system audit requests are evaluated. `always`, always create an event.

Essentially: `-a exit,always` trigger the logging (e.g., always log on exit of a syscall).
<br>

The `-F` option build a rule field: name, operation, value. you would normally have one or more `-F` options that fine tune what events to match against. 
The `arch` field represent the CPU architecture of the syscall.

In this way, you can write rules that are somewhat arch independent because the family type will be auto detected.

Essentially: `-F arch=b32` and `-F arch=b64` monitor system calls on systems that run both 32-bit and 64-bit applications. 
They ensure that the audit system only logs the correct system calls for each architecture.
<br>

The `-S` option can either be the syscall name or number. If the given syscall is made by a program, then start an audit record. 
If a field rule is given and no syscall is specified, it will default to all syscalls.
<br>

The `-K` option set a filter key on an audit rule.

# References

https://access.redhat.com/solutions/49257
https://man.archlinux.org/man/audit.rèules.7.en
https://man.archlinux.org/man/auditctl.8.en
https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening#understanding-audit-log-files_auditing-the-system