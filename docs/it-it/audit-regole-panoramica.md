# Panoramica regole audit

## Ambiente

- Red Hat Enterprise Linux 7
- Red Hat Enterprise Linux 8
- Red Hat Enterprise Linux 9
- auditd

## Risoluzione

Il pacchetto di audit si collega al sottosistema di audit del kernel Linux. Il sistema di audit controlla le chiamate di sistema e altri eventi a livello di kernel, 
non eventi dello spazio utente, quindi dobbiamo controllare la chiamata di sistema `execve()` che è ciò che avvia l'esecuzione di nuovi programmi.

## Regole di audit

```
-a exit,always -F arch=b32 -S execve -k auditcmd
-a exit,always -F arch=b64 -S execve -k auditcmd
```
Definisci una chiamata di sistema per chiamare le regole che vengono caricate in un motore di corrispondenza che intercetta ogni syscall che tutti i programmi sul sistema fanno.

L'opzione `-a` indica al motore di corrispondenza delle regole del kernel che vogliamo aggiungere una regola alla fine dell'elenco delle regole. 
Ma dobbiamo specificare su quale elenco di regole va e quale azione intraprendere quando viene attivata. 

Il filtro `exit` è il punto in cui vengono valutate tutte le richieste di audit di syscall e filesystem. `always`, crea sempre un evento.

In sostanza: `-a exit,always` attiva la registrazione (ad esempio, registra sempre all'uscita di una syscall).
<br>

L'opzione `-F` crea un campo di regola: nome, operazione, valore. Normalmente avresti una o più opzioni `-F` che mettono a punto gli eventi da confrontare. 
Il campo `arch` rappresenta l'architettura della CPU della syscall.

In questo modo, puoi scrivere regole che sono in qualche modo indipendenti dall'architettura perché il tipo di famiglia verrà rilevato automaticamente.

In sostanza: `-F arch=b32` e `-F arch=b64` monitorano le chiamate di sistema su sistemi che eseguono applicazioni sia a 32 bit che a 64 bit. 
Garantiscono che il sistema di audit registri solo le chiamate di sistema corrette per ogni architettura.
<br>

L'opzione `-S` può essere il nome o il numero della syscall. Se la syscall data viene eseguita da un programma, avvia una registrazione di audit. 
Se viene fornita una regola di campo e non viene specificata alcuna syscall, per impostazione predefinita verranno utilizzate tutte le syscall.
<br>

L'opzione `-K` imposta una chiave di filtro su una regola di audit.

# Riferimenti

https://access.redhat.com/solutions/49257
https://man.archlinux.org/man/audit.rules.7.en
https://man.archlinux.org/man/auditctl.8.en
https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/auditing-the-system_security-hardening#understanding-audit-log-files_auditing-the-system
