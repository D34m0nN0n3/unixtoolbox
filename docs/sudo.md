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

### 8.2 Ошибки и решение проблем

!!! error "Поврежденный /etc/sudoers - ошибка в синтаксисе"
    Никто не застрахован от ошибок, вместо команды `sudo visudo` я отредактировал файл с помощью стандартного `sudo vim /etc/sudoers` или любым другим редактором или скриптом, и после сохранения всех правок и попытке использовать права  суперпользователя, система выдала ошибку:  
    ```bash
    >>> /etc/sudoers: syntax error near line 23 <<<  
    sudo: parse error in /etc/sudoers near line 23  
    sudo: no valid sudoers sources found, quitting  
    sudo: unable to initialize policy plugin  
    ```

    Есть решения проблемы, использовать:  
    ```bash
    # pkexec visudo -f /etc/sudoers.d/<file_name>  
    ```

    Но получаем в ответ:  
    ```bash
    ==== AUTHENTICATING FOR org.freedesktop.policykit.exec ===  
    Authentication is needed to run '/usr/sbin/visudo' as the super user  
    Authenticating as: user,,, (name) Password:  polkit-agent-helper-1:  
    error response to PolicyKit daemon: GDBus.Error:org.freedesktop.PolicyKit1.Error.Failed: No session for cookie  
    ==== AUTHENTICATION FAILED ===  
    Error executing command as another user: Not authorized  
    This incident has been reported.  
    ```

    Интересная ситуация, чтобы редактировать sudoers мне нужны права суперпользователя, но получить их можно, только "починив" файл sudoers - замкнутый круг. Но есть выход из этой ситуации: откройте два сеанса ssh к серверу (или работа в двух терминалах или две вкладки в терминале).  

    === "В первом сеансе получите PID bash:"
    ```bash
    # echo $$
    ```

    === "Во второй сессии запустите агент аутентификации с помощью:"
    ```bash
    # pkttyagent --process <PID>
    ```
    
    === "Вернувшись в первый сеанс, запустите:"
    ```bash
    # pkexec visudo
    ```

    === "На втором сеансе вы получите приглашение пароля:"
    ```bash
    ==== AUTHENTICATING FOR org.freedesktop.policykit.exec ===  
    Для запуска приложения '/usr/sbin/visudo' от имени суперпользователя требуется аутентификация  
    Authenticating as: user,,, (name)  
    Password:  
    ==== AUTHENTICATION COMPLETE ===  
    ```

    `visudo` запуститься в первой сессии. Проблема решена!

    Если что-то пойдет не так, то выдаст предупреждение:  
    ```bash
    >>> /etc/sudoers: syntax error near line 30 <<<  
    What now?                                             #Что будем делать?  
    Options are:  
      (e)dit sudoers file again                           #снова редактировать  
      e(x)it without saving changes to sudoers file       #выйти без сохранения  
      (Q)uit and save changes to sudoers file (DANGER!)   #сохранить изменения (опасность!)  
    What now? x
    ```
