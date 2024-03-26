## 16 Установка программного обеспечения

!!! abstract ""
    [Списки пакетов](#161-список-установленных-пакетов) | [Установка и удаление](#162-добавлениеудаление-программного-обеспечения) | [Пакетные менеджеры](#163-пакетные-менеджеры) | [Библиотеки](#164-путь-к-библиотекам)

Обычно менеджер пакетов использует переменную proxy для http/ftp-запросов. В файле `.bashrc`:

!!! example ""
    *export http_proxy=http://proxy_server:3128*  
    *export ftp_proxy=http://proxy_server:3128*  

!!! hint ""
    Во внутрених сетях передачи данных организации используются системы управления контентом, на базе Katello.

### 16.1 Список установленных пакетов

!!! example ""
    **# rpm -qa**                            - Список установленных пакетов (RH, SuSE, основанные на RPM)  
    **# yum list installed**                 - RedHat 7  
    **# dnf list --installed**               - RedHat 8 и 9  
    **# dpkg -l**                            - Debian, Ubuntu  
    **# pkg_info**                           - FreeBSD список всех установленных пакетов  
    **# pkg_info -W smbd**                   - FreeBSD показать, к какому пакету относится smbd  
    **# pkginfo**                            - Solaris  

### 16.2 Добавление/удаление программного обеспечения

Front-ends: yast2/yast для SuSE, redhat-config-packages для Red Hat.

!!! example ""
    **# rpm -i <pkgname.rpm>**                  - Установить пакет (RH, SuSE, основанные на RPM)  
    **# rpm -e <pkgname>**                      - Удалить пакет  

### 16.3 Пакетные менеджеры

#### RedHat Yum ([см. документацию](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-yum))

!!! example ""
    **# yum install vim**                 - Установить пакет vim  
    **# yum remove vim**                  - Удалить пакет vim  
    **# yum search vim**                  - Поиск пакетов vim  

#### RedHat DNF ([см. документацию](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/index))

!!! example ""
    **# dnf install vim**                 - Установить пакет vim  
    **# dnf remove vim**                  - Удалить пакет vim  
    **# dnf search vim**                  - Поиск пакетов vim  

#### SuSE zypper ([см. документацию и шпаргалку](http://en.opensuse.org/SDB:Zypper_usage))

!!! example ""
    **# zypper refresh**                     - Обновить репозитории  
    **# zypper install vim**                 - Установить пакет vim  
    **# zypper remove vim**                  - Удалить пакет vim  
    **# zypper search vim**                  - Поиск пакетов vim  
    **# zypper update vim**                  - Обновление пакета vim  

#### Debian

!!! example ""
    **# apt-get update**                     - Сначала обновить списки пакетов  
    **# apt-get install emacs**              - Установить пакет emacs  
    **# dpkg --remove emacs**                - Удалить пакет emacs  
    **# dpkg -S file**                       - найти пакет, к которому относится файл  

#### Gentoo

Gentoo использует emerge в качестве основы своей системы управления пакетами "Portage".

!!! example ""
    **# emerge --sync**                      - сначала синхронизировать локальное дерево portage  
    **# emerge -u packagename**              - установить или обновить пакет  
    **# emerge -C packagename**              - удалить пакет  
    **# revdep-rebuild**                     - исправить зависимости  

#### Solaris

Путь <cdrom> обычно /cdrom/cdrom0.

!!! example ""
    **# pkgadd -d <cdrom>/Solaris_9/Product SUNWgtar**
    **# pkgadd -d SUNWgtar**                 - добавить скачанный пакет (сначала выполнить bunzip2)  
    **# pkgrm SUNWgtar**                     - удалить пакет  

### FreeBSD

!!! example ""
    **# pkg_add -r rsync**                   - загрузить и установить rsync  
    **# pkg_delete /var/db/pkg/rsync-xx**    - удалить пакет rsync  

Задайте переменную PACKAGESITE, чтобы указать, откуда загружать пакеты. Например:

!!! example ""
    **# export PACKAGESITE=ftp://ftp.freebsd.org/pub/FreeBSD/ports/i386/packages/Latest/**  
     *или ftp://ftp.freebsd.org/pub/FreeBSD/ports/i386/packages-6-stable/Latest/*  

[Порты](http://www.freebsd.org/handbook/ports.html) FreeBSD

Дерево портов `/usr/ports/` - это коллекция программного обеспечения, готового к компиляции и установке (см. man ports). Порты обновляются с помощью программы `portsnap`.

!!! example ""
    **# portsnap fetch extract**             - создать дерево при первом запуске  
    **# portsnap fetch update**              - обновить дерево портов  
    **# cd /usr/ports/net/rsync/**           - выбрать пакет для установки  
    **# make install distclean**             - установить и очистить (см. также `man ports`)  
    **# make package**                       - создать бинарный пакет для этого порта  
    **# pkgdb -F**                           - исправить базу данных реестра пакетов  
    **# portsclean -C -DD**                  - очистить рабочий каталог и каталог `distdir` (часть portupgrade)  

OS X [MacPorts](http://guide.macports.org/) (используйте sudo для всех команд)

!!! example ""
    **# port selfupdate**                      - обновить дерево портов (безопасно)  
    **# port installed**                       - перечислить установленные порты  
    **# port deps apache2**                    - перечислить зависимости для этого порта  
    **# port search pgrep**                    - поиск по строке  
    **# port install proctools**               - установить этот пакет  
    **# port variants ghostscript**            - перечислить варианты этого порта  
    **# port -v install ghostscript +no_x11**  - -no_x11 для отрицательного значения  
    **# port clean --all ghostscript**         - очистить рабочий каталог порта  
    **# port upgrade ghostscript**             - обновить этот порт  
    **# port uninstall ghostscript**           - удалить этот порт  
    **# port -f uninstall installed**          - Деустановить все  

### 16.4 Путь к библиотекам

Из-за сложных зависимостей и динамической компоновки программы трудно копировать на другую систему или дистрибутив. Тем не менее, для небольших программ с небольшими зависимостями отсутствующие библиотеки можно скопировать. Библиотеки, которые используются во время выполнения (включая отсутствующие), проверяются с помощью ldd и управляются с помощью ldconfig.

!!! example ""
    **# ldd /usr/bin/rsync**                  - Список всех необходимых библиотек для выполнения  
    **# otool -L /usr/bin/rsync**             - Вариант для OS X для ldd  
    **# ldconfig -n /путь/к/библиотекам/**    - Добавить путь к каталогам с общими библиотеками  
    **# ldconfig -m /путь/к/библиотекам/**    - FreeBSD  
    **# LD_LIBRARY_PATH**                     - Переменная, устанавливающая путь к библиотекам связи  
