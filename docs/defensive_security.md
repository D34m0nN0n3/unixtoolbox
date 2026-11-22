## 25 Defensive (оборонительная) безопасность

!!! abstract "" 
    [Аудит безопасности](#251-аудит-безопасности-lynis) | [Поиск руткитов](#252-поиск-руткитов-rkhunter-и-chkrootkit) | [Ручной поиск признаков компрометации](#255-ручной-поиск-признаков-компрометации-ioc) | [Анализ журналов аудита и поиск точки входа](#256-анализ-журналов-аудита-и-поиск-точки-входа) | [Incident Response Toolkit](#257-запуск-без-установки-incident-response-toolkit) | [Сбор артефактов для DFIR](#258-сбор-артефактов-для-dfir) | [Удаление компрометации и точек закрепления](#259-удаление-компрометации-и-точек-закрепления-persistence)

Раздел содержит команды и утилиты для аудита безопасности системы, поиска руткитов, анализа журналов, сбора артефактов для DFIR (Digital Forensics and Incident Response) и устранения признаков несанкционированного доступа (IoC).

!!! warning "Важно"
    При подозрении на компрометацию не доверяйте системным бинарным файлам (`ps`, `netstat`, `ls`, `find`, `ss`), так как они могут быть подменены злоумышленником. Используйте статически скомпилированные утилиты (например, BusyBox) с доверенного носителя или запускайте их из изолированной директории.

### 25.1 Аудит безопасности (Lynis)

**Lynis** — инструмент для аудита безопасности Linux/Unix систем, проверки конфигураций и поиска уязвимостей.

!!! example ""
    **# apt install lynis**                                              - Установка (Debian / Ubuntu / Astra Linux)  
    **# dnf install lynis**                                              - Установка (RHEL / Fedora / РЕД ОС)  
    **# lynis audit system**                                             - Полный аудит системы (рекомендуется запускать от root)  
    **# lynis audit system --quick**                                     - Быстрый аудит без пауз (удобно для скриптов и cron)  
    **# lynis audit system --warnings-only**                             - Аудит с выводом только предупреждений и рекомендаций  
    **# lynis audit system --tests-from-group networking,kernel,ssh**    - Проверка конкретного компонента (например, сети, ядра или SSH)  
    **# lynis show details KRNL-6000**                                   - Просмотр подробностей по конкретному тесту (по его ID из отчета)  

Логи и отчеты по умолчанию сохраняются в `/var/log/lynis.log` и `/var/log/lynis-report.dat`.

### 25.2 Поиск руткитов (rkhunter и chkrootkit)

Утилиты сканируют систему на наличие известных руткитов, бэкдоров, снифферов и модификаций системных файлов.

#### 25.2.1 Rootkit Hunter (rkhunter)

!!! example ""
    **# apt install rkhunter**                                           - Установка (Debian / Astra Linux)  
    **# dnf install rkhunter**                                           - Установка (RHEL / РЕД ОС)  
    **# rkhunter --update**                                              - Обновление баз сигнатур  
    **# rkhunter --propupd**                                             - Создание снимка эталонных хешей системных файлов (делать на чистой системе)  
    **# rkhunter --check**                                               - Запуск полной проверки системы  
    **# rkhunter --check --sk --rwo**                                    - Проверка без интерактивного подтверждения и вывод только предупреждений  

Лог проверки записывается в `/var/log/rkhunter.log`.

#### 25.2.2 chkrootkit

!!! example ""
    **# apt install chkrootkit**                                         - Установка (Debian / Astra Linux)  
    **# dnf install chkrootkit**                                         - Установка (RHEL / РЕД ОС)  
    **# chkrootkit**                                                     - Запуск полной проверки  
    **# chkrootkit -q**                                                  - Тихий режим (вывод только подозрительных находок)  
    **# chkrootkit -r /mnt/compromised_root**                            - Проверка смонтированной скомпрометированной системы (например, с LiveCD)  

### 25.3 Контроль целостности файлов (AIDE)

**AIDE** (Advanced Intrusion Detection Environment) создает базу хешей файлов и отслеживает их несанкционированное изменение.

!!! example ""
    **# apt install aide**                                                    - Установка (Debian / Astra Linux)  
    **# dnf install aide**                                                    - Установка (RHEL / РЕД ОС)  
    **# aide --init**                                                         - Инициализация базы данных (создает `/var/lib/aide/aide.db.new`)  
    **# mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db**                  - Активация созданной базы в качестве эталонной  
    **# aide --check**                                                        - Проверка целостности файлов по текущей базе  
    **# aide --update && mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db** - Обновление базы после легитимных изменений в системе  

### 25.4 Антивирусное сканирование (ClamAV)

!!! example ""
    **# apt install clamav clamav-daemon**                               - Установка (Debian / Astra Linux)  
    **# dnf install clamav clamav-update**                               - Установка (RHEL / РЕД ОС)  
    **# freshclam**                                                      - Обновление антивирусных баз  
    **# clamscan -r -i /var/www /tmp /home**                             - Рекурсивная проверка директорий с выводом только зараженных файлов  

### 25.5 Ручной поиск признаков компрометации (IoC)

Базовые команды для первичного осмотра (Incident Response) без установки стороннего ПО.

#### 25.5.1 Учетные записи и сессии

!!! example ""
    **# awk -F: '(\$3 == "0") {print}' /etc/passwd**                     - Проверка пользователей с UID 0 (права root)  
    **# awk -F: '(\$2 == "") {print}' /etc/shadow**                      - Поиск пользователей с пустыми паролями  
    **# last -a | head -n 30**                                           - Просмотр последних входов в систему и перезагрузок  
    **# lastb -a | head -n 30**                                          - Неудачные попытки входа  
    **# w**                                                              - Проверка активных сессий и запущенных ими процессов  

#### 25.5.2 Процессы и планировщик

!!! example ""
    **# ps auxwf**                                                        - Дерево всех процессов (поиск скрытых или нестандартных дочерних процессов)  
    **# ls -alR /proc/*/exe 2>/dev/null | grep deleted**                  - Процессы, запущенные из удаленных бинарных файлов (признак малвари в памяти)  
    **# tr '\0' '\n' < /proc/<PID>/environ**                              - Проверка переменных окружения подозрительного процесса (подмена `LD_PRELOAD`)  
    **# for u in $(cut -f1 -d: /etc/passwd); do crontab -u \$u -l; done** - Проверка задач cron для всех пользователей  
    **# ls -la /etc/cron* /var/spool/cron/crontabs/**                     - Системные задания cron  
    **# systemctl list-timers --all**                                     - Проверка всех таймеров systemd  

#### 25.5.3 Сеть и открытые порты

!!! example ""
    **# ss -tulnp**                                                      - Активные сетевые соединения и слушающие порты с привязкой к процессам  
    **# ss -tupn state established**                                     - Поиск процессов с установленными внешними соединениями  
    **# lsof -i -P -n**                                                  - Просмотр списка открытых сетевых файлов (альтернатива `ss`)  

#### 25.5.4 Файловая система и модули ядра

!!! example ""
    **# find / -perm /6000 -type f 2>/dev/null**                         - Поиск файлов с SUID/SGID битами (потенциальное повышение привилегий)  
    **# find / \( -nouser -o -nogroup \) 2>/dev/null**                   - Поиск файлов без владельца или группы  
    **# find / -xdev -mtime -1 -type f 2>/dev/null**                     - Файлы, измененные за последние 24 часа (исключая виртуальные ФС)  
    **# find /tmp /var/tmp /dev/shm -type f -executable 2>/dev/null**    - Исполняемые файлы в директориях временного хранения  
    **# lsmod**                                                          - Проверка загруженных модулей ядра  
    **# debsums -s**                                                     - Проверка целостности пакетов в Debian / Ubuntu / Astra Linux  
    **# rpm -Va**                                                        - Проверка целостности пакетов в RHEL / Fedora / РЕД ОС  

### 25.6 Анализ журналов аудита и поиск точки входа

Поиск первичного вектора проникновения: брутфорс SSH, повышение привилегий (`sudo`/`su`), эксплуатация веб-сервисов или попытки очистки следов.

#### 25.6.1 Журналы аутентификации (`auth.log` / `secure`)

В системах на базе Debian/Astra Linux события пишутся в `/var/log/auth.log`, в RHEL/РЕД ОС — в `/var/log/secure`.

!!! example ""
    **# grep "Accepted " /var/log/auth.log /var/log/secure 2>/dev/null** - Успешные входы по SSH (поиск нестандартных IP или входов по ключам)  
    **# grep "Failed password" /var/log/auth.log | awk '{print \$(NF-3)}' | sort | uniq -c | sort -nr | head -n 20** - Топ IP-адресов с неудачными попытками входа  
    **# grep -E "useradd|usermod|groupadd|new user" /var/log/auth.log /var/log/secure 2>/dev/null** - Поиск фактов создания новых пользователей или добавления в группы (`sudo`/`wheel`)  
    **# grep "COMMAND=" /var/log/auth.log /var/log/secure 2>/dev/null**  - История использования `sudo` (какие команды запускались от root)  

#### 25.6.2 Системный журнал (`journalctl`)

!!! example ""
    **# journalctl -u ssh -u sshd --since "2026-01-01 00:00:00" --until "2026-01-02 23:59:59"** - Проверка логов службы SSH за конкретный период времени  
    **# journalctl _COMM=sshd _COMM=sudo _COMM=su -n 100 --no-pager**    - Поиск всех событий аутентификации и `sudo` в systemd-journal  
    **# journalctl -k | grep -iE "segfault|traps|overflow"**             - Поиск ошибок сегментации (признак попыток эксплуатации RCE/BoF)  
    **# journalctl --verify**                                            - Проверка целостности бинарных файлов журнала systemd  

#### 25.6.3 Веб-серверы и история команд (поиск RCE и веб-шеллов)

!!! example ""
    **# grep -E "POST .*\.(php|jsp|asp|py|sh)" /var/log/nginx/access.log /var/log/httpd/access_log 2>/dev/null** - Поиск подозрительных POST-запросов и обращений к скриптам  
    **# grep -iE "union.*select|eval\(|base64_decode|/etc/passwd|cmd=|wget%20|curl%20" /var/log/nginx/access.log 2>/dev/null** - Поиск признаков инъекций и сканеров в HTTP-запросах  
    **# ls -la /root/.*history /home/*/.*history 2>/dev/null**           - Проверка файлов истории команд пользователей (поиск обнуления/подмены на `/dev/null`)  

### 25.7 Запуск без установки (Incident Response Toolkit)

Для защиты от подмены системных утилит руткитами (`LD_PRELOAD` или троянизированные бинарники) на чистой машине той же архитектуры (`x86_64` / `aarch64`) собирается портативный набор со статически скомпилированным **BusyBox** и сканерами.

#### 25.7.1 Сборка доверенного окружения (на чистой машине)

!!! example ""
    **# mkdir -p ~/ir-toolkit/bin**                                      - Создание структуры каталогов для переносного набора  
    **# wget -O ~/ir-toolkit/bin/busybox https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox** - Загрузка статически скомпилированного BusyBox  
    **# chmod +x ~/ir-toolkit/bin/busybox**                              - Выдача прав на исполнение  
    **# for cmd in \$(~/ir-toolkit/bin/busybox --list); do ln -s busybox ~/ir-toolkit/bin/\$cmd; done** - Создание символических ссылок на базовые утилиты внутри каталога  
    **# git clone https://github.com/Magentron/chkrootkit.git ~/ir-toolkit/chkrootkit** - Клонирование исходного кода chkrootkit  
    **# cd ~/ir-toolkit/chkrootkit && make STATIC=1**                    - Статическая сборка C-утилит из состава chkrootkit  
    **# find . -maxdepth 1 -type f -executable ! -name "chkrootkit" -exec cp {} ~/ir-toolkit/bin/ \;** - Копирование собранных бинарников в общую папку `bin`  
    **# git clone --depth 1 https://github.com/CISOfy/lynis ~/ir-toolkit/lynis** - Загрузка портативного Lynis (не требует компиляции)  
    **# cd ~ && tar -czf ir-toolkit.tar.gz ir-toolkit/**                  - Упаковка набора в архив для передачи на целевой хост  

#### 25.7.2 Применение на исследуемом хосте

!!! example ""
    **# scp ir-toolkit.tar.gz user@target-host:/tmp/**                   - Копирование архива на целевой сервер  
    **# cd /tmp && tar -xzf ir-toolkit.tar.gz**                          - Распаковка архива на целевом сервере  
    **# export PATH=/tmp/ir-toolkit/bin:\$PATH && unset LD_PRELOAD**      - Переопределение `PATH` и сброс `LD_PRELOAD` для изоляции от системных бинарников  
    **# /tmp/ir-toolkit/bin/busybox sh**                                 - Запуск изолированной оболочки BusyBox (игнорирует системный `/bin/bash`)  
    **# ps aux && netstat -tulnp**                                       - Проверка процессов и сети внутри доверенной оболочки  
    **# /tmp/ir-toolkit/chkrootkit/chkrootkit -p /tmp/ir-toolkit/bin -q** - Запуск chkrootkit с явным указанием пути к доверенным бинарникам (`-p`)  
    **# cd /tmp/ir-toolkit/lynis && ./lynis audit system --pentest --quick** - Запуск Lynis без установки (флаг `--pentest` отключает проверку прав владельца)  

### 25.8 Сбор артефактов для DFIR

При обнаружении вредоносных файлов перед их удалением необходимо зафиксировать метаданные, снять хеши, обезвредить файлы добавлением префикса и упаковать в зашифрованный архив для передачи.

!!! warning "Порядок действий"
    1. Сначала снимите хеши и скопируйте файлы в карантин (до изменения их содержимого).
    2. Остановите вредоносный процесс, и только затем удаляйте исходные файлы, иначе процесс может воссоздать их на диске.

#### 25.8.1 Сбор метаданных, хеширование и карантин

!!! example ""
    **# INCIDENT_DIR="/tmp/dfir_artifacts_\$(date +%Y%m%d_%H%M%S)" && mkdir -p "\$INCIDENT_DIR/files"** - Создание изолированной директории для сбора артефактов  
    **# SUSPECT_FILE="/tmp/.hidden_miner"**                              - Задание пути к обнаруженному подозрительному файлу  
    **# stat "\$SUSPECT_FILE" >> "\$INCIDENT_DIR/metadata.txt"**           - Фиксация метаданных файла (права, владелец, временные метки MACB)  
    **# sha256sum "\$SUSPECT_FILE" >> "\$INCIDENT_DIR/hashes_sha256.txt"** - Подсчет контрольной суммы SHA-256  
    **# md5sum "\$SUSPECT_FILE" >> "\$INCIDENT_DIR/hashes_md5.txt"**       - Подсчет контрольной суммы MD5  
    **# cp -p "\$SUSPECT_FILE" "\$INCIDENT_DIR/files/INFECTED_\$(basename "\$SUSPECT_FILE").quarantine"** - Копирование файла в карантин с сохранением атрибутов и префиксом `INFECTED_`  
    **# chmod -R a-x "\$INCIDENT_DIR/files/"**                            - Снятие прав на исполнение со всех файлов в карантине  

Пакетный сбор нескольких файлов из подозрительной директории:

```bash
find /dev/shm -type f | while read -r file; do
    sha256sum "$file" >> "$INCIDENT_DIR/hashes_sha256.txt"
    cp -p "$file" "$INCIDENT_DIR/files/INFECTED_$(basename "$file").quarantine"
done
```

#### 25.8.2 Упаковка и шифрование архива для передачи в DFIR

!!! example ""
    **# tar -czf - -C /tmp "\$(basename "\$INCIDENT_DIR")" | openssl enc -aes-256-cbc -salt -pbkdf2 -out "/tmp/dfir_package_\$(hostname).tar.gz.enc"** - Упаковка в `tar.gz` и шифрование AES-256  
    **# zip -r -P infected "/tmp/dfir_package_\$(hostname).zip" "\$INCIDENT_DIR"** - Альтернатива: создание ZIP-архива с паролем (`infected`)  
    **# sha256sum "/tmp/dfir_package_\$(hostname).zip"**                  - Подсчет итогового хеша архива для контроля целостности при передаче  

### 25.9 Удаление компрометации и точек закрепления (Persistence)

!!! example ""
    **# fuser -k -9 "\$SUSPECT_FILE"**                                     - Принудительное завершение процессов, использующих вредоносный файл  
    **# kill -9 <PID>**                                                    - Завершение вредоносного процесса по его PID  
    **# lsattr "\$SUSPECT_FILE" && chattr -ia "\$SUSPECT_FILE"**           - Проверка и снятие атрибутов защиты от удаления/изменения (`immutable`)  
    **# rm -f "\$SUSPECT_FILE"**                                           - Удаление вредоносного файла с диска  
    **# rm -rf "\$INCIDENT_DIR" "/tmp/dfir_package_$(hostname)."* "/tmp/ir-toolkit"* /tmp/ir-toolkit.tar.gz** - Очистка временных каталогов после передачи архива  

Проверка и очистка механизмов закрепления (Persistence):

!!! example ""
    **# crontab -u <user> -e**                                                        - Редактирование пользовательских задач cron  
    **# ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/**                      - Проверка системных директорий планировщика cron  
    **# systemctl stop <malicious.service> && systemctl disable <malicious.service>** - Остановка и отключение вредоносного systemd-сервиса  
    **# rm -f /etc/systemd/system/<malicious.service> && systemctl daemon-reload**    - Удаление unit-файла службы и перезагрузка конфигурации systemd  
    **# cat /etc/ld.so.preload && > /etc/ld.so.preload**                              - Проверка и очистка файла перехвата библиотек в user-space  
    **# grep -rn "curl\|wget\|base64\|/dev/tcp" /etc/profile /etc/bash.bashrc ~/.bashrc ~/.profile 2>/dev/null** - Поиск вредоносных вставок в профилях оболочек  
    **# cat ~/.ssh/authorized_keys**                                                  - Проверка доверенных SSH-ключей на наличие посторонних записей  
