## 9 Шифрование файлов

!!! abstract ""
    [OpenSSL](#91-openssl) | [GPG](#92-gpg)

### 9.1 OpenSSL

#### Один файл

Зашифровать и расшифровать:

!!! example ""
    **# openssl aes-128-cbc -salt -in file -out file.aes**    - Зашифровать  
    **# openssl aes-128-cbc -d -salt -in file.aes -out file** - Расшифровать  

Обратите внимание, что файл может быть архивом `tar`.

#### Заархивировать `tar` и зашифровать целый каталог

!!! example ""
    **# tar -cf - directory | openssl aes-128-cbc -salt -out directory.tar.aes** - Зашифровать  
    **# openssl aes-128-cbc -d -salt -in directory.tar.aes | tar -x -f -**       - Расшифровать  

#### Архивировать `tar`, сжать `zip` и зашифровать целый каталог

!!! example ""
    **# tar -zcf - directory | openssl aes-128-cbc -salt -out directory.tar.gz.aes** - Зашифровать  
    **# openssl aes-128-cbc -d -salt -in directory.tar.gz.aes | tar -xz -f -**       - Расшифровать  

* Используйте `-k mysecretpassword` после `aes-128-cbc`, чтобы избежать интерактивного запроса пароля. Однако имейте в виду, что это крайне небезопасно.
* Используйте `aes-256-cbc` вместо `aes-128-cbc`, чтобы получить еще более сильное шифрование. Это также требует больше процессорных ресурсов.

### 9.2 GPG

GnuPG широко известен для шифрования и подписи электронных писем или любых данных. Кроме того, gpg также предоставляет продвинутую систему управления ключами. Этот раздел охватывает только шифрование файлов, а не использование электронной почты, подписи или Web-Of-Trust.

Простейшее шифрование выполняется симметричным шифром. В этом случае файл шифруется паролем, и любой, кто знает пароль, может расшифровать его, поэтому ключи не нужны. Gpg добавляет расширение ".gpg" к зашифрованным именам файлов.

!!! example ""
    **# gpg -c file**  - Зашифровать файл с паролем  
    **# gpg file.gpg** - Расшифровать файл (необязательно -o другой_файл)  

#### Использование ключей

Для более подробной информации см. GPG Краткое руководство http://www.madboa.com/geek/gpg-quickstart и Основы [GPG/PGP](http://aplawrence.com/Basics/gpg.html) и документацию [gnupg](http://gnupg.org/documentation) среди прочего.

Закрытые и открытые ключи - это сердце асимметричной криптографии. Важно запомнить:

* Ваш открытый ключ используется другими для шифрования файлов, которые можете расшифровать только вы как получатель (даже тот, кто зашифровал файл, не может его расшифровать). Открытый ключ предназначен для распространения.
* Ваш закрытый ключ зашифрован вашей фразой-паролем и используется для расшифровки файлов, которые были зашифрованы с вашим открытым ключом. Закрытый ключ должен храниться в безопасности. Также если ключ или фраза-пароль утеряны, утеряны и все файлы, зашифрованные с вашим открытым ключом.
* Файлы ключей называются ключевыми кольцами, поскольку могут содержать больше одного ключа.

Сначала сгенерируйте пару ключей. По умолчанию все в порядке, однако вам понадобится ввести как минимум ваше полное имя, электронную почту и необязательно комментарий. Комментарий полезен для создания более чем одного ключа с одним и тем же именем и электронной почтой. Также вам следует использовать "фразу-пароль", а не простой пароль.

!!! example ""
    **# gpg --gen-key** - Это может занять много времени  

Ключи хранятся в `~/.gnupg/` в Unix, в Windows обычно хранятся в `C:/Users/%USERNAME%/AppData/Roaming/gnupg/`.

!!! example ""
    **~/.gnupg/pubring.gpg** - Содержит ваши открытые ключи и все другие импортированные  
    **~/.gnupg/secring.gpg** - Может содержать больше одного закрытого ключа  

!!! info "Краткое напоминание наиболее используемых параметров:"
    -e зашифровать данные  
    -d расшифровать данные  
    -r ИМЯ зашифровать для получателя ИМЯ (или 'Полное Имя' или 'email@domain')  
    -a создать ascii выходной ключ  
    -o использовать в качестве выходного файла  

В примерах используются 'Ваше Имя' и 'Алиса', поскольку ключи обозначаются по электронной почте, полному имени или частичному имени. Например, я могу использовать 'Коля' или 'c@cb.vu' для своего ключа [Колин Баршел (cb.vu) <c@cb.vu>].

#### Шифрование только для личного пользования

Нет необходимости экспортировать/импортировать какие-либо ключи для этого. У вас уже есть оба.

!!! example ""
    **# gpg -e -r 'Ваше Имя' file** - Зашифровать вашим открытым ключом
    **# gpg -o file -d file.gpg**   - Расшифровать. Используйте -o или вывод в stdout

Шифрование - Расшифровка с ключами

Сначала вам нужно экспортировать свой открытый ключ, чтобы кто-то другой мог использовать его. И вам также нужно импортировать открытый, например, от Алисы, чтобы зашифровать файл для нее.
Вы можете обрабатывать ключи либо в простых текстовых файлах ascii, либо использовать открытый сервер ключей.
Например, Алиса экспортирует свой открытый ключ, а вы импортируете его, затем вы можете зашифровать файл для нее. То есть только Алиса сможет расшифровать его.

!!! example ""
    **# gpg -a -o alicekey.asc --export 'Алиса'**               - Алиса экспортировала свой ключ в текстовый файл ascii.  
    **# gpg --send-keys --keyserver subkeys.pgp.net KEYID**     - Алиса разместила свой ключ на сервере.  
    **# gpg --import alicekey.asc**                             - Вы импортируете ее ключ в свой pubring.  
    **# gpg --search-keys --keyserver subkeys.pgp.net 'Алиса'** - или получите ее ключ с сервера.  

После импорта ключей очень просто зашифровать или расшифровать файл:

!!! example ""
    **# gpg -e -r 'Алиса' file**  - Зашифровать файл для Алисы.
    **# gpg -d file.gpg -o file** - Расшифровать файл, зашифрованный Алисой для вас.

#### Администрирование ключей

!!! example ""
    **# gpg --list-keys**                 # список открытых ключей и просмотр KEYIDS  
    *KEYID следует за '/' например для: pub 1024D/D12B77CE KEYID - D12B77CE*  
    **# gpg --gen-revoke 'Ваше имя'**     # сгенерировать сертификат отзыва  
    **# gpg --list-secret-keys**          # список закрытых ключей  
    **# gpg --delete-keys ИМЯ**           # удалить открытый ключ из локального ключевого кольца  
    **# gpg --delete-secret-key ИМЯ**     # удалить секретный ключ из локального ключевого кольца  
    **# gpg --fingerprint KEYID**         # Показать отпечаток ключа  
    **# gpg --edit-key KEYID**            # Редактировать ключ (например, подписать или добавить/удалить email)  
