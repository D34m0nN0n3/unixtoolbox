## 19 Базы данных

!!! abstract ""
    [PostgreSQL](#191-postgresql) | [MySQL](#192-mysql) | [SQLite](#193-sqlite)

### 19.1 PostgreSQL

#### Изменение пароля для пользователя

Для изменения пароля для пользователя пользователя в PostgreSQL, вы можете использовать следующую команду:

```bash
# psql -d template1 -U pgsql
> alter user pgsql with password 'pgsql_password';
```

Замените `pgsql` на имя пользователя, для которого вы хотите изменить пароль.

#### Создание пользователя и базы данных

Для создания пользователя и базы данных в PostgreSQL, вы можете использовать команды `createuser`, `dropuser`, `createdb` и `dropdb`. Ниже приведены примеры команд для создания пользователя с именем `bob` и базы данных с именем `bobdb`, используя суперпользователя базы данных `pgsql`:

```bash
# createuser -U pgsql -P bob
# createdb -U pgsql -O bob bobdb
```

Вы также можете удалить базу данных и пользователя с помощью следующих команд:

```bash
# dropdb bobdb
# dropuser bob
```

#### Общий механизм аутентификации в базе данных настраивается в файле pg_hba.conf

Файл `pg_hba.conf` определяет механизм контроля доступа в PostgreSQL. Если вы хотите предоставить удаленный доступ к базе данных, вам необходимо настроить этот файл. Вот примеры настроек для разрешения доступа:

!!! example ""
    ```plaintext
    # TYPE  DATABASE    USER        IP-ADDRESS        IP-MASK          METHOD
    host    bobdb       bob        212.117.81.42     255.255.255.255   password
    host    all         all        0.0.0.0/0                           password
    ```

##### Дополнение описания pg_hba.conf

Файл `pg_hba.conf` в PostgreSQL определяет механизм контроля доступа к базе данных. В нем можно настроить различные методы аутентификации для разных пользователей, баз данных и IP-адресов. Вот несколько дополнительных методов аутентификации, которые можно использовать в `pg_hba.conf`:

* **trust**: Этот метод позволяет подключаться к базе данных без аутентификации. Он полностью доверяет любому пользователю или IP-адресу. Например:

!!! example ""
    ```plaintext
    host    all         all        0.0.0.0/0        trust
    ```

* **md5**: Этот метод использует хэш-функцию MD5 для аутентификации пароля. Пользователю будет предложено ввести пароль при подключении к базе данных. Например:

!!! example ""
    ```plaintext
    host    all         all        0.0.0.0/0        md5
    ```

* **peer**: Этот метод используется для локальных подключений и основан на проверке операционной системы. Он позволяет пользователю подключаться к базе данных с тем же именем, что и его операционная система. Например:

!!! example ""
    ```plaintext
    local   all         all                        peer
    ```

* **ldap**: Этот метод использует протокол LDAP для аутентификации пользователей. Он позволяет интегрировать PostgreSQL с существующей инфраструктурой LDAP. Например:

!!! example ""
    ```plaintext
    host    all         all        0.0.0.0/0        ldap
    ```

* **cert**: Этот метод использует сертификаты для аутентификации пользователей. Он требует настройки SSL/TLS для подключения к базе данных. Например:

!!! example ""
    ```plaintext
    hostssl all         all        0.0.0.0/0        cert
    ```

Это лишь некоторые из возможных методов аутентификации, которые можно использовать в `pg_hba.conf`. Вы можете выбрать подходящий метод в зависимости от ваших потребностей и требований безопасности.

#### Резервное копирование и восстановление

Для резервного копирования и восстановления баз данных в PostgreSQL, вы можете использовать команды `pg_dump` и `psql`. Ниже приведены примеры команд для резервного копирования и восстановления отдельной базы данных:

!!! example ""
    ```bash
    # pg_dump --clean dbname > dbname_sql.dump
    # psql dbname < dbname_sql.dump
    ```

Вы также можете выполнить резервное копирование и восстановление всех баз данных (включая пользователей) с помощью следующих команд:

!!! example ""
    ```bash
    # pg_dumpall --clean > full.dump
    # psql -f full.dump postgres
    ```

При восстановлении всех баз данных рекомендуется начать с базы данных `postgres`, особенно при загрузке пустого кластера.

#### Дополнение описания и примеры других команд

В PostgreSQL существуют и другие команды, которые могут быть полезны при работе с базой данных. Вот несколько примеров:

##### Изменение текущей базы данных

Чтобы изменить текущую базу данных в PostgreSQL, вы можете использовать команду `\c` или `\connect`. Например, чтобы подключиться к базе данных с именем `mydb`, вы можете выполнить следующую команду:

!!! example ""
    ```bash
    # psql -U pgsql
    > \c mydb
    ```

##### Просмотр списка баз данных

Чтобы просмотреть список всех баз данных в PostgreSQL, вы можете использовать команду `\l` или `\list`. Например:

!!! example ""
    ```bash
    # psql -U pgsql
    > \l
    ```

##### Просмотр списка таблиц

Чтобы просмотреть список всех таблиц в текущей базе данных, вы можете использовать команду `\dt`. Например:

!!! example ""
    ```bash
    # psql -U pgsql -d mydb
    > \dt
    ```

##### Выполнение SQL-запросов

Чтобы выполнить произвольный SQL-запрос в PostgreSQL, вы можете использовать команду `\g` или `\gexec`. Например, чтобы выполнить запрос `SELECT * FROM users;`, вы можете выполнить следующую команду:

!!! example ""
    ```bash
    # psql -U pgsql -d mydb
    > SELECT * FROM users;
    > \g
    ```

#### Выход из psql

Чтобы выйти из интерактивной оболочки psql, вы можете использовать команду `\q` или `\quit`. Например:

!!! example ""
    ```bash
    # psql -U pgsql -d mydb
    > \q
    ```

Это лишь некоторые из команд, которые могут быть полезны при работе с PostgreSQL. Вы можете изучить документацию PostgreSQL для получения более подробной информации о доступных командах и их использовании.

### 19.2 MySQL

#### Изменение пароля для `root` или пользователя `mysql`

!!! example "Метод 1"
    **# /etc/init.d/mysql stop**  
    *или*  
    **# killall mysqld**  
    **# mysqld --skip-grant-tables**  
    **# mysqladmin -u root password 'newpasswd'**  
    **# /etc/init.d/mysql start**  

!!! example "Метод 2"
    **# mysql -u root mysql**  
    **mysql&gt; UPDATE USER SET PASSWORD=PASSWORD("newpassword") where user='root';**  
    **mysql&gt; FLUSH PRIVILEGES;**                             - Используйте имя пользователя вместо "root"  
    **mysql&gt; quit**  

#### Создание пользователя и базы данных (см. документацию [MySQL](http://dev.mysql.com/doc/refman/5.1/en/adding-users.html))

!!! example ""
    **# mysql -u root mysql**  
    **mysql&gt; CREATE USER 'bob'@'localhost' IDENTIFIED BY 'pwd';**            - создать только пользователя  
    **mysql&gt; CREATE DATABASE bobdb;**  
    **mysql&gt; GRANT ALL ON *.* TO 'bob'@'%' IDENTIFIED BY 'pwd';**            - Используйте localhost вместо % для ограничения сетевого доступа  
    **mysql&gt; DROP DATABASE bobdb;**                                          - Удалить базу данных  
    **mysql&gt; DROP USER bob;**                                                - Удалить пользователя  
    **mysql&gt; DELETE FROM mysql.user WHERE user='bob and host='hostname';**   - Альтернативная команда  
    **mysql&gt; FLUSH PRIVILEGES;**  

#### Предоставление удаленного доступа

Удаленный доступ обычно разрешен для определенной базы данных, а не для всех баз данных. Файл `/etc/my.cnf` содержит IP-адрес, к которому нужно подключиться. (На FreeBSD my.cnf не создается по умолчанию, скопируйте один `.cnf` файл из `/usr/local/share/mysql` в `/usr/local/etc/my.cnf`) В общем случае закомментируйте строку `bind-address =`.

!!! example ""
    **# mysql -u root mysql**  
    **mysql&gt; GRANT ALL ON bobdb.* TO bob@'xxx.xxx.xxx.xxx' IDENTIFIED BY 'PASSWORD';**  
    **mysql&gt; REVOKE GRANT OPTION ON foo.* FROM bar@'xxx.xxx.xxx.xxx';**  
    **mysql&gt; FLUSH PRIVILEGES;**                  - Используйте 'hostname' или также '%' для полного доступа  

#### Резервное копирование и восстановление

Резервное копирование и восстановление отдельной базы данных:

!!! example ""
    **# mysqldump -u root -psecret --add-drop-database dbname &gt; dbname_sql.dump**  
    **# mysql -u root -psecret -D dbname &lt; dbname_sql.dump**  

Резервное копирование и восстановление всех баз данных:

!!! example ""
    **# mysqldump -u root -psecret --add-drop-database --all-databases &gt; full.dump**  
    **# mysql -u root -psecret &lt; full.dump**  

Здесь "secret" - это пароль администратора mysql, после `-p` нет пробела. Если опция `-p` используется без указания пароля, пароль запрашивается в командной строке.

### 19.3 SQLite

[SQLite](http://www.sqlite.org) - это небольшая, мощная, автономная, безвременная SQL база данных.

#### Создание резервной копии и восстановление
Может быть полезным создать резервную копию и восстановить базу данных SQLite. Например, можно отредактировать файл резервной копии, чтобы изменить атрибут или тип столбца, а затем восстановить базу данных. Это проще, чем манипулировать с SQL-командами. Для работы с базой данных версии 3.x используйте команду sqlite3.

!!! example ""
    **# sqlite database.db .dump &gt; dump.sql**              - создание резервной копии  
    **# sqlite database.db &lt; dump.sql**                    - восстановление  

#### Конвертация базы данных версии 2.x в версию 3.x

!!! example ""
    **sqlite database_v2.db .dump | sqlite3 database_v3.db**