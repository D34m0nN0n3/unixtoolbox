## 8 SUDO

!!! abstract ""
    [Конфигурация](#81-конфигурация)

Sudo - это стандартный способ предоставить пользователям некоторые права администратора, не выдавая `root` пароль. Sudo очень полезен в многопользовательской среде с сочетанием серверов и рабочих станций. Просто вызовите команду с sudo:

!!! example ""
    **# sudo /etc/init.d/dhcpd restart** - Запустить сценарий `rc` от `root`  
    **# sudo -l -U sysadmin whoami**     - Получить информацию какие команды от пользователь `sysadmin` можно запускать  
    **# sudo -u sysadmin whoami**        - Запустить команду от пользователь `sysadmin`  
    **# sudo -i**                        - Запустить оболочку, файлы: `.profile`, `.bash_profile` или `.login`, будут прочитаны оболочкой  
    **# sudo -s**                        - Запустить оболочку, указанную в переменной среды `SHELL`  

### 8.1 Конфигурация  

Sudo настраивается в `/etc/sudoers` и должен редактироваться только через `visudo`. Основной синтаксис (списки разделены запятыми):

!!! note "В /etc/sudoers"
    *user hosts = (runas) commands*

!!! info ""
    users - один или несколько пользователей или %group (например %wheel) для получения прав  
    hosts - список хостов (или ALL)  
    runas - список пользователей (или ALL), от имени которых будет запускаться команда. Заключено в `()`!  
    commands - список команд (или ALL), которые будут запускаться как root или как (runas)  

Кроме того, эти ключевые слова могут быть определены как псевдонимы, они называются *User_Alias*, *Host_Alias*, *Runas_Alias* и *Cmnd_Alias*. Это полезно для больших установок. Вот пример `sudoers`:  

!!! note "/etc/sudoers"
    ```ini
    # Псевдонимы хостов - это подсети или имена хостов. 
    Host_Alias DMZ = 212.118.81.40/28  
    Host_Alias DESKTOP = work1, work2
    
    # Псевдонимы пользователей - это список пользователей, которые могут иметь одинаковые права
    User_Alias ADMINS = colin, luca, admin
    User_Alias DEVEL = joe, jack, julia
    Runas_Alias DBA = oracle, pgsql
    
    # Псевдонимы команд определяют полный путь к списку команд  
    Cmnd_Alias SYSTEM = /sbin/reboot,/usr/bin/kill,/sbin/halt,/sbin/shutdown,/etc/init.d/
    Cmnd_Alias PW = /usr/bin/passwd [A-z]*, !/usr/bin/passwd root # Нельзя сменить пароль root!
    Cmnd_Alias DEBUG = /usr/sbin/tcpdump,/usr/bin/wireshark,/usr/bin/nmap  
    
    # Фактические правила
    root,ADMINS ALL = (ALL) NOPASSWD: ALL # Админы могут делать все без пароля.
    DEVEL DESKTOP = (ALL) NOPASSWD: ALL # Разработчики имеют полные права на настольных ПК
    DEVEL DMZ = (ALL) NOPASSWD: DEBUG # Разработчики могут отлаживать серверы DMZ.
    
    # Пользователь sysadmin может управлять серверами DMZ с некоторыми командами.
    sysadmin DMZ = (ALL) NOPASSWD: SYSTEM,PW,DEBUG  
    sysadmin ALL,!DMZ = (ALL) NOPASSWD: ALL # Может делать все вне DMZ.
    %dba ALL = (DBA) ALL # Группа dba может запускать как пользователь БД.
    
    # Каждый может монтировать/размонтировать CD-ROM на настольных ПК  
    ALL DESKTOP = NOPASSWD: /sbin/mount /cdrom, /sbin/umount /cdrom
    ```
