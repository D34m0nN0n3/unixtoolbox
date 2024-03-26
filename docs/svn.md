## 13 SVN

!!! abstract ""
    [Настройка сервера](#131-настройка-сервера) | [Использование SVN](#132-команды-и-использование-svn)

[Subversion (SVN)](http://subversion.tigris.org/) - это система управления версиями, разработанная для замены CVS (Concurrent Versions System). Концепция похожа на CVS, но устранены многие недостатки. См. также книгу по [SVN](http://svnbook.red-bean.com/en/1.4/).

### 13.1 Настройка сервера

Инициализация репозитория довольно проста (здесь, например, должна существовать директория `/home/svn/`):

!!! example ""
    **# svnadmin create --fs-type fsfs /home/svn/project1**

Теперь доступ к репозиторию осуществляется так:

* `file://` Прямой доступ к файловой системе с помощью клиента svn. Для этого требуются локальные разрешения на файловой системе.
* `svn://` или `svn+ssh://` Доступ по сети с использованием сервера svnserve (также через SSH). Для этого требуются локальные разрешения на файловой системе (порт по умолчанию: 2690/tcp).
* `http://` Доступ по сети с использованием webdav с помощью apache. Для этого не требуются локальные пользователи.

Используя локальную файловую систему, теперь можно импортировать и затем проверить существующий проект. В отличие от CVS, не нужно выполнять команду cd в директории проекта, достаточно указать полный путь:

!!! example ""
    **# svn import /project1/ file:///home/svn/project1/trunk -m 'Initial import'**  
    **# svn checkout file:///home/svn/project1**  

Новая директория "trunk" - это просто соглашение, она не требуется.

#### Удаленный доступ с помощью SSH

Для доступа к репозиторию через SSH не требуется особая настройка, просто замените `file://` на `svn+ssh/hostname`. Например:

!!! example ""
    **# svn checkout svn+ssh://hostname/home/svn/project1**

Как и с локальным доступом к файлам, каждому пользователю необходим доступ по SSH к серверу (с локальной учетной записью) и также права на чтение/запись. Этот метод может быть подходящим для небольшой группы. Все пользователи могут принадлежать к группе subversion, которой принадлежит репозиторий, например:

!!! example ""
    **# groupadd subversion**  
    **# groupmod -A user1 subversion**  
    **# chown -R root:subversion /home/svn**  
    **# chmod -R 770 /home/svn**  

#### Удаленный доступ с помощью http (apache)

Удаленный доступ через http (https) - единственное хорошее решение для большой группы пользователей. Этот метод использует аутентификацию apache, а не локальные аккаунты. Вот типичная, но небольшая конфигурация apache:

!!! note ""
    *LoadModule dav_module         modules/mod_dav.so*  
    *LoadModule dav_svn_module     modules/mod_dav_svn.so*  
    *LoadModule authz_svn_module   modules/mod_authz_svn.so*    - Только для контроля доступа  

!!! note ""
    <location svn="">  
      DAV svn  
      *# Любой URL "/svn/foo" будет сопоставлен с хранилищем /home/svn/foo*  
      SVNParentPath /home/svn  
      AuthType Basic  
      AuthName "Subversion repository"  
      AuthzSVNAccessFile /etc/apache2/svn.acl  
      AuthUserFile /etc/apache2/svn-passwd
      Require valid-user  
    </location>  

Серверу apache требуется полный доступ к хранилищу:

!!! example ""
    **# chown -R www:www /home/svn**

!!! note "Создание пользователя с помощью htpasswd2"
    **# htpasswd -c /etc/svn-passwd user1**  - `-c` создает файл

!!! note "Пример контроля доступа svn.acl"
    *# По умолчанию доступ на чтение. "\* =" будет означать отсутствие доступа по умолчанию*
    [/]
    * = r
    [groups]
    project1-developers = joe, jack, jane
    *# Даем доступ на запись разработчикам*
    [project1:]
    @project1-developers = rw

### 13.2 Команды и использование SVN

См. также Быструю справку по [Subversion](http://www.cs.put.poznan.pl/csobaniec/Papers/svn-refcard.pdf). [Tortoise SVN](http://tortoisesvn.tigris.org) - хороший интерфейс для Windows.

#### Импорт

Новый проект, это каталог с некоторыми файлами, импортируется в хранилище с помощью команды `import`. Import также используется для добавления каталога со всем его содержимым к существующему проекту.

!!! example ""
    **# svn help import**                                - Получить справку по любой команде  
     *# Добавить новый каталог (с содержимым) в директорию src на проекте project1*  
    **# svn import /project1/newdir http://host.url/svn/project1/trunk/src -m 'add newdir'**  

#### Типичные команды SVN

!!! example ""
    **# svn co http://host.url/svn/project1/trunk**      - Настройка последней версии  
        *# Метки и ветки создаются путем копирования*  
    **# svn mkdir http://host.url/svn/project1/tags/**   - Создание директории меток  
    **# svn copy -m "Tag rc1 rel." http://host.url/svn/project1/trunk \\**  
                                 **http://host.url/svn/project1/tags/1.0rc1**  
    **# svn status [--verbose]**                         - Проверка статуса файлов в рабочей директории  
    **# svn add src/file.h src/file.cpp**                - Добавление двух файлов  
    **# svn commit -m 'Added new class file'**           - Фиксация изменений с сообщением  
    **# svn ls http://host.url/svn/project1/tags/**      - Показать все теги  
    **# svn move foo.c bar.c**                           - Переименовать файлы  
    **# svn delete some_old_file**                       - Удалить файлы  
