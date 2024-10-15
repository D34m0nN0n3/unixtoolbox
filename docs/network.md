## 4 Сеть

!!! abstract ""
    [Диагностика](#41-диагностика) | [Маршрутизация](#42-маршрутизация) | [Дополнительные IP](#43-настройка-дополнительных-ip-адресов) | [Изменение MAC-адреса](#44-изменение-mac-адреса) | [Порты](#45-используемые-порты) | [Брандмауэр](#46-брандмауэр) | [IP-перенаправление](#47-ip-forward-для-маршрутизации) | [NAT](#48-nat-network-address-translation) | [DNS](#49-dns) | [DHCP](#410-dhcp) | [Трафик](#411-анализ-трафика) | [QoS](#412-управление-трафиком-qos) | [NIS](#413-отладка-nis) | [Netcat](#414-netcat) | [cURL](#415-curl) | [HTTP Status Codes](#416-http-status-codes)

Отладка (см. также анализ трафика)

### 4.1 Диагностика

#### Linux

!!! example ""
    **# ethtool eth0**                          - Показать статус Ethernet (заменяет mii-diag)  
    **# ethtool -s eth0 speed 100 duplex full** - Принудительно установить 100 Мбит/с полнодуплексный режим  
    **# ethtool -s eth0 autoneg off**           - Отключить автоматическую настройку  
    **# ethtool -p eth1**                       - Мигать светодиодом Ethernet - очень полезно, если поддерживается  
    **# ip link show**                          - Отобразить все интерфейсы в Linux (аналогично ifconfig)  
    **# ip link set eth0 up**                   - Включить устройство (или выключить). То же самое, что "ifconfig eth0 up"  
    **# ip addr show**                          - Отобразить все IP-адреса в Linux (аналогично ifconfig)  
    **# ip neigh show**                         - Аналогично arp -a  

#### Другие ОС

!!! example ""
    **# ifconfig fxp0**                                      - Проверить поле "media" в FreeBSD  
    **# arp -a**                                             - Проверить запись ARP маршрутизатора (или хоста) (все ОС)  
    **# ping example.com**                                         - Первое, что нужно попробовать...  
    **# traceroute example.com**                                   - Вывести путь маршрута до пункта назначения  
    **# ifconfig fxp0 media 100baseTX mediaopt full-duplex** - 100 Мбит/с полнодуплексный режим (FreeBSD)  
    **# netstat -s**                                         - Системная статистика для каждого сетевого протокола  

Дополнительные команды, которые не всегда устанавливаются по умолчанию, но легко находятся:

!!! example ""
    **# arping 192.168.16.254**     - Пинг на уровне Ethernet  
    **# tcptraceroute -f 5 example.com**  - Использует TCP вместо ICMP для трассировки через брандмауэры  

!!! error "Обнаружение коллизий в сети"
    Для обнаружения одного IP адреса на разных хостах необходимо выполнить `arping` с любого узла из той же сети:  
    **# arping -I <имя интерфейса> -c 4 <конфликтующий IP адрес>**  
    Если IP адрес принадлежит нескольким устройства, то в ответе будут содержаться MAC адреса этих устройств.

### 4.2 Маршрутизация

Вывод таблицы маршрутизации

!!! example ""
    **# route -n**                  - Linux или используйте "ip route"  
    **# netstat -rn**               - Linux, BSD и UNIX  
    **# route print**               - Windows  

Добавление и удаление маршрута

#### FreeBSD

!!! example ""
    **# route add 212.117.0.0/16 192.168.1.1**  
    **# route delete 212.117.0.0/16**  
    **# route add default 192.168.1.1**  

!!! note "Добавление маршрута постоянно в /etc/rc.conf"
    *static_routes="myroute"*  
    *route_myroute="-net 212.117.0.0/16 192.168.1.1" * 

#### Linux

!!! example ""
    **# route add -net 192.168.20.0 netmask 255.255.255.0 gw 192.168.16.254**  
    **# ip route add 192.168.20.0/24 via 192.168.16.254**                           - то же самое с использованием ip route  
    **# route add -net 192.168.20.0 netmask 255.255.255.0 dev eth0**  
    **# route add default gw 192.168.51.254**  
    **# ip route add default via 192.168.51.254 dev eth0**                          - то же самое с использованием ip route  
    **# route delete -net 192.168.20.0 netmask 255.255.255.0**  

#### Solaris

!!! example ""
    **# route add -net 192.168.20.0 -netmask 255.255.255.0 192.168.16.254**  
    **# route add default 192.168.51.254 1**                                     - 1 = количество прыжков до следующего шлюза  
    **# route change default 192.168.50.254 1**  

Постоянные записи устанавливаются в файле `/etc/defaultrouter`.

#### Windows

!!! example ""
    **# Route add 192.168.50.0 mask 255.255.255.0 192.168.51.253**  
    **# Route add 0.0.0.0 mask 0.0.0.0 192.168.51.254**  

Используйте add -p, чтобы сделать маршрут постоянным.

### 4.3 Настройка дополнительных IP-адресов

#### Linux

!!! example ""
    **# ifconfig eth0 192.168.50.254 netmask 255.255.255.0**       - Первый IP  
    **# ifconfig eth0:0 192.168.51.254 netmask 255.255.255.0**     - Второй IP  
    **# ip addr add 192.168.50.254/24 dev eth0**                   - Эквивалентные команды ip  
    **# ip addr add 192.168.51.254/24 dev eth0 label eth0:1**  

#### FreeBSD

!!! example ""
    **# ifconfig fxp0 inet 192.168.50.254/24**                     - Первый IP  
    **# ifconfig fxp0 alias 192.168.51.254 netmask 255.255.255.0** - Второй IP  
    **# ifconfig fxp0 -alias 192.168.51.254**                      - Удалить второй IP-алиас  

!!! note "Постоянные записи в файле `/etc/rc.conf`"
    *ifconfig_fxp0="inet 192.168.50.254  netmask 255.255.255.0"*  
    *ifconfig_fxp0_alias0="192.168.51.254 netmask 255.255.255.0"*  

#### Solaris

Проверить настройки с помощью команды `ifconfig -a`

!!! example ""
    **# ifconfig hme0 plumb**                                      - Включить сетевую карту
    **# ifconfig hme0 192.168.50.254 netmask 255.255.255.0 up**    - Первый IP
    **# ifconfig hme0:1 192.168.51.254 netmask 255.255.255.0 up**  - Второй IP

### 4.4 Изменение MAC-адреса

Обычно перед изменением MAC-адреса необходимо выключить интерфейс. Не говорите мне, зачем вам нужно изменить MAC-адрес...

!!! example ""
    **# ifconfig eth0 down**  
    **# ifconfig eth0 hw ether 00:01:02:03:04:05**      - Linux  
    **# ifconfig fxp0 link 00:01:02:03:04:05**          - FreeBSD  
    **# ifconfig hme0 ether 00:01:02:03:04:05**         - Solaris  
    **# sudo ifconfig en0 ether 00:01:02:03:04:05**     - OS X Tiger, Snow Leopard LAN*  
    **# sudo ifconfig en0 lladdr 00:01:02:03:04:05**    - OS X Leopard  

*Обычный беспроводной интерфейс - `en1` и перед изменением MAC-адреса необходимо отключиться от любой сети (инструкция osxdaily).

!!! example ""
    **# echo "alias airport='/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'"\\**  
    **&gt;&gt; ~/.bash_profile**         # или создайте символическую ссылку на /usr/sbin  
    **# airport -z**                     # Отключиться от беспроводных сетей  
    **# airport -I**                     # Получить информацию о беспроводной сети  

Для Windows существует множество инструментов. Например, [etherchange](http://ntsecurity.nu/toolbox/etherchange). Или ищите "Mac Makeup", "smac".

### 4.5 Используемые порты

Слушающие открытые порты:

!!! example ""
    **# netstat -an | grep LISTEN**  
    **# lsof -i**                                       - Показать все интернет-соединения в Linux  
    **# socklist**                                      - Отобразить список открытых сокетов в Linux  
    **# sockstat -4**                                   - Список приложений FreeBSD  
    **# netstat -anp --udp --tcp | grep LISTEN**        - Linux  
    **# netstat -tup**                                  - Список активных соединений в/из системы (Linux)  
    **# netstat -tupl**                                 - Список прослушиваемых портов в системе (Linux)  
    **# netstat -ano**                                  - Windows  

### 4.6 Брандмауэр

Проверка работы брандмауэра (обычная конфигурация):

#### Linux

!!! example ""
    **# iptables -L -n -v**                  - Состояние  
    Открыть брандмауэр iptables  
    **# iptables -P INPUT       ACCEPT**     - Открыть все  
    **# iptables -P FORWARD     ACCEPT**  
    **# iptables -P OUTPUT      ACCEPT**  
    **# iptables -Z**                        - Обнулить счетчики пакетов и байтов во всех цепочках  
    **# iptables -F**                        - Очистить все цепочки  
    **# iptables -X**                        - Удалить все цепочки  


#### FreeBSD

!!! example ""
    **# ipfw show**                          - Состояние  
    **# ipfw list 65535**                    - если ответ "65535 deny ip from any to any", то брандмауэр отключен  
    **# sysctl net.inet.ip.fw.enable=0**     - Отключить  
    **# sysctl net.inet.ip.fw.enable=1**     - Включить  


### 4.7 IP Forward для маршрутизации

#### Linux

Проверить и затем включить IP Forward:

!!! example ""
    **# cat /proc/sys/net/ipv4/ip_forward**          # Проверить IP Forward (0=выключено, 1=включено)  
    **# echo 1 > /proc/sys/net/ipv4/ip_forward**  

!!! note "или отредактировать `/etc/sysctl.conf`:"
    *net.ipv4.ip_forward = 1*

#### FreeBSD

Проверить и включить:

!!! example ""
    **# sysctl net.inet.ip.forwarding**        - Проверить IP Forward (0=выключено, 1=включено)  
    **# sysctl net.inet.ip.forwarding=1**  
    **# sysctl net.inet.ip.fastforwarding=1**	 - Для выделенного маршрутизатора или брандмауэра  

!!! note "Постоянное включение с помощью записи в `/etc/rc.conf`:"
    *gateway_enable="YES"*                 - Установить YES, если этот хост будет шлюзом.

#### Solaris

!!! example ""
    **# ndd -set /dev/ip ip_forwarding 1**   - Установить IP Forward (0=выключено, 1=включено)


### 4.8 NAT (Network Address Translation)

#### Linux

!!! example ""
    **# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE**	- Активация NAT  
    **# iptables -t nat -A PREROUTING -p tcp -d 78.31.70.238 --dport 20022 -j DNAT \\**  
    **--to 192.168.16.44:22**           - Перенаправление порта 20022 на внутренний IP-адрес и порт SSH  
    **# iptables -t nat -A PREROUTING -p tcp -d 78.31.70.238 --dport 993:995 -j DNAT \\**  
    **--to 192.168.16.254:993-995**     - Перенаправление диапазона портов 993-995  
    **# ip route flush cache**  
    **# iptables -L -t nat**            - Проверить состояние NAT  

Удалите пересылку портов с помощью `-D` вместо `-А`. Программа [netstat-nat](http://tweegy.nl/projects/netstat-nat) очень полезна для отслеживания соединений (она использует `/proc/net/ip_conntrack` или `/proc/net/nf_conntrack`).

!!! example ""
    **# netstat-nat -n**                - показать все соединения с IP-адресами

#### FreeBSD

!!! example ""
    **# natd -s -m -u -dynamic -f /etc/natd.conf -n fxp0**

!!! note "Или измените файл `/etc/rc.conf` следующим образом:"
    **firewall_enable="YES"**                             - Установите YES для включения функциональности брандмауэра  
    **firewall_type="open"**                              - Тип брандмауэра (см. `/etc/rc.firewall`)  
    **natd_enable="YES"**                                 - Включить natd (если firewall_enable == YES)  
    **natd_interface="tun0"**                             - Общедоступный интерфейс или IP-адрес для использования  
    **natd_flags="-s -m -u -dynamic -f /etc/natd.conf"**  

Перенаправление порта:
!!! example "cat /etc/natd.conf"
    same_ports yes  
    use_sockets yes  
    unregistered_only  

!!! example ""
    **# redirect_port tcp insideIP:2300-2399 3300-3399**  - диапазон портов  
    **# redirect_port udp 192.168.51.103:7777 7777**  

### 4.9 DNS

В Unix записи DNS являются действительными для всех интерфейсов и хранятся в `/etc/resolv.conf`. Домен, к которому принадлежит хост, также хранится в этом файле. Минимальная конфигурация выглядит следующим образом:

!!! note ""
    *nameserver 78.31.70.238*  
    *search sleepyowl.net intern.lab*  
    *domain sleepyowl.net*  

Проверьте системное доменное имя с помощью команды:

!!! example ""
    **# hostname -d**                        - То же самое, что и dnsdomainname

#### Windows

В Windows DNS настраивается для каждого интерфейса. Чтобы отобразить настроенные DNS-серверы и очистить кэш DNS, используйте:

!!! example ""
    **# ipconfig /?**                        - Вывести справку  
    **# ipconfig /all**                      - Показать всю информацию, включая DNS  

#### Очистка DNS-кэша

Очистите кэш DNS операционной системы; некоторые приложения используют свой собственный кэш (например, Firefox) и не будут затронуты.

!!! example ""
    **# systemctl restart nscd.service**     - Перезапустить nscd, если используется - Linux  
    **# /etc/init.d/nscd restart**           - Перезапустить nscd, если используется - Linux/BSD/Solaris  
    **# lookupd -flushcache**                - OS X Tiger  
    **# dscacheutil -flushcache**            - OS X Leopard и новее  
    **# ipconfig /flushdns**                 - Windows  

#### Перенаправление запросов

Используйте команду `dig` для тестирования настроек DNS. Например, для тестирования можно использовать публичный DNS-сервер `213.133.105.2 ns.second-ns.de`. Просмотрите, с какого сервера клиент получает ответ (упрощенный ответ).

!!! example ""
    **# dig sleepyowl.net**  
    *sleepyowl.net.          600     IN      A       78.31.70.238*  
    *;; SERVER: 192.168.51.254#53(192.168.51.254)*  

Ответил маршрутизатор `192.168.51.254`, и ответом является запись `A`. Любую запись можно запросить, выбрав DNS-сервер с помощью `@`:

!!! example ""
    **# dig MX google.com**  
    **# dig @127.0.0.1 NS sun.com**          - Для тестирования локального сервера  
    **# dig @204.97.212.10 NS MX heise.de**  - Запросить внешний сервер  
    **# dig AXFR @ns1.xname.org example.com**      - Получить полную зону (зоновой трансфер)  

Программа `host` также мощная.

!!! example ""
    **# host -t MX example.com**                   - Получить запись MX для электронной почты  
    **# host -t NS -T sun.com**              - Получить запись NS через TCP-соединение  
    **# host -a sleepyowl.net**              - Получить все данные  

#### Обратные запросы

Найти имя, соответствующее IP-адресу (`in-addr.arpa.`). Это можно сделать с помощью `dig`, `host` и `nslookup`:

!!! example ""
    **# dig -x 78.31.70.238**  
    **# host 78.31.70.238**  
    **# nslookup 78.31.70.238**  

#### /etc/hosts

!!! note "Отдельные хосты можно настроить в файле `/etc/hosts` вместо локального запуска `named` для разрешения запросов имени хоста. Формат простой, например:"
    *78.31.70.238   sleepyowl.net   sleepyowl*

!!! note "Приоритет между хостами и DNS-запросом, то есть порядок разрешения имен, можно настроить в `/etc/nsswitch.conf` И `/etc/host.conf`. Файл также существует в Windows, обычно он находится в:"
    C:\WINDOWS\SYSTEM32\DRIVERS\ETC

### 4.10 DHCP

#### Linux

Некоторые дистрибутивы (SuSE) используют `dhcpcd` в качестве клиента. Интерфейс по умолчанию — `eth0`.

!!! example ""
    **# dhcpcd -n eth0** - Инициировать обновление (не всегда работает)  
    **# dhcpcd -k eth0** - выпуск и завершение работы  

Договор аренды с полной информацией хранится в:

!!! info ""
    */var/lib/dhcpcd/dhcpcd-eth0.info*

#### Windows

Для обновления аренды DHCP можно воспользоваться командой `ipconfig`:

!!! example ""
    **# ipconfig /renew**          - обновить все адаптеры  
    **# ipconfig /renew LAN**      - обновить адаптер с именем "LAN"  
    **# ipconfig /release WLAN**   - освободить адаптер с именем "WLAN"  

Да, это хорошая идея переименовать свой адаптер простым именем!

### 4.11 Анализ трафика

[Bmon](http://people.suug.ch/~tgr/bmon/) - это небольшой монитор пропускной способности консоли, который может отображать поток на разных интерфейсах.

#### Перехватывайте с помощью tcpdump

!!! example ""
    **# tcpdump -nl -i bge0 not port ssh and src \\(192.168.16.121 or 192.168.16.54\\)**  
    **# tcpdump -n -i eth1 net 192.168.16.121**           - выберите только входящий/исходящий трафик для одного IP-адреса  
    **# tcpdump -n -i eth1 net 192.168.16.0/24**          - выберите трафик, входящий/исходящий для сети  
    **# tcpdump -l > dump && tail -f dump**               - Буферизованный вывод  
    **# tcpdump -i rl0 -w traffic.rl0**                   - Запись заголовков трафика в бинарный файл  
    **# tcpdump -i rl0 -s 0 -w traffic.rl0**              - Запись трафика и полезных данных в бинарный файл  
    **# tcpdump -r traffic.rl0**                          - Чтение из файла (также для программы Ethereal)  
    **# tcpdump port 80**                                 - Два классических команды  
    **# tcpdump host google.com**  
    **# tcpdump -i eth0 -X port \(110 or 143\)**          - Проверка безопасности протоколов POP или IMAP  
    **# tcpdump -n -i eth0 icmp**                         - Отлавливать только пинги  
    **# tcpdump -i eth0 -s 0 -A port 80 | grep GET**      - `-s 0` для полного пакета `-A` для ASCII

!!! info "Дополнительные важные параметры:"
    -A    &nbsp; &nbsp; Выводить каждый пакет в виде текста (без заголовка)  
    -X    &nbsp; &nbsp; Выводить пакеты в шестнадцатеричном и ASCII форматах  
    -l    &nbsp; &nbsp; Включить буферизацию вывода по строкам  
    -D    &nbsp; &nbsp; Вывести список всех доступных интерфейсов  

На Windows используйте windump с сайта www.winpcap.org. Используйте команду `windump -D`, чтобы вывести список интерфейсов.

#### Сканирование с помощью nmap

[Nmap](http://insecure.org/nmap/) - это сканер портов с определением операционной системы, который обычно устанавливается на большинстве дистрибутивов и также доступен для Windows. Если вы не сканируете свои серверы, хакеры делают это за вас...

!!! example ""
    **# nmap example.com**               - Сканировать все зарезервированные TCP-порты на хосте  
    **# nmap -sP 192.168.16.0/24** - Узнать, какие IP-адреса используются и каким хостом находятся в этой подсети  
    **# nmap -sS -sV -O example.com**    - Сканирование stealth SYN с определением версии и ОС  
    *PORT    &nbsp; &nbsp;   STATE &nbsp; &nbsp;  SERVICE  &nbsp; &nbsp; &nbsp; &nbsp; VERSION*  
    *22/tcp    &nbsp; &nbsp; open   &nbsp; &nbsp; &nbsp; &nbsp; ssh      &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; OpenSSH 3.8.1p1 FreeBSD-20060930 (protocol 2.0)*  
    *25/tcp    &nbsp; &nbsp; open   &nbsp; &nbsp; &nbsp; &nbsp; smtp     &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sendmail smtpd 8.13.6/8.13.6*  
    *80/tcp    &nbsp; &nbsp; open   &nbsp; &nbsp; &nbsp; &nbsp; http     &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Apache httpd 2.0.59 (FreeBSD) DAV/2 PHP/4.*  
    *[...]*  
    *Running: FreeBSD 5.X*  
    *Uptime 33.120 days (since Fri Aug 31 11:41:04 2007)*  

Другие нестандартные, но полезные инструменты - [hping](www.hping.org) - сборщик/анализатор пакетов IP и [fping](fping.sourceforge.net). `fping` может проверять несколько хостов по круговому принципу.

### 4.12 Управление трафиком (QoS)

Управление трафиком управляет очередью, контролирует скорость, планирует и другие параметры трафика в сети. Вот несколько простых практических примеров использования возможностей Linux и FreeBSD для более эффективного использования доступной пропускной способности.

#### Ограничение загрузки

DSL или кабельные модемы имеют длинную очередь для повышения пропускной способности загрузки. Однако заполнение очереди быстрым устройством (например, Ethernet) резко снизит интерактивность. Поэтому полезно ограничить скорость загрузки устройства в соответствии с физической емкостью модема, это должно значительно улучшить интерактивность. Установите примерно 90% от максимальной скорости модема (кабель).

##### Linux

Для модема с загрузкой на передачу данных 512 Кбит.

!!! example ""
    **# tc qdisc add dev eth0 root tbf rate 480kbit latency 50ms burst 1540**  
    **# tc -s qdisc ls dev eth0**                                                   - Состояние  
    **# tc qdisc del dev eth0 root**                                                - Удалить очередь  
    **# tc qdisc change dev eth0 root tbf rate 220kbit latency 50ms burst 1540**  

##### FreeBSD

FreeBSD использует `traffic shaper dummynet`, который настраивается с помощью `ipfw`. Каналы используются для установки ограничений на пропускную способность в единицах `[K|M]{bit/s|Byte/s}`, `0` означает неограниченную пропускную способность. Использование того же номера канала переконфигурирует его. Например, ограничить пропускную способность загрузки до 500 Кбит.

!!! example ""
    **# kldload dummynet**                                - загрузить модуль, если необходимо  
    **# ipfw pipe 1 config bw 500Kbit/s**                 - создать канал с ограниченной пропускной способностью  
    **# ipfw add pipe 1 ip from me to any**               - направить всю загрузку в канал  

#### Качество обслуживания

QoS (англ. quality of service «качество обслуживания») — технология предоставления различным классам трафика различных приоритетов в обслуживании, также этим термином в области компьютерных сетей называют вероятность того, что сеть связи соответствует заданному соглашению о трафике, или же, в ряде случаев, неформальное обозначение вероятности прохождения пакета между двумя точками сети.

##### Linux

Приоритетное упорядочение с помощью `tc` для оптимизации VoIP. См. полный пример на voip-info.org или www.howtoforge.com.
Предположим, что VoIP использует udp на портах 10000:11024 и устройстве eth0 (может быть также ppp0 и т. д.). Следующие команды определяют QoS для трех очередей и принудительно направляют трафик VoIP в очередь 1 с QoS `0x1e` (все биты установлены). Трафик по умолчанию направляется в очередь 3, а QoS Minimize-Delay направляется в очередь 2.

!!! example ""
    **# tc qdisc add dev eth0 root handle 1: prio priomap 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 0**  
    **# tc qdisc add dev eth0 parent 1:1 handle 10: sfq**  
    **# tc qdisc add dev eth0 parent 1:2 handle 20: sfq**  
    **# tc qdisc add dev eth0 parent 1:3 handle 30: sfq**  
    **# tc filter add dev eth0 protocol ip parent 1: prio 1 u32 \\**  
      **match ip dport 10000 0x3C00 flowid 1:1**          - использовать диапазон портов сервера  
      **match ip dst 123.23.0.1 flowid 1:1**              - или/и использовать IP-адрес сервера  

Статус и удаление с помощью

!!! example ""
    **# tc -s qdisc ls dev eth0**                         - статус очереди  
    **# tc qdisc del dev eth0 root**                      - удалить все QoS  

***Расчет диапазона портов и маски***

Фильтр `tc` определяет диапазон портов с помощью порта и маски, которые необходимо вычислить. Найдите окончание диапазона портов `2^N`, вычтите из него диапазон и преобразуйте в HEX. Это будет ваша маска. Пример для 10000 -&gt; 11024, диапазон равен 1024.

!!! example ""
    **# 2^13 (8192) &lt; 10000 &lt; 2^14 (16384)**              - окончание - 2^14 = 16384  
    **# echo "obase=16;(2^14)-1024" | bc**                      - маска - 0x3C00  

##### FreeBSD

Максимальная пропускная способность соединения составляет 500 Kбит/с, и мы определяем 3 очереди с приоритетом `100:10:1` для `VoIP:ssh:все` остальное.

!!! example ""
    **# ipfw pipe 1 config bw 500Kbit/s**  
    **# ipfw queue 1 config pipe 1 weight 100**  
    **# ipfw queue 2 config pipe 1 weight 10**  
    **# ipfw queue 3 config pipe 1 weight 1**  
    **# ipfw add 10 queue 1 proto udp dst-port 10000-11024**  
    **# ipfw add 11 queue 1 proto udp dst-ip 123.23.0.1**          - или/и использовать IP-адрес сервера  
    **# ipfw add 20 queue 2 dsp-port ssh**  
    **# ipfw add 30 queue 3 from me to any**                       - все остальное  

Статус и удаление с помощью

!!! example ""
    **# ipfw list**                - статус правил  
    **# ipfw pipe list**           - статус каналов  
    **# ipfw flush**               - удалить все правила, кроме стандартных  

### 4.13 Отладка NIS

Некоторые команды, которые должны работать на хорошо настроенном клиенте NIS:

!!! example ""
    **# ypwhich**                          - получить имя подключенного сервера NIS  
    **# domainname**                       - настроенное имя домена NIS  
    **# ypcat group**                      - должен отображать группу с сервера NIS  
    **# cd /var/yp &amp;&amp; make**       - Перестроить базу данных yp  
    **# rpcinfo -p servername**            - Отчет о службах RPC сервера  

Запущен ли ypbind?

!!! example ""
    **# ps auxww | grep ypbind**  
    */usr/sbin/ypbind -s -m -S servername1,servername2* &nbsp; &nbsp; - FreeBSD  
    */usr/sbin/ypbind* &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; - Linux  
    **# yppoll passwd.byname**  
    *Map passwd.byname has order number 1190635041. Mon Sep 24 13:57:21 2007*  
    *The master server is servername.domain.net.*  

#### Linux

!!! example ""
    **# cat /etc/yp.conf**  
    *ypserver servername*  
    *domain domain.net broadcast*  

### 4.14 Netcat

[Netcat](http://netcat.sourceforge.net) (nc) больше известен как "сетевой швейцарский нож", он может манипулировать, создавать или читать/записывать соединения TCP/IP. Вот несколько полезных примеров, их много больше в Интернете, например, [g-loaded.eu](http://www.g-loaded.eu/2006/11/06/netcat-a-couple-of-useful-examples) и [здесь](http://www.terminally-incoherent.com/blog/2007/08/07/few-useful-netcat-tricks). Возможно, вам потребуется использовать команду `netcat` вместо `nc`. Также см. аналогичную команду `socat`.

#### Передача файлов

Скопировать большую папку через неразобранное TCP-соединение. Передача очень быстрая (без накладных расходов протокола), и вам не нужно возиться с `NFS` или `SMB` или `FTP` и т.д., просто сделайте файл доступным на сервере и получите его с клиента. Здесь 192.168.1.1 - это IP-адрес сервера.

!!! example ""
    *server ->* **# tar -cf - -C VIDEO_TS . | nc -l -p 4444**         - Сервер предоставляет архивную папку на порту 4444  
    *client ->* **# nc 192.168.1.1 4444 | tar xpf - -C VIDEO_TS**     - Получает файл по порту 4444 и распаковывает его в папку VIDEO_TS  
    *server ->* **# cat largefile | nc -l 5678**                      - Сервер передает одиночный файл  
    *client ->* **# nc 192.168.1.1 5678 > largefile**                 - Получает одиночный файл  
    *server ->* **# dd if=/dev/da0 | nc -l 4444**                     - Сервер предоставляет образ раздела  
    *client ->* **# nc 192.168.1.1 4444 | dd of=/dev/da0**            - Копирует раздел для клонирования  
    *client ->* **# nc 192.168.1.1 4444 | dd of=da0.img**             - Копирует раздел в файл  

#### Другие возможности

Особенно здесь, вы должны знать, что делаете.

**Удаленная оболочка**

Опция `-e` есть только в версии для Windows? Или использовать `nc 1.10`.

!!! example ""
    **# nc -lp 4444 -e /bin/bash**    - Предоставляет удаленную оболочку  
    **# nc -lp 4444 -e cmd.exe**      - Удаленная оболочка для Windows  

**Аварийный веб-сервер**

Постоянно предоставляет одиночный файл на порту 80.

!!! example ""
    **# while true; do nc -l -p 80 < unixtoolbox.xhtml; done**

**Чат**

Алиса и Боб могут общаться по простому TCP-сокету. Текст передается по нажатию клавиши `Enter`.

!!! example ""
    *alice ->* **# nc -lp 4444**  
    *bob   ->* **# nc 192.168.1.1 4444**  

### 4.15 cURL

**cURL** — (распространяемая по лицензии MIT) кроссплатформенная служебная программа командной строки, позволяющая взаимодействовать с множеством различных серверов по множеству различных протоколов с синтаксисом URL. Название расшифровывается как "client for URL".

#### Простое использование

!!! example ""
    **curl https://www.example.com/**               - Получить главную страницу с веб-сервера  
    **curl http://www.weirdserver.com:8000/**       - Получите веб-страницу с сервера, используя порт 8000  
    **curl ftp://ftp.funet.fi**                     - Получите список каталогов FTP-сайта  
    **curl ftp://ftp.funet.fi/README**              - Получите файл README с FTP-сервера  
    **curl --ftp-ssl ftp://files.are.secure.com/secrets.txt**     - Получить файл с FTPS-сервера  
    **curl ftp://ftp.funet.fi/ http://www.weirdserver.com:8000/** - Получите два документа одновременно  
    **curl -u username sftp://example.com/etc/issue**             - Получите файл с SSH-сервера с помощью SFTP  
    **curl -u username: --key ~/.ssh/id_rsa scp://example.com/~/file.txt** - Получите файл с SSH-сервера, используя SCP, используя закрытый ключ (не защищенный паролем) для аутентификации  
    **curl -u username: --key ~/.ssh/id_rsa --pass private_key_password scp://example.com/~/file.txt** - Получите файл с SSH-сервера, используя SCP, используя закрытый ключ (защищенный паролем) для аутентификации  
    **curl -u "domain\username:passwd" smb://server.example.com/share/file.txt** - Получить файл с SMB-сервера  

#### Использование паролей

!!! example ""
    *Curl также поддерживает имя пользователя и пароль в URL-адресах HTTP, поэтому вы можете выбрать такой файл:*  
    **curl http://name:passwd@machine.domain/full/path/to/file**  
    *или укажите пользователя и пароль отдельно с помощью флага `-u`:*  
    **curl -u name:passwd http://machine.domain/full/path/to/file**  

!!! help ""
    HTTP предлагает множество различных методов аутентификации, и Curl поддерживает несколько из них: базовый, дайджест, NTLM и согласование (SPNEGO). Не указывая, какой метод использовать, по умолчанию используется значение `Basic`. Вы также можете попросить Curl выбрать наиболее безопасные из тех, которые сервер принимает для данного URL-адреса, используя `--anyauth`.

#### Прокси

Curl поддерживает прокси-серверы HTTP и SOCKS с дополнительной аутентификацией. Он не имеет специальной поддержки прокси-серверов FTP, поскольку для них не существует стандартов, но его все же можно заставить работать со многими из них. Вы также можете использовать прокси-серверы HTTP и SOCKS для передачи файлов на FTP-серверы и обратно.

!!! example ""
    **curl -x my-proxy:888 ftp://ftp.leachsite.com/README** - Получите ftp-файл, используя HTTP-прокси с именем my-proxy, который использует порт 888  
    **curl -u user:passwd -x my-proxy:888 http://www.get.this/** - Получите файл с HTTP-сервера, для которого требуется имя пользователя и пароль, используя тот же прокси-сервер  
    **curl -U user:passwd -x my-proxy:888 http://www.get.this/** - Некоторые прокси требуют специальной аутентификации. Укажите, используя `-U`  
    **curl --noproxy localhost,get.this -x my-proxy:888 http://www.get.this/** - Список хостов и доменов, разделенных запятыми, которые не используют прокси  

!!! hint "Подсказка"
    Если прокси-сервер указан `--proxy1.0` вместо `--proxy` или `-x`, то для любых попыток Curl будет использовать HTTP/1.0 вместо HTTP/1.1 CONNECT. Curl также поддерживает прокси-серверы SOCKS4 и SOCKS5 с `--socks4` расширением `--socks5`.

#### Диапазоны

!!! example ""
    **curl -r 0-99 http://www.get.this/** - Получите первые 100 байт документа  
    **curl -r -500 http://www.get.this/** - Получить последние 500 байт документа  

#### Загрузка

!!! example ""
    **curl -T - ftp://ftp.upload.com/myfile** - Загружает все данные на стандартный ввод на указанный сервер  
    **curl -T uploadfile -u user:passwd ftp://ftp.upload.com/myfile** - Загружает данные из указанного файла, войдите под пользователем и паролем  
    **curl -T localfile -a ftp://ftp.upload.com/remotefile** - Загружает локальный файл, чтобы добавить его к удаленному файлу  
    **curl -T file.txt -u "domain\username:passwd" smb://server.example.com/share/** - Загружает данные на шаровый ресурс по SMB  

#### Отладка

!!! example ""
    **curl -v ftp://ftp.upload.com/** - Используйте флаг `-v` чтобы получить подробную выборку  
    **curl --trace trace.txt www.haxx.se** - Чтобы получить еще больше подробностей и информации о том, что делает Curl, попробуйте использовать параметры `--trace` или `--trace-asciiс` заданным именем файла для входа  
    **curl --dump-header headers.txt curl.se** - Сохраните заголовки HTTP в отдельном файле (в примере headers.txt)  

#### Возобновление передачи файлов и временные условия

!!! example ""
    **curl -C - -o file http://www.server.com/** - Продолжить загрузку документа с веб-сервера  
    **curl -z local.html http://remote.server.com/remote.html** - Выполнить загрузку, которая будет выполняться только в том случае, если удаленный файл новее локальной копии  
    **curl -z "Jan 12 2012" http://remote.server.com/remote.html** - Curl загрузит файл только в том случае, если он был обновлен после 12 января 2012 г.  

#### Telnet

!!! example ""
    **curl telnet://remote.server.com:port** - Подключитесь к удаленному серверу telnet, используя командную строку  
    **curl -tTTYPE=vt100 telnet://remote.server.com** - Чтобы сообщить серверу, что мы используем терминал vt100, попробуйте что-то вроде  

### 4.16 HTTP Status Codes

#### Что такое коды статуса и почему они важны?

Когда клиент делает запрос на сервер, коды статуса позволяют узнать, был ли запрос успешным, неудавшимся или чем-то другим. Коды статуса поддерживаются Управление по присвоенным номерам в Интернете, или IANA, и включает в себя коды статуса от Интернет инженерной целевой группы (IETF) и Интернет-общества (ISOC). В соответствии с определением IANA организация, tВот пять классификаций http статус трескиes:

**1xx**: *Информационные ответы* – Запрос получен, продолжается процесс
**2xx**: *Успешные ответы* – Действие было успешно получено, понято, и принято
**3xx**: *Сообщения о перенаправлении* – Дальнейшие действия должны быть приняты для того, чтобы завершить запрос
**4xx**: *Ошибка клиента* – Запрос содержит плохой синтаксис или не может быть выполнен
**5xx**: *Ошибка сервера* – Сервер не выполнил явно действительный запрос

##### Информационные ответы

!!! info "Informational"
    Данная группа отвечает за передачу данных. Коды этого типа свидетельствуют о том, что запрос принят сервером и обрабатывается.



##### Успешные ответы

!!! check "Success"
    Коды группы сообщают, что запрос не только принят сервером, но и успешно обработан.



##### Сообщения о перенаправлении

!!! attention "Redirection"
    Данная группа кодов состояния сообщает о перенаправлении пользователя с его согласием или без него.



##### Ошибка клиента

!!! fail "Client Error"
    Коды состояний данной группы сообщают об ошибках клиента, при которых сервер не может вызвать запрашиваемый результат.



##### Ошибка сервера

!!! bug "Server Error"
    В эту группу входят коды ошибок со стороны сервера, когда по тем или иным причинам он не способен обработать запрос или выполнить требуемую операцию.


