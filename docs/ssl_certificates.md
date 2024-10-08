## 11 Сертификаты SSL

!!! abstract ""
    [Порядок действий](#111-процедура) | [Настройка OpenSSL](#112-настройка-openssl) | [Создание центра сертификации](#113-создание-центра-сертификации) | [Создание запроса на подписание](#114-создание-запроса-на-подписание-сертификата) | [Подписание сертификата](#115-подписание-сертификата) | [Создание объединенного сертификата](#116-создание-объединенного-сертификата) | [Просмотр информации о сертификате](#117-просмотр-информации-о-сертификате)

Так называемые сертификаты `SSL/TLS` - это криптографические сертификаты открытых ключей, состоящие из открытого и закрытого ключа. Сертификаты используются для аутентификации конечных точек и шифрования данных. Они используются, например, на веб-сервере (`https`) или почтовом сервере (`imaps`).

### 11.1 Процедура

* Нам нужен центр сертификации, чтобы подписать наш сертификат. Этот шаг обычно выполняется поставщиком, например Thawte, Verisign и т.д., однако мы также можем создать свой собственный.
* Создать запрос на подписание сертификата. Этот запрос похож на неподписанный сертификат (открытая часть) и уже содержит всю необходимую информацию. Запрос на сертификат обычно отправляется поставщику для подписи. На этом этапе также создается закрытый ключ на локальной машине.
* Подписать сертификат центром сертификации.
* При необходимости объединить сертификат и ключ в один файл для использования приложением (веб-сервер, почтовый сервер и т. д.).

### 11.2 Настройка OpenSSL

!!! hint ""
    В разных дистрибутивах файл конфигурации расположение отличается. В RHEL он расположен по пути: `/etc/pki/tls/openssl.cnf` Проверить расположение можно командой: `find / -name openssl.cnf`

Мы используем `/usr/local/certs` как каталог для этого примера, проверьте или отредактируйте `/etc/ssl/openssl.cnf` соответственно вашим настройкам, чтобы знать, где будут созданы файлы. Вот относящиеся к делу части `openssl.cnf`:

!!! note ""
    *[ CA_default ]*  
    *dir = /usr/local/certs/CA* - Где все хранится  
    *certs = $dir/certs*        - Где хранятся выданные сертификаты  
    *crl_dir = $dir/crl*        - Где хранятся выданные crl  
    *database = $dir/index.txt* - Индексный файл базы данных.  

!!! example "Убедитесь, что каталоги существуют или создайте их"
    **# mkdir -p /usr/local/certs/CA**  
    **# cd /usr/local/certs/CA**  
    **# mkdir certs crl newcerts private**  
    **# echo "01" > serial** - Только если serial не существует  
    **# touch index.txt**  

Если вы намерены получить подписанный сертификат от поставщика, вам нужен только запрос на подписание сертификата (CSR). Этот CSR затем будет подписан поставщиком на ограниченное время (например, 1 год).

### 11.3 Создание центра сертификации

Если у вас нет центра сертификации от поставщика, вам придется создать свой собственный. Этот шаг не является обязательным, если вы намерены использовать поставщика для подписи запроса. Чтобы создать центр сертификации (ЦС):

!!! example ""
    **# openssl req -new -x509 -days 730 -config /etc/ssl/openssl.cnf \\**  
    **-keyout CA/private/cakey.pem -out CA/cacert.pem**  

### 11.4 Создание запроса на подписание сертификата

!!! info "Секция в конфиге отвечающая за формирования запроса"
    ```txt
    ####################################################################
    [ req ]
    default_bits            = 2048
    default_md              = sha256
    default_keyfile         = privkey.pem
    distinguished_name      = req_distinguished_name
    attributes              = req_attributes
    x509_extensions = v3_ca # The extensions to add to the self signed cert
    
    # Passwords for private keys if not present they will be prompted for
    # input_password = secret
    # output_password = secret
    
    # This sets a mask for permitted string types. There are several options.
    # default: PrintableString, T61String, BMPString.
    # pkix   : PrintableString, BMPString (PKIX recommendation before 2004)
    # utf8only: only UTF8Strings (PKIX recommendation after 2004).
    # nombstr : PrintableString, T61String (no BMPStrings or UTF8Strings).
    # MASK:XXXX a literal mask value.
    # WARNING: ancient versions of Netscape crash on BMPStrings or UTF8Strings.
    string_mask = utf8only
    
    # req_extensions = v3_req # The extensions to add to a certificate request
    
    [ req_distinguished_name ]
    countryName                     = Country Name (2 letter code)
    countryName_default             = XX
    countryName_min                 = 2
    countryName_max                 = 2
    
    stateOrProvinceName             = State or Province Name (full name)
    #stateOrProvinceName_default    = Default Province
    
    localityName                    = Locality Name (eg, city)
    localityName_default            = Default City
    
    0.organizationName              = Organization Name (eg, company)
    0.organizationName_default      = Default Company Ltd
    ```

Чтобы создать новый сертификат (для почтового сервера или веб-сервера, например), сначала создайте запрос на сертификат со своим закрытым ключом. Если ваше приложение не поддерживает шифрование закрытого ключа (например, UW-IMAP не поддерживает), отключите шифрование с `-nodes`.

!!! example ""
    **# openssl req -new -keyout newkey.pem -out newreq.pem \\**  
    **-config /etc/ssl/openssl.cnf**  
    **# openssl req -nodes -new -keyout newkey.pem -out newreq.pem \\**  
    **-config /etc/ssl/openssl.cnf**   - Без шифрования ключа  

Сохраните созданный CSR (`newreq.pem`), так как он может быть подписан снова при следующем продлении, подпись ограничит срок действия сертификата. Этот процесс также создал закрытый ключ `newkey.pem`.

!!! help "Для генерации запроса одной командой с созданием приватного ключа в 4096 бит"
    openssl req -new \  
    -newkey rsa:4096 -nodes -keyout your.key \  
    -out your.csr \  
    -subj "/C=RU/ST=Moscow/L=Moscow/O=RZD/CN=hostname.domain/emailAddress=admin@domain"  

### 11.5 Подписание сертификата

Запрос на сертификат должен быть подписан ЦС, чтобы быть действительным, обычно этот шаг выполняется поставщиком. Примечание: замените "servername" именем вашего сервера в следующих командах.

!!! example ""
    **# cat newreq.pem newkey.pem > new.pem**  
    **# openssl ca -policy policy_anything -out servernamecert.pem \\**  
    **-config /etc/ssl/openssl.cnf -infiles new.pem**  
    **# mv newkey.pem servernamekey.pem**  

Теперь servernamekey.pem - это закрытый ключ, а servernamecert.pem - сертификат сервера.

### 11.6 Создание объединенного сертификата

Сервер IMAP хочет иметь закрытый ключ и сертификат сервера в одном файле. И в целом это также проще обрабатывать, но файл должен храниться в безопасности! Apache также может хорошо с этим справиться. Создайте файл servername.pem, содержащий сертификат и ключ.

* Откройте закрытый ключ (servernamekey.pem) в текстовом редакторе и скопируйте закрытый ключ в файл "servername.pem".
* Сделайте то же самое с сертификатом сервера (servernamecert.pem).

!!! note "Конечный файл servername.pem должен выглядеть так"
    ```
    -----BEGIN RSA PRIVATE KEY-----  
    MIICXQIBAAKBgQDutWy+o/XZ/[...]-qK5LqQgT3c9dU6fcR+WuSs6aejdEDDqBRQ  
    -----END RSA PRIVATE KEY-----  
    ```
    ```
    -----BEGIN CERTIFICATE-----  
    MIIERzCCA7CgAwIBAgIBBDANB[...]-iG9w0BAQQFADCBxTELMAkGA1UEBhMCREUx  
    -----END CERTIFICATE-----  
    ```

!!! note "Теперь в каталоге `/usr/local/certs/` есть"
    *CA/private/cakey.pem*     -закрытый ключ ЦС  
    *CA/cacert.pem*            -открытый ключ ЦС  
    *certs/servernamekey.pem*  -закрытый ключ сервера  
    *certs/servernamecert.pem* -подписанный сертификат сервера  
    *certs/servername.pem*     -сертификат сервера с закрытым ключом  

**Храните закрытый ключ в безопасности!**

### 11.7 Преобразование формата сертификата

#### PEM to PKCS12

!!! example ""
    openssl pkcs12 -export -name "yourdomain-digicert-(expiration date)" \  
    -out yourdomain.pfx -inkey yourdomain.key -in yourdomain.crt

#### PKCS12 to PEM

!!! example "Используйте следующую команду, чтобы извлечь закрытый ключ из файла PKCS#12 (.pfx) и преобразовать его в закрытый ключ в формате PEM"
    openssl pkcs12 -in yourdomain.pfx -nocerts -out yourdomain.key -nodes

!!! example "Используйте следующую команду, чтобы извлечь сертификат из файла PKCS#12 (.pfx) и преобразовать его в сертификат в кодировке PEM"
    openssl pkcs12 -in yourdomain.pfx -nokeys -clcerts -out yourdomain.crt

#### PEM to DER

!!! example "Используйте следующую команду для преобразования сертификата в кодировке PEM в сертификат в кодировке DER"
    openssl x509 -inform PEM -in yourdomain.crt -outform DER -out yourdomain.der

!!! example "Используйте следующую команду для преобразования закрытого ключа, закодированного в PEM, в закрытый ключ, закодированный в DER"
    openssl rsa -inform PEM -in yourdomain.key -outform DER -out yourdomain_key.der

#### DER to PEM

!!! example "Используйте следующую команду для преобразования сертификата в кодировке DER в сертификат в кодировке PEM"
    openssl x509 -inform DER -in yourdomain.der -outform PEM -out yourdomain.crt

!!! example "Используйте следующую команду для преобразования закрытого ключа, закодированного в DER, в закрытый ключ, закодированный в PEM"
    openssl rsa -inform DER -in yourdomain_key.der -outform PEM -out yourdomain.key

### 11.8 Просмотр информации о сертификате

Чтобы просмотреть информацию о сертификате, просто выполните:

!!! example ""
    **# openssl x509 -text -in servernamecert.pem** - Просмотр информации о сертификате  
    **# openssl req -noout -text -in server.csr**   - Просмотр информации о запросе  
    **# openssl s_client -connect cb.vu:443**       - Проверка сертификата веб-сервера  
    **# echo quit | openssl s_client -showcerts -servername example.com -connect example.com:443 > cacert.pem**   - Выгрузить корневой сертификат CA из цепочки веб-сервера  

!!! hint "Утилиты online"
    https://www.cryptool.org/en/cto/openssl/  
    https://www.ssl.com/online-csr-and-key-generator/  
    https://github.com/linux-system-roles/certificate  
