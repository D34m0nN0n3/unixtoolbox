## 3 Файловая система

!!! abstract ""
    [Разрешения](#31-разрешения) | [Информация о диске](#32-информация-о-диске) | [Загрузка](#33-загрузка) | [Использование диска](#34-точки-монтирования-системыиспользование-диска) | [Использование файлов](#35-использование-файлов) | [Монтирование файловой системы](#36-монтированиеперемонтирование-файловой-системы) | [Файл подкачки](#37-добавление-подкачки-на-лету) | [Монтирование SMB](#38-монтирование-smb-файловой-сетевой-папки) | [Монтирование образа](#39-монтирование-образа) | [ISO образы](#310-создание-и-запись-образа-iso) | [Файловые образы](#311-создать-образ-на-основе-файла) | [Производительность диска](#312-производительность-диска)

### 3.1 Разрешения

Изменение разрешений и владения с помощью команд `chmod` и `chown`.
Значение umask по умолчанию может быть изменено для всех пользователей в файле `/etc/profile` для Linux или `/etc/login.conf` для FreeBSD. Значение umask по умолчанию обычно равно `022`. Значение umask вычитается из `777`, поэтому `umask 022` приводит к разрешению `755`.

!!! info ""
    1 --x выполнение                        - Режим 764 = Владелец: выполнение/чтение/запись | Группа: чтение/запись | Другие: чтение  
    2 -w- запись  
    **ugo=a**: u=пользователь, g=группа, o=другие, a=все  

!!! example ""
    **# chmod *[ПАРАМЕТР] РЕЖИМ[,РЕЖИМ] ФАЙЛ***    - РЕЖИМ имеет форму `[ugoa]*([-+=]([rwxXst]))`  
    **# chmod 640 /var/log/maillog**         - Ограничить доступ к журналу `-rw-r-----`  
    **# chmod u=rw,g=r,o= /var/log/maillog** - То же самое, что и выше  
    **# chmod -R o-r /home/\***               - Рекурсивно удалить возможность чтения для всех пользователей  
    **# chmod u+s /path/to/prog**            - Установить бит SUID для исполняемого файла (будьте внимательны!)  
    **# find / -perm -u+s -print**           - Найти все программы с битом *SUID*  
    **# chown user:group /path/to/file**     - Изменить владельца и группу файла  
    **# chgrp group /path/to/file**          - Изменить группу владельца файла  
    **# chmod 640 \`find ./ -type f -print\`** - Изменить разрешения на `640` для всех файлов  
    **# chmod 751 \`find ./ -type d -print\`** - Изменить разрешения на `751` для всех каталогов  

### 3.2 Информация о диске

!!! example ""
    **# diskinfo -v /dev/ad2**               - информация о диске (сектор/размер) FreeBSD  
    **# hdparm -I /dev/sda**                 - информация о диске IDE/ATA (Linux)  
    **# fdisk /dev/ad2**                     - Отобразить и изменить таблицу разделов  
    **# smartctl -a /dev/ad2**               - Отобразить информацию о диске SMART  

### 3.3 Загрузка

#### FreeBSD

Чтобы загрузить старое ядро, если новое ядро не загружается, остановите загрузку во время обратного отсчета.

!!! example ""
    **# unload**  
    **# load kernel.old**  
    **# boot**  

### 3.4 Точки монтирования системы/Использование диска

!!! example ""
    **# mount | column -t**                  - Показать смонтированные файловые системы в системе  
    **# df**                                 - отобразить свободное место на диске и смонтированные устройства  
    **# cat /proc/partitions**               - Показать все зарегистрированные разделы (Linux)  

!!! example "Использование диска"
    **# du -sh \***                          - Размеры директорий в виде списка  
    **# du -csh**                            - Общий размер текущей директории  
    **# du -ks * | sort -n -r**              - Сортировка файлов по размеру в килобайтах  
    **# ls -lSr**                            - Показать файлы, с наибольшим размером последним  

### 3.5 Использование файлов

Это полезно, чтобы узнать, какой файл блокирует раздел, который нужно отмонтировать, и вызывает типичную ошибку:

!!! example ""
    **# umount /home/**  
    *umount: unmount of /home*             - Невозможно отмонтировать /home, так как файл блокирует доступ  
       *failed: Device busy*  

#### FreeBSD и большинство Unix-подобных систем

!!! example ""
    **# fstat -f /home                     - для точки монтирования  
    **# fstat -p PID                       - для приложения с указанным PID  
    **# fstat -u user                      - для пользователя по имени  

Найти открытый лог-файл (или другие открытые файлы), например, для Xorg:

!!! example ""
    **# ps ax | grep Xorg | awk '{print $1}'**  
    *1252*  
    **# fstat -p 1252**  
    USER     CMD          PID   FD MOUNT      INUM MODE         SZ|DV R/W  
    *root     Xorg        1252 root /             2 drwxr-xr-x     512  r*  
    *root     Xorg        1252 text /usr     216016 -rws--x--x  1679848 r*  
    *root     Xorg        1252    0 /var     212042 -rw-r--r--   56987  w*  

Файл с индексным номером (inum) 212042 является единственным файлом в /var:

!!! example ""
    **# find -x /var -inum 212042**  
    */var/log/Xorg.0.log*  

#### Linux

Найти открытые файлы на точке монтирования с помощью fuser или lsof:

!!! example ""
    **# fuser -m /home**                     - Список процессов, обращающихся к /home  
    **# lsof /home**  
    COMMAND   PID    USER   FD   TYPE DEVICE    SIZE     NODE NAME  
    *tcsh    29029 eedcoba  cwd    DIR   0,18   12288  1048587 /home/eedcoba (guam:/home)*  
    *lsof    29140 eedcoba  cwd    DIR   0,18   12288  1048587 /home/eedcoba (guam:/home)*  

!!! example "О приложении:"
    **# ps ax | grep Xorg | awk '{print $1}'**  
    *3324*  
    **# lsof -p 3324**  
    COMMAND  PID USER    FD  TYPE     DEVICE    SIZE       NODE NAME  
    *Xorg    3324 root    0w   REG        8,6   56296      12492 /var/log/Xorg.0.log*  

!!! example "Одиночный файл:"
    **# lsof /var/log/Xorg.0.log**  
    COMMAND  PID USER    FD  TYPE DEVICE  SIZE  NODE NAME  
    *Xorg    3324 root    0w   REG    8,6 56296 12492 /var/log/Xorg.0.log*  

### 3.6 Монтирование/перемонтирование файловой системы

!!! example "Например, CD-ROM. Если указано в /etc/fstab:"
    **# mount /cdrom**

Или найти устройство в `/dev/` или с помощью `dmesg`

#### FreeBSD

!!! example ""
    **# mount -v -t cd9660 /dev/cd0c /mnt**  - cdrom  
    **# mount_cd9660 /dev/wcd0c /cdrom**     - другой метод  
    **# mount -v -t msdos /dev/fd0c /mnt**   - дискета  

Запись в /etc/fstab:
!!! note ""
    Устройство        Точка монтирования      FStype  Опции         Dump    Pass  
    /dev/acd0         /cdrom                  cd9660  ro,noauto       0       0  

Для разрешения пользователям делать это:

!!! example ""
    **# sysctl vfs.usermount=1**  - Или добавьте строку *vfs.usermount=1* в `/etc/sysctl.conf`

#### Linux

!!! example ""
    **# mount -t auto /dev/cdrom /mnt/cdrom**   - типичная команда монтирования cdrom  
    **# mount /dev/hdc -t iso9660 -r /cdrom**   - типичное IDE-устройство  
    **# mount /dev/scd0 -t iso9660 -r /cdrom**  - типичный SCSI cdrom  
    **# mount /dev/sdc0 -t ntfs-3g /windows**   - типичный SCSI  

Запись в /etc/fstab:

!!! note ""
    /dev/cdrom   /media/cdrom  subfs noauto,fs=cdfss,ro,procuid,nosuid,nodev,exec 0 0

Монтирование раздела FreeBSD с помощью Linux
Найдите номер раздела с помощью `fdisk`, обычно это корневой раздел, но он также может быть другим срезом BSD. Если у FreeBSD есть несколько срезов, то они не указываются в таблице `fdisk`, но видны в `/dev/sda*` или `/dev/hda*`.

!!! example ""
    **# fdisk /dev/sda**                     - Найдите раздел FreeBSD  
    */dev/sda3   \*        5357        7905    20474842+  a5  FreeBSD*  
    **# mount -t ufs -o ufstype=ufs2,ro /dev/sda3 /mnt /dev/sda10 = /tmp; /dev/sda11 /usr**   - Другие срезы  

**Перемонтировать**

Перемонтируйте устройство без размонтирования. Необходимо, например, для `fsck`.

!!! example ""
    **# mount -o remount,ro /**              - Linux  
    **# mount -o ro -u /**                   - FreeBSD  

Скопировать сырые данные с `cdrom` в образ `iso` (стандартный размер блока 512 может вызывать проблемы):

!!! example ""
    **# dd if=/dev/cd0c of=file.iso bs=2048**

#### Virtualbox

Разрешить общую папку на хосте:

!!! example ""
    **# VBoxManage sharedfolder add "GuestName" --name "share" --hostpath "C:\hostshare"**

Подключить общую папку на гостевой машине (Linux, FreeBSD)

!!! example ""
    **# sudo mount -t vboxsf share /home/vboxshare**  (-o uid=1000,gid=1000)  
    *share /home/colin/share vboxsf defaults,uid=colin 0 0* - запись в fstab (при необходимости)  

#### OSX

!!! example ""
    **# diskutil list**                      - Список разделов диска  
    **# diskutil unmountDisk /dev/disk1**    - Размонтирование всего диска (все тома)  
    **# chflags hidden ~/Documents/folder**  - Скрыть папку (отменить с помощью unhidden)  

### 3.7 Добавление подкачки "на лету"

Предположим, нам нужно больше подкачки (прямо сейчас), скажем, 2 ГБ файла `/swap2gb` (только для Linux).

!!! example ""
    **# dd if=/dev/zero of=/swap2gb bs=1024k count=2000**  
    **# mkswap /swap2gb**                    - создать область подкачки  
    **# swapon /swap2gb**                    - активировать подкачку. Она теперь используется  
    **# swapoff /swap2gb**                   - когда закончите, деактивируйте подкачку  
    **# rm /swap2gb**  

### 3.8 Монтирование SMB-файловой сетевой папки

Предположим, мы хотим получить доступ к SMB-сетевой папке myshare на компьютере smbserver, адрес, указанный на компьютере с Windows, будет `\\smbserver\myshare\`.
Монтирование на `/mnt/smbshare`. Предупреждение&gt; cifs требует IP-адрес или DNS-имя, а не Windows-имя.

#### Linux/OSX

!!! example ""
    **# smbclient -U user -I 192.168.16.229 -L //smbshare/**    - Просмотр списка общих ресурсов  
    **# mount -t smbfs -o username=winuser //smbserver/myshare /mnt/smbshare**  
    **# mount -t cifs -o username=winuser,password=winpwd //192.168.16.229/myshare /mnt/share**  

Монтирование общего ресурса Samba через SSH-туннель

!!! example ""
    **# ssh -C -f -N -p 20022 -L 445:127.0.0.1:445 me@server**  - Подключение к порту 20022, туннель 445  
    **# mount -t smbfs //colin@localhost/colin ~/mnt**  
    **# mount_smbfs //colin:mypassword@127.0.0.1/private /Volumes/private** - Использую это на OSX + SSH  

!!! example "Также с помощью пакета `mount.cifs` можно сохранить учетные данные в файле, например, `/home/user/.smb`:"
    username=winuser  
    password=winpwd  

И монтировать следующим образом:

!!! example ""
    **# mount -t cifs -o credentials=/home/user/.smb //192.168.16.229/myshare /mnt/smbshare**

#### FreeBSD

Используйте -I для указания IP-адреса (или DNS-имени); smbserver - это Windows-имя.

!!! example ""
    **# smbutil view -I 192.168.16.229 //winuser@smbserver**    - Просмотр списка общих ресурсов  
    **# mount_smbfs -I 192.168.16.229 //winuser@smbserver/myshare /mnt/smbshare**  

### 3.9 Монтирование образа

!!! example ""
    **# hdiutil mount image.iso**                               - OS X

!!! example "Loop-back в linux"
    **# mount -t iso9660 -o loop file.iso /mnt**                - Монтирование образа CD  
    **# mount -t ext3 -o loop file.img /mnt**                   - Монтирование образа с файловой системой ext3  

FreeBSD. С использованием устройства в памяти (если необходимо, выполните команду kldload md.ko):

!!! example ""
    **# mdconfig -a -t vnode -f file.iso -u 0**  
    **# mount -t cd9660 /dev/md0 /mnt**  
    **# umount /mnt; mdconfig -d -u 0**                         - Очистка устройства md  

Или с использованием виртуального узла:

!!! example ""
    **# vnconfig /dev/vn0c file.iso; mount -t cd9660 /dev/vn0c /mnt**  
    **# umount /mnt; vnconfig -u /dev/vn0c**                    - Очистка устройства vn  

Solaris и FreeBSD с использованием интерфейса файла обратной связи или lofi:

!!! example ""
    **# lofiadm -a file.iso**  
    **# mount -F hsfs -o ro /dev/lofi/1 /mnt**  
    **# umount /mnt; lofiadm -d /dev/lofi/1**                   - Очистка устройства lofi  

### 3.10 Создание и запись образа ISO

Это будет копировать каждый сектор CD или DVD. Без опции `conv=notrunc` образ будет меньшего размера, если на диске содержится меньше данных. См. ниже примеры команды `dd`.

!!! example ""
    **# dd if=/dev/hdc of=/tmp/mycd.iso bs=2048 conv=notrunc**

Используйте mkisofs для создания образа CD/DVD из файлов в директории. Чтобы обойти ограничения имён файлов: -r позволяет использовать расширения Rock Ridge, общие для UNIX-систем, -J позволяет использовать расширения Joliet, используемые системами Microsoft. -L разрешает начинать имена файлов ISO9660 с точки.

!!! example ""
    **# mkisofs -J -L -r -V TITLE -o imagefile.iso /path/to/dir**  
    **# hdiutil makehybrid -iso -joliet -o dir.iso dir/**       - macOS  

В FreeBSD `mkisofs` находится в портах sysutils/cdrtools.

#### Запись образа ISO на CD/DVD

#### FreeBSD

По умолчанию FreeBSD не включает DMA для ATAPI-приводов. DMA можно включить с помощью команды sysctl и следующих аргументов или с помощью файла /boot/loader.conf с указанными ниже записями:

!!! example ""
    hw.ata.ata_dma="1"  
    hw.ata.atapi_dma="1"  

Используйте `burncd` с устройством ATAPI (burncd является частью базовой системы) и `cdrecord` (в sysutils/cdrtools) с приводом SCSI.

!!! example ""
    **# burncd -f /dev/acd0 data imagefile.iso fixate**       - Для ATAPI-привода  
    **# cdrecord -scanbus**                                   - Чтобы найти устройство-записыватель (подобно 1,0,0)  
    **# cdrecord dev=1,0,0 imagefile.iso**

#### Linux

Также используйте cdrecord с Linux, как описано выше. Кроме того, можно использовать собственный интерфейс ATAPI, который находится по адресу:

!!! example ""
    **# cdrecord dev=ATAPI -scanbus**

И записывайте CD/DVD так же, как описано выше.

**dvd+rw-tools**

Пакет dvd+rw-tools (FreeBSD: ports/sysutils/dvd+rw-tools) содержит все необходимое, включая growisofs для записи CD или DVD. В примерах используется устройство dvd, которое может быть символической ссылкой на `/dev/scd0` (типичный scsi в Linux) или `/dev/cd0` (типичный FreeBSD) или `/dev/rcd0c` (типичное символьное SCSI в NetBSD/OpenBSD) или `/dev/rdsk/c0t1d0s2` (пример Solaris с символьным SCSI/ATAPI-устройством CD-ROM). В руководстве [FreeBSD главы 18.7](http://www.freebsd.org/handbook/creating-dvds.html) имеется хорошая документация со множеством примеров.

!!! example ""
    *# -dvd-compat закрывает диск*  
    **# growisofs -dvd-compat -Z /dev/dvd=imagefile.iso**     - Запись существующего образа iso  
    **# growisofs -dvd-compat -Z /dev/dvd -J -R /p/to/data**  - Прямая запись  

#### Преобразовать файл .nrg Nero в файл .iso

Просто добавьте Nero 300Kb заголовок к обычному образу `iso`. Это можно сделать, используя команду `dd`.

!!! example ""
    **# dd bs=1k if=imagefile.nrg of=imagefile.iso skip=300**

#### Преобразовать образ bin/cue в файл .iso

Маленькая программа [bchunk](http://freshmeat.net/projects/bchunk/) может выполнить это. Она находится в портах FreeBSD в `sysutils/bchunk`.

!!! example ""
    **# bchunk imagefile.bin imagefile.cue imagefile.iso**

### 3.11 Создать образ на основе файла
Например, создадим раздел объемом 1 ГБ с использованием файла `/usr/vdisk.img`. Здесь мы используем vnode 0, но это также может быть 1.

#### FreeBSD

!!! example ""
    **# dd if=/dev/random of=/usr/vdisk.img bs=1K count=1M**  
    **# mdconfig -a -t vnode -f /usr/vdisk.img -u 0**         - Создает устройство /dev/md1  
    **# bsdlabel -w /dev/md0**  
    **# newfs /dev/md0c**  
    **# mount /dev/md0c /mnt**  
    **# umount /mnt; mdconfig -d -u 0; rm /usr/vdisk.img**    - Очистка устройства md  

Файловый образ можно автоматически монтировать при загрузке с помощью записи в файлы `/etc/rc.conf` и `/etc/fstab`. Протестируйте настройку с помощью команды: `# /etc/rc.d/mdconfig start` (перед этим удалите устройство md0 с помощью команды: # `mdconfig -d -u 0`).
Однако обратите внимание, что эта автоматическая настройка будет работать только в том случае, если файловый образ НЕ находится на разделе root. Причина в том, что скрипт `/etc/rc.d/mdconfig` выполняется очень рано во время загрузки, а раздел root все еще доступен только для чтения. Образы, расположенные за пределами раздела root, будут монтироваться позже с помощью скрипта `/etc/rc.d/mdconfig2`.

/boot/loader.conf:

!!! example ""
    md_load="YES"

/etc/rc.conf:

!!! example ""
    **# mdconfig_md0="-t vnode -f /usr/vdisk.img"**          - /usr не находится на разделе root

/etc/fstab: (0 0 в конце важно, оно указывает fsck игнорировать это устройство, поскольку оно еще не существует)

!!! example ""
    /dev/md0                /usr/vdisk      ufs     rw              0       0

Также возможно увеличение размера образа позднее, скажем, на 300 МБ.

!!! example ""
    **# umount /mnt; mdconfig -d -u 0**  
    **# dd if=/dev/zero bs=1m count=300 >> /usr/vdisk.img**  
    **# mdconfig -a -t vnode -f /usr/vdisk.img -u 0**  
    **# growfs /dev/md0**  
    **# mount /dev/md0c /mnt**                                - Раздел файла теперь больше на 300 МБ  

#### Linux

!!! example ""
    **# dd if=/dev/zero of=/usr/vdisk.img bs=1024k count=1024**  
    **# mkfs.ext3 /usr/vdisk.img**  
    **# mount -o loop /usr/vdisk.img /mnt**  
    **# umount /mnt; rm /usr/vdisk.img**                      - Очистка  

**Linux с использованием losetup**

`/dev/zero` гораздо быстрее, чем `urandom`, но менее безопасен для шифрования.

!!! example ""
    **# dd if=/dev/urandom of=/usr/vdisk.img bs=1024k count=1024**  
    **# losetup /dev/loop0 /usr/vdisk.img**                   - Создание и ассоциирование `/dev/loop0`  
    **# mkfs.ext3 /dev/loop0**  
    **# mount /dev/loop0 /mnt**  
    **# losetup -a**                                          - Проверка используемых петель  
    **# umount /mnt**  
    **# losetup -d /dev/loop0**                               - Отсоединение  
    **# rm /usr/vdisk.img**  

#### Создание файловой системы в памяти (memory file system)

Файловая система, работающая в памяти, очень быстра для приложений с интенсивным вводом-выводом. Как создать раздел размером 64 МБ, смонтированный по пути `/memdisk`:

#### FreeBSD

!!! example ""
    **# mount_mfs -o rw -s 64M md /memdisk**  
    **# umount /memdisk; mdconfig -d -u 0**                   - Очистка устройства md  
    *md     /memdisk     mfs     rw,-s64M    0   0*           - Запись в /etc/fstab  

#### Linux

!!! example ""
    **# mount -t tmpfs -osize=64m tmpfs /memdisk**

### 3.12 Производительность диска

Чтение и запись файла размером 1 ГБ на разделе `ad4s3c` (/home)

!!! example ""
    **# time dd if=/dev/ad4s3c of=/dev/null bs=1024k count=1000**  
    **# time dd if=/dev/zero bs=1024k count=1000 of=/home/1Gb.file**  
    **# hdparm -tT /dev/hda**      - Только для Linux  
