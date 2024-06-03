## 22 Создание скриптов

!!! abstract ""
    [Основы](#221-основы) | [Пример сценария](#222-пример-сценария-bourne) | [Сценарии Python](#223-написание-сценариев-на-python) | [awk](#224-некоторые-команды-awk) | [sed](#225-некоторые-команды-sed) | [Регулярные выражения](#226-регулярные-выражения) | [Полезные команды](#227-некоторые-полезные-команды)

Оболочка Bourne (`/bin/sh`) присутствует во всех установках Unix, и скрипты, написанные на этом языке, являются переносимыми; `man 1 sh` хорошая справочная информация.

### 22.1 Основы

#### Переменные и аргументы

Присваивание с помощью `variable=value`, получение содержимого с помощью `$variable`

!!! example ""
    **MESSAGE="Привет, Мир"**                        - Присваивание строки  
    **PI=3.1415**                                    - Присваивание десятичного числа  
    **N=8**  
    **TWON=`expr \$N * 2`**                           - Арифметическое выражение (только целые числа)  
    **TWON=\$((\$N * 2))**                             - Другой синтаксис  
    **TWOPI=`echo "\$PI * 2" | bc -l`**               - Используйте bc для операций с плавающей точкой  
    **ZERO=`echo "c(\$PI/4)-sqrt(2)/2" | bc -l`**  

Аргументы командной строки:

!!! info ""
    **\$0, \$1, \$2, ...**                              - \$0 - сама команда  
    **\$#**                                           - Количество аргументов  
    **\$\***                                          - Все аргументы (также \$@)  

Специальные переменные:

!!! info ""
    **\$\$**                                           - Текущий идентификатор процесса  
    **\$?**                                           - Код возврата последней команды  

!!! example ""
    **<команда>**  
    **if [ \$? != 0 ]; then**  
    &nbsp; **echo "команда завершилась с ошибкой"**  
    **fi**  

!!! info ""
    Особого внимания здесь заслуживает конструкция **\${PWD##*/}**, которая берет полный путь до текущего каталога (переменная *\\$PWD*) и удаляет из него первую часть вплоть до последнего слеша, оставляя, таким образом, только имя самого каталога.

!!! example ""
    **mypath=`pwd`**  
    **mypath=\${mypath}/file.txt**  
    **echo \${mypath##*/}**                           - Показать только имя файла  
    **echo \${mypath%%.*}**                           - Полный путь без расширения  

!!! example ""
    **foo=/tmp/my.dir/filename.tar.gz**  
    **path = \${foo%/*}**                             - Полный путь без расширения  
    **var2=\${var:=string}**                          - Использовать `var`, если установлено, в противном случае использовать `string` присвоить `string` переменной `var`, а затем переменной `var2`.  

!!! example ""
    **size=\$(stat -c%s "\$file")**                    - получить размер файла в сценарии Bourne  
    **filesize=\${size:=-1}**  

#### Конструкции

!!! example "Показать содержимое файлов из вывода команды ls"
    **for file in `ls`**  
    **do**  
    &nbsp; **echo \$file**  
    **done**  

!!! example "Однострочная запись, разрешения имен для двух доменнов: example.com и google.com"
    **for i in {example.com,google.com}; do dig ANY \$i; done**

!!! example "Выполняет цикл 5 раз"
    **count=0**  
    **while [ \$count -lt 5 ]; do**  
    &nbsp; **echo \$count**  
    &nbsp; **sleep 1**  
    &nbsp; **count=\$((\$count + 1))**  
    **done**  

!!! example "Пример функции с поиском файлов по расширению"
    **myfunction() {**  
    &nbsp; **find . -type f -name "*.\$1" -print**       - \$1 - первый аргумент функции  
    **}**  
    **myfunction "txt"**  

!!! example "А это уже скрипт, кoторый запускает команду в ответ на изменение файлов в каталoге"
    **# while true; do inotifywait -r -e MODIFY <path> && <command> done**

#### Создание файла

!!! example "Многострочное перенапровление в файл"
    **MYHOME=/home/colin**  
    **cat > testhome.sh << _EOF**  
    *# Весь этот код помещается в файл testhome.sh*  
    **if [ -d "\$MYHOME" ] ; then**  
    &nbsp; **echo \$MYHOME существует**  
    **else**  
    &nbsp; **echo \$MYHOME не существует**  
    **fi**  
    **_EOF**  
    **sh testhome.sh**  

### 22.2 Пример сценария Bourne

В качестве небольшого примера, вот скрипт, используемый для создания PDF-буклета из XHTML-документа:

!!! example "Этот скрипт создает книгу в формате PDF для печати на двухстороннем принтере"
    ```bash
    #!/bin/sh
    if [ $# -ne 1 ]; then                        # Проверяем аргумент
      echo 1>&2 "Использование: $0 HtmlFile"
      exit 1                                     # Ненулевое значение при ошибке
    fi
    
    file=$1                                      # Присваиваем имя файла
    fname=${file%.*}                             # Получаем только имя файла
    fext=${file#*.}                              # Получаем расширение файла
    
    prince $file -o $fname.pdf                   # от www.princexml.com
    pdftops -paper A4 -noshrink $fname.pdf $fname.ps # создаем постскриптовый буклет
    cat $fname.ps |psbook|psnup -Pa4 -2 |pstops -b "2:0,1U(21cm,29.7cm)" > $fname.book.ps
    
    ps2pdf13 -sPAPERSIZE=a4 -sAutoRotatePages=None $fname.book.ps $fname.book.pdf
                                                 # используем #a4 и #None в Windows!
    exit 0                                       # успешное завершение
    ```

### 22.3 Написание сценариев на Python

Основные особенности языка программирования Python:

* Скриптовый язык. Код программ определяется в виде скриптов.

* Поддержка самых различных парадигм программирования, в том числе объектно-ориентированной и функциональной парадигм.

* Интерпретация программ. Для работы со скриптами необходим интерпретатор, который запускает и выполняет скрипт.

* Портативность и платформонезависимость. Не имеет значения, какая у нас операционная система - Windows, Mac OS, Linux, нам достаточно написать скрипт, который будет запускаться на всех этих ОС при наличии интерпретатора.

* Автоматическое управление памяти.

* Динамическая типизация.

Python применяется в различных сферах от администрирования до аналитики.

#### В примере ниже приведен код функции декорирования. Данная функция оборачивается вокруг другой функции расширяя ее возможности

!!! example "Пример кода"
    ``` python
    """ Пример декоратора (функция с замыканием)
    """
    var = f'Основная функция!'
    
    def decor(func):
        func_out = None
        def inner(*args,**kwargs):
            nonlocal func_out
            print(f'*' * 100 + f'\n')
            func_out = func(*args,**kwargs)
            print(f'\n' + f'*' * 100)
            return func_out
        return inner
    
    @decor
    def hellow(*args):
        for a in args:
            print(a)
    
    hellow(var)
    ```

??? quote "Результат"
    ``` console
    ****************************************************************************************************
    
    Основная функция!
    
    ****************************************************************************************************
    ```

#### Пример декоратора замеряющего время выполнения функции

!!! example "Пример кода"
    ``` python
    import time
    
    from datetime import datetime
    
    def task_time(func):
        """Add time task works
        
        Example:
          @task_time
          function_name(*args, **kwargs):
            pass
        """
        func_out = None
        def time_stamp(*args, **kwargs):
            nonlocal func_out
            stime = datetime.now()
            print(f"Function: {func.__name__}")
            func_out = func(*args, **kwargs)
            etime = f"Task time: {str(datetime.now() - stime)[:10]}"
            eline = round((10 - len(etime) - 2) / 2)
            print(f"{etime}")
            return func_out
        time_stamp.__name__ = func.__name__
        time_stamp.__doc__ = func.__doc__
        return time_stamp
    
    @task_time
    def create_array(size):
        """Create array
        """
        time.sleep(1.15)
        array = [[ x for x in range(0,size)] for y in range(size)]
        return array
    
    size = int(input('Enter size: '))
    
    a = create_array(size)
    
    print(f'\nPrint resault:')
    for i in a:
        print(*i)
    ```

??? quote "Результат"
    ``` console
    Enter size:  5
    Function: create_array
    Task time: 0:00:01.15  
    
    Print resault:
    0 1 2 3 4
    0 1 2 3 4
    0 1 2 3 4
    0 1 2 3 4
    0 1 2 3 4
    ```

#### Меняем переменные местами

!!! example "Пример кода"
    ``` python
    a, b = 1, 2
    print(f'Before: a = {a}, b = {b}')
    a, b = b, a
    print(f'After: a = {a}, b = {b}')
    ```

??? quote "Результат"
    ``` console
    Before: a = 1, b = 2
    After: a = 2, b = 1
    ```

#### Создание числовой последовательности с добавленными нулями

!!! example "Пример кода"
    ``` python
    for i in range(1,15+1):
        print(f'{i:05d}')
    ```

??? quote "Результат"
    ``` console
    00001
    00002
    00003
    00004
    00005
    00006
    00007
    00008
    00009
    00010
    00011
    00012
    00013
    00014
    00015
    ```

#### Во фрагменте кода ниже приведен алгоритм выбора из веденных данных

!!! example "Пример кода"
    ``` python
    """ Цыкл с выбором
    """
    while True:
        choice = str(input(f'Хочешь?\n>').lower())
        if choice in ('да', 'о да'): 
            print("Хочу")
            break
        elif choice in ('нет', 'ну нет'):
            print("Не хочу")
            pass
        else:
            print('Еще раз!')
    ```

??? quote "Результат"
    ``` console
    Хочешь?
    >нет
    Не хочу
    Хочешь?
    >точно
    Еще раз!
    Хочешь?
    >да
    Хочу
    ```

#### Пример наглядно показывает отличие списка от множества. В множестве на основе списка отсутствуют дубликаты

!!! example "Пример кода"
    ``` python
    """ Счетчик и множество
    """
    from collections import Counter
    
    my_list = ['foo', 'bar', 'etc', 'etc']
    for i in my_list:
        print(i)
    
    # Подсчет
    print(Counter(my_list))
    # Множиство удаляет дубликат
    print({i for i in my_list})
    ```

??? quote "Результат"
    ``` console
    foo
    bar
    etc
    etc
    Counter({'etc': 2, 'foo': 1, 'bar': 1})
    {'bar', 'foo', 'etc'}
    ```

#### В примере демонстрируется разбиение строки и создание списка с использованием нескольких видов разделителя

!!! example "Пример кода"
    ``` python
    """ Мульти разделитель
    """
    import re
    
    my_list1 = str('id,id -h, who;who --help; ls')
    my_list2 = str('1.1.1.1,1.1.1.2, 2.2.2.2;2.2.2.3; 3.3.3.3')
    
    q = list(map(str, re.split(r'[,;]+ ?',input('Please enter FQDN host for register: '))))
    q1 = list(map(str, re.split(r'[,;]+ ?',my_list1)))
    q2 = list(map(str, re.split(r'[,;]+ ?',my_list2)))
    
    print(q1,q2)
    
    for item in q1:
        print(f'> {item}')
    
    print('')
    
    for item in q2:
        print(f'ip: {item}')
    ```

??? quote "Результат"
    ``` console
    ['id', 'id -h', 'who', 'who --help', 'ls'] ['1.1.1.1', '1.1.1.2', '2.2.2.2', '2.2.2.3', '3.3.3.3']
    > id
    > id -h
    > who
    > who --help
    > ls

    ip: 1.1.1.1
    ip: 1.1.1.2
    ip: 2.2.2.2
    ip: 2.2.2.3
    ip: 3.3.3.3
    ```

#### Пример скрипта работы с сетью

Проверка формата соответствия форматам записи: IP адресов, FQDN и портов TCP.

!!! example "Пример кода"
    ``` python
    import csv, getopt, logging, os, re, socket
    
    from concurrent.futures import as_completed, ThreadPoolExecutor
    from datetime import datetime
    from icmplib import ping, multiping
    from shlex import quote
    from tabulate import tabulate
    from tqdm.notebook import trange, tqdm
    
    log_file = 'check_hosts.log'
    
    if os.path.exists(log_file):
        fmode = 'a'
    else:
        fmode = 'w'
        
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode=fmode, datefmt='%d-%b-%y %H:%M:%S', format='%(asctime)s - Level severity: [%(levelname)s] USER: %(name)s, PID: %(process)d - FUNCTON:(%(filename)s).%(funcName)s(%(lineno)d), Thread ID: %(thread)d, MSG: %(message)s')
    
    def task_time(func):
        """ Decorator add task running time
    
        Args:
            func (function): _description_
    
        Returns:
            string: The time it took for the task to complete
        """
        func_out = None
        def time_stamp(*args, **kwargs):
            nonlocal func_out
            stime = datetime.now()
            print(f"---> Function: {func.__name__} <---")
            func_out = func(*args, **kwargs)
            etime = f"Task time: {str(datetime.now() - stime)[:10]}"
            print(f"\n---> {etime} <---")
            return func_out
        time_stamp.__name__ = func.__name__
        time_stamp.__doc__ = func.__doc__
        return time_stamp
    
    def check_fqdn(host):
        """ Checks the format of the entry for compliance with the FQDN spelling rules
    
        Args:
            host (string): Hostname of the host being checked
    
        Returns:
            boolean: The time it took for the task to complete
        """
        try:
            fqdn = re.search(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', host)
            if fqdn is None:
                return False
            else:
                return True
        except (Exception, getopt.GetoptError) as err:
            logging.exception("Exception occurred")
    
    def check_ip_addr(host):
        """ Checks the format of the entry for compliance with the IP address spelling rules
    
        Args:
            host (string): IP address of the host being checked
    
        Returns:
            boolean: The time it took for the task to complete
        """
        try:
            ip_addr = re.search(r'(?=^.{7,16}$)(^(?:\d{1,3}\.){3}\d{1,3}$)', host)
            if ip_addr is None:
                return False
            else:
                return True
        except (Exception, getopt.GetoptError) as err:
            logging.exception("Exception occurred")
    
    def check_dns(host):
        """ Checks for a record in the DNS
    
        Args:
            host (string): Hostname of the host being checked
    
        Returns:
            boolean: True if the entry exists
        """
        try:
            dns_data = socket.gethostbyname(host)
            if dns_data is not None:
                return True, dns_data
        except socket.gaierror:
            logging.exception("Exception occurred")
    
    def check_ping(host):
        """ Checks host availability with icmp request
    
        Args:
            host (string): Hostname or IP address of the host being checked
    
        Returns:
            boolean: True if the entry exists
        """
        try:
            ping_status = ping(host, count=1, timeout=2, id=None, source=None, family=None, privileged=True)
            return ping_status.is_alive
        except (Exception, getopt.GetoptError) as err:
            logging.exception("Exception occurred")
    
    def check_port(host, port):
        """ Checks if a port is open
    
        Args:
            host (string): Hostname or IP address of the host being checked
            port (string): Port number to check
    
        Returns:
            boolean: True if the port is open
        """
        port_match = re.search(r'(^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$)', port)
        if port_match is None:
            return False, None
        else:
            socket.setdefaulttimeout(3.0)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error:
                logging.exception("Exception occurred")
            try:
                result = s.connect_ex((host, int(port)))
                s.close()
                if result is not None and result == 0:
                    return True, result
                else:
                    return False, result
            except (Exception, getopt.GetoptError) as err:
                logging.exception("Exception occurred")
    
    def run_check(host, ports, list_hosts, position):
        """ Run check
    
        Args:
            host (string): Host for check
            ports (list): Port for check
            list_hosts (list): List results
    
        Returns:
            list: List results
        """
        count_host = 0
        count_port = 0
        list_ports = list()
        status_ping = check_ping(host['Host'])
        if status_ping is True:
            count_host += 1
        pbar = tqdm(set(ports), dynamic_ncols=False, position=position, leave=None, disable=False)
        for port in pbar:
            pbar.set_description(f"Host {host['Host']}, Port {port}")
            status_port = check_port(host['Host'], port)
            if status_port[0] is True:
                list_ports.append(port)
                count_port += 1
        if count_host != 0 and count_port != 0:
            list_hosts.append({'Host':host['Host'],'Format':True,'DNS':host['DNS'],'Ping':True,'Ports':",".join(sorted(list_ports, key=len))})
        elif count_host != 0 and count_port == 0:
            list_hosts.append({'Host':host['Host'],'Format':True,'DNS':host['DNS'],'Ping':True,'Ports':None})
        elif count_host == 0 and count_port != 0:
            list_hosts.append({'Host':host['Host'],'Format':True,'DNS':host['DNS'],'Ping':False,'Ports':",".join(sorted(list_ports, key=len))})
        else:
            print(f'The host could not be verified or is not available')
        
        return list_hosts
    
    @task_time
    def show_ckeck(list_hosts):
        """ Generates a summary table with results
    
        Args:
            list_hosts (list): List of dictionaries with hosts state
        """
        print(f'\nFormat table Markdown\n')
        print(tabulate(list_hosts, headers='keys', tablefmt='pipe'))
    
    def write_csv(file, data):
        """ Save results to CSV file.
    
        Args:
            file (string): CSV file
            data (list): Check result
        """
        with open(file, 'w', newline= '') as csvfile:
            header_key = ['Host', 'Format', 'DNS', 'Ping', 'Ports']
            writer = csv.DictWriter(csvfile, fieldnames=header_key)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
    
    def main():
        try:
            hosts = list(map(str, re.split(r'[,;]+ ?',input('Please enter FQDN hosts or IP address: '))))
            ports = list(map(str, re.split(r'[,;]+ ?',input('Please enter ports numbers: '))))
            csv_file = 'check_hosts.csv'
            current_hosts = list()
            invalid_hosts = list()
            for host in set(hosts):
                ip = check_ip_addr(host)
                if ip is True:
                    current_hosts.append({'Host':host,'Format':True,'DNS':'Skip'})
                elif ip is False:
                    fqdn = check_fqdn(host)
                    if fqdn is True:
                        dns = check_dns(host)
                        if dns[0] is True:
                            current_hosts.append({'Host':host,'Format':True,'DNS':dns[1]})
                        else:
                            invalid_hosts.append({'Host':host,'Format':True,'DNS':False})
                    else:
                        invalid_hosts.append({'Host':host,'Format':False,'DNS':False})
                else:
                    invalid_hosts.append({'Host':host,'Format':True,'DNS':False})
            
            list_hosts = list()
            with ThreadPoolExecutor(max_workers = None) as executor:
                futures = [executor.submit(run_check, host, ports, list_hosts, len(current_hosts)) for host in current_hosts]        
                for f in tqdm(as_completed(futures), total=len(current_hosts), position=0, dynamic_ncols=True, unit='run_check', unit_scale=True, disable=False, desc="Check host(s)"):
                    pass
            
            show_ckeck(list_hosts)
            print(list_hosts)
            write_csv(csv_file, list_hosts)
        except (Exception, getopt.GetoptError) as err:
            logging.exception("Exception occurred")
    
    if __name__ == "__main__":
        main()
    ```

??? quote "Результат"
    ``` console
    Please enter FQDN hosts or IP address:  8.8.8.8, example.com
    Please enter ports numbers:  53, 80, 443, 65556
    Check host(s): ############################################################# 100%
    2.00/2.00 [00:02<00:00, 2.10s/run_check]
    ---> Function: show_ckeck <---
    
    Format table Markdown
    
    | Host                        | Format   | DNS           | Ping   |   Ports |
    |:----------------------------|:---------|:--------------|:-------|--------:|
    | 8.8.8.8                     | True     | Skip          | True   |      53 |
    | example.com                 | True     | 93.184.216.34 | False  |      80 |
    
    ---> Task time: 0:00:00.00 <---
    [{'Host': '8.8.8.8', 'Format': True, 'DNS': 'Skip', 'Ping': True, 'Ports': '53'}, {'Host': 'example.com', 'Format': True, 'DNS': '93.184.216.34', 'Ping': False, 'Ports': '80'}]
    ```

#### Password generator

Генератор паролей, и linux хешей для утилиты `useradd`.

!!! example "Пример кода"
    ``` python
    import crypt, csv, logging, os, random, string
    from datetime import datetime
    from shlex import quote
    from tabulate import tabulate
    
    # Global variables
    lower,upper,num,symbols = string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation
    
    def password_gen(сomplexity,length,pass_num):
        """ Generat passwords.
    
        Args:
            сomplexity (list): Password complexity
            length (integer): Password length
            pass_num (integer): Number of generated passwords
        """
        password_list = list()
        for n in range(pass_num):
            temp = random.sample(сomplexity,length)
            salt = crypt.mksalt(method=crypt.METHOD_SHA512)
            PLAIN = "".join(temp)
            SHA512 = crypt.crypt(PLAIN, salt=salt)
            password_list.append({'Password':PLAIN,'Hash':SHA512})
        return password_list
    
    def show_table(password_list):
        """ Print passwords tables.
    
        Args:
            password_list (list): Passwords and hash
        """
        print(f'\nFormat table Markdown\n')
        print(tabulate(password_list, headers='keys', tablefmt='pipe'))
    
    def write_csv(file, data):
        """ Save results to CSV file.
    
        Args:
            file (string): CSV file
            data (list): Check result
        """
        with open(file, 'w', newline= '') as csvfile:
            header_key = ['Password', 'Hash']
            writer = csv.DictWriter(csvfile, fieldnames=header_key)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
    
    def main():
        try:
            сomplexity = lower
            length = 16
            pass_num = 5
            
            csv_file = 'passwords.csv'
            log_file = 'passwords.log'
            
            if os.path.exists(log_file):
                fmode = 'a'
            else:
                fmode = 'w'
            
            logging.basicConfig(level=logging.INFO, filename=log_file, filemode=fmode, datefmt='%d-%b-%y %H:%M:%S', format='%(asctime)s - Level severity: [%(levelname)s] USER: %(name)s, PID: %(process)d - FUNCTON:(%(filename)s).%(funcName)s(%(lineno)d), Thread ID: %(thread)d, MSG: %(message)s')
            
            print(f"Choose what to add to complicate the password...\n\n1. Uppercase\n2. Digits\n3. Special characters\n4. All\nC. Confirm\n")
            
            while (choice := quote(input("Pick a number: ").lower())) !='c':
                if(int(choice) == 1):
                    сomplexity += upper
                elif(int(choice) == 2):
                    сomplexity += num
                elif(int(choice) == 3):
                    сomplexity += symbols
                elif(int(choice) == 4):
                    сomplexity += upper + num + symbols
                    break
                else:
                    print("Please pick a valid option!")
            
            while (choice := quote(input(f'\nBy default password length 16 characters. Do you want change [Y/N]: ').lower())) !=str():
                if choice in ('yes', 'y'):
                    length = int(quote(input(f'\nEnter new password length: ')))
                    break
                elif choice in ('no', 'n'):
                    break
                else:
                    print("Please use y/n or yes/no.\n")
            
            while (choice := quote(input(f'\nBy default Number of passwords 5. Do you want change [Y/N]: ').lower())) !=str():
                if choice in ('yes', 'y'):
                    pass_num = int(quote(input(f'\nEnter new number of passwords: ')))
                    break
                elif choice in ('no', 'n'):
                    break
                else:
                    print("Please use y/n or yes/no.\n")
        
            passwords = password_gen(сomplexity,length,pass_num)
            show_table(passwords)
            write_csv(csv_file, passwords)
        except (Exception, getopt.GetoptError) as err:
            logging.exception("Exception occurred")
    
    if __name__ == "__main__":
        main()
    ```

??? quote "Результат"
    ``` console
    Choose what to add to complicate the password...
    
    1. Uppercase
    2. Digits
    3. Special characters
    4. All
    C. Confirm
    
    Pick a number:  1
    Pick a number:  2
    Pick a number:  c
    
    By default password length 16 characters. Do you want change [Y/N]:  
    
    By default Number of passwords 5. Do you want change [Y/N]:  y
    
    Enter new number of passwords:  10
    
    Format table Markdown
    
    | Password         | Hash                                                                                                       |
    |:-----------------|:-----------------------------------------------------------------------------------------------------------|
    | 2Xwc7P0qsUtLCSDl | $6$zScSpHj4S3pOOFu/$aCuzPI5ejvCXm1y.N1ip5bjBraWBgzjLrBq.79h21PfOsJaW3z79ApiFtc3gxi1KmXtckddIOiI2JhCMId5LI1 |
    | 1snlC4O8fXxmr05E | $6$ZdQ46shwArv6l..q$DQJJ53XQCFU7jxpSaTYp5otxpMirJFzo8vsADUFCDkSVhSomkP1stuzISM9WQusio.atxIjSirnjvea17Y0i0/ |
    | TUBfIul4xC5JYmy8 | $6$uZ0oVfGMmO1xdy9A$KedeXnSEbE0KoGszQ5igp0g8S/fcuzwm4oJMQDjB/5Q2Tly/nIqQEw4LfzI33FtMumDS97z9Ok.hPHX4g4GWM0 |
    | hGQigpkRV57SWw1s | $6$qs3UVBXBeuw5qz3g$uSY1RrZJdb8x0UX0fPlh7foYfU6e1alXWopj1Jf9bvdLChQwe7L/zCzR45yGvM0/vNnThbcf9xCbZMbEiDqE.1 |
    | vZrVWInzS0NwKdsT | $6$L7E4FIArN.MRitwD$49NqB8aJup4KXe/aQgdr/.Ra8o/JtN.uoKKoflSCUuapZp/BQjpUEYMbOKOsgo/S.wsxScdL957zi285K6oRH1 |
    | iEPR4WZCTnMrOJDq | $6$lwxEYIuK4jX1K1pr$ywjqNUVF4di/MybunQzndVqryGtfID3c6Hgg6yyWLpSjycejG/cf.ZFLw19JYun.il9CI4VdrrCAxufqFuJyl. |
    | FCKPuh9rQoIjBvLf | $6$2IzLGJuP.8hPc0QQ$Tw/5K80PeuoLOUkKKsuY7ifjpwAykqyPJDoX8c2rqsAuxsgznV2kT/tI96N.V5F4glGuVPehlB5gZR/fH4oN1. |
    | S2nAs9jXcYezNV7K | $6$F6KuEHVlCRWM/EPw$m/I7jnH.m1mgkEV10iQNSbP1OZCuocv8pyGHYjeyF/Q.T9QHOXMNub.yQJ/SlSERpatwgRwXPBXIFfke6j4p50 |
    | zBUiDlqJ9YWV2KLO | $6$XfloR.0cIJ3n4Ga1$8olQ.D83VQwjrjvoZGSRJ8XBDZVgHSuhP/byKUtYHT..3y/l96gmkqg/swMUnTalmLv.O2ZyVJpw.G59aqWqQ. |
    | dIHS2A5D4mEz6uVn | $6$CwgzqOpL0pi6tuc5$sm.VUXpckzbhPYfOSG0t.oCz3BUJAQPyK0HIKNOfV5SdzK.jtQ0m4R1B/cmhQgjI3HFu2VZ93p7awQmVTy91T1 |
    ```

#### QR-code

##### QR-code generator

!!! example "Пример кода"
    ``` python
    import io
    import qrcode
    
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    
    f = io.StringIO()
    
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data("https://docs-python.ru/packages/generator-qr-kodov")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white", image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img.save(f"qr-code.png", format=None)
    
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
    
    qr.clear()
    ```

??? quote "Результат"
    ``` console
                                         
                                         
        █▀▀▀▀▀█ ▀▄▄▄▀▄█ █▀█▀  █▀▀▀▀▀█    
        █ ███ █ ███▀▀█▄▄ ▄▀▀█ █ ███ █    
        █ ▀▀▀ █ ▀ ▄ █▄▀▀█▀▀█  █ ▀▀▀ █    
        ▀▀▀▀▀▀▀ ▀ █ █ ▀▄█▄▀▄█ ▀▀▀▀▀▀▀    
        ▀███▄▄▀▄█ ██  █▀█▀████▄ █▀▀ █    
        █▀█▀█ ▀█▄██▀▄▄  ▀▀▄ ███ ▀ ▀▀▄    
        ▀  ▄▀▄▀  █▀ ████▄█ █▄▄▄▀ ▀█▄▄    
        ▀▀▄██▀▀███ ▄▀ █ ▄▀ █▄▄▀▀█ ▀█▀    
          ▀▄▀ ▀▄ ▄▀▄▄█▄▄ ▄▀▀██ █▀█▄█     
        ▀ █▄  ▀██▀█  ▀▄████▄▀█▀▀▄ █      
         ▀ ▀▀▀▀▀█▄▀█ ▄ ▀▀▀█ █▀▀▀███▄▄    
        █▀▀▀▀▀█  ▀█▀█▄▄▄█▀▄▀█ ▀ ██ ▀     
        █ ███ █ ▄ █▀▀▀▀███  ██▀██▄▀█▄    
        █ ▀▀▀ █ ██▀▄▄▀▄▄▄▀▀▀█▀ ▀▄▄▀▄▀    
        ▀▀▀▀▀▀▀ ▀▀▀▀▀▀    ▀▀▀      ▀     
                                         
                                         
    ```

##### Show QR-code

!!! example "Пример кода"
    ``` python
    import cv2
    from matplotlib import pyplot as plt
    
    img = cv2.imread(f"qr-code.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    
    detect = cv2.QRCodeDetector()
    value = detect.detectAndDecode(img)
    
    print(value[0])
    ```

![qrcode](images/qr-code.png){.border}

??? quote "Результат"
    ``` console
    https://docs-python.ru/packages/generator-qr-kodov
    ```

#### Установка Jupyter-Lab на сервер c CentOS

Для установки выполнить следующие команды

##### Создать виртуальное окружение

!!! example ""
    ``` console
    python -m venv data-science
    ```

###### Активировать виртуальное окружение

!!! example ""
    ``` console
    source data-science/bin/activate
    ```

##### Установить приложение

!!! example ""
    ``` console
    python -m pip install --force-reinstall --upgrade pip
    python -m pip install --use-pep517 --force-reinstall -U \
    wheel jupyterlab notebook jupyter-git ipywidgets
    ```

##### Задать пароль на доступ

!!! example ""
    ``` console
    jupyter-lab password
    ```

##### Создать директорию для проектов

!!! example ""
    ``` console
    mkdir -p /var/jupyter-lab
    ```

##### Создать сервис для запуска приложения

Заменить переменные на свои. Переменные указаны в формате `{значение}`

!!! example ""
    ``` console
    cat <<- 'EOF' > /etc/systemd/system/jupyter-lab.service
    [Unit]
    Description=Jupyter WEB server
    Documentation=https://docs.jupyter.org/en/latest/
    After=network.target
    [Service]
    Type=simple
    User={Имя пользователя в домашней директории которого создано виртуальное окружение}
    Group={Имя группы пользователя в домашней директории которого создано виртуальное окружение}
    PIDFile=/var/run/jupyter-lab/jupyter-lab.pid
    WorkingDirectory=/root/data-science/
    Environment="VIRTUAL_ENV=/root/data-science/"
    Environment="PATH=$VIRTUAL_ENV/bin:$PATH"
    ExecStart=bash -c 'bin/jupyter-lab --ip {IP адрес сервера} --port 8888 --no-browser --allow-root --autoreload --notebook-dir=/var/jupyter-lab'
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s KILL $MAINPID
    TimeoutSec=0
    RestartSec=2
    Restart=always
    StartLimitBurst=3
    StartLimitInterval=60s
    [Install]
    WantedBy=multi-user.target
    EOF
    ```

Запустить и активировать сервис

!!! example ""
    ``` console
    systemctl start --now jupyter-lab.service
    ```

### 22.4 PowerShell

Оболочка PowerShell имеет следующие возможности.

* Удобная история командной строки

* Широкие возможности, такие как завершение табуляции и предсказание команд

* Псевдонимы команд и параметров

* Система изменения команд

* Встроенная справочная система, подобная Unix man pages

#### Шпаргалка PowerShell по командам

##### Командлеты (Cmdlets)

Это внутренние команды PowerShell. Эти команды возвращают один или несколько объектов в конвейер.


| Команда                                     | Описание                                                                                                                                     |
| :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| Get-Help                                    | Эта команда позволяет получить поддержку с помощью PowerShell.                                                                               |
| Get-PSdrive                                 | Эта команда предлагает вам список доступных PSDrives, таких как c, env, hklm, hkcu, alias и т.д.                                             |
| Get-ChildItem                               | В любом реестре дочерние ключи — это подключи текущего ключа. Чтобы получить необходимые сведения, можно воспользоваться следующей командой. |
| Get-ChildItem -recurse                      | Выполните эту команду, чтобы рекурсивно перечислить все дочерние элементы текущего PSdrive, папки или ключа реестра.                         |
| Get-ChildItem -rec -force                   | Используйте эту команду для включения скрытых папок (каталогов).                                                                             |
| (Get-ChildItem).name or Get-ChildItem -name | Выполните любую из этих команд, чтобы получить список имен файлов и каталогов в текущей папке.                                               |
| (Get-ChildItem).count                       | Используйте эту команду, чтобы получить количество записей в коллекции объектов, возвращенных командой Get-Children.                         |

##### PSdrives

Это коллекция объектов, сгруппированных вместе, чтобы к ним можно было получить доступ как к диску файловой системы. PSprovider выполняет эту группировку.

По умолчанию сеанс PS может обращаться к нескольким PSdrives, включая `c:, env:, alias: и HKLM:`, где `c:` означает обычный диск c Windows; `env:` — это пространство переменных среды Windows; `alias:` — это коллекция псевдонимов команд; а `HKLM` — это ветка в реестре.

##### Конвейеры

Cmdlets использует конвейеры для передачи объектов, но не потоков символов, как Unix. Символ конвейера — | (ASCII 124), за которым следует команда, обрабатывающая вывод, проходящий через конвейер.

| Команда                                                        | Описание                                                                                                          |
| :------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| (Get-Item /Users/praashibansal/Desktop).lastwritetime.year     | Легко устанавливает значение свойства ‘lastwritetime.year’ на текущую дату и время, не влияя на содержимое файла. |
| (Get-ChildItem data.txt.rtf -name).name # -> null              | Предоставляет пустой результат.                                                                                   |
| "data.txt.rtf" \| Rename-Item -NewName "data_new.txt.rtf"      | Изменяет старые имена файлов и расширения файлов на новые.                                                        |
| Get-ChildItem data.txt \| Rename-Item -new {$_.name}           | Тривиальная команда переименования, вызывающая автоматическую переменную.                                         |
| Get-ChildItem data.txt.rtf -name \| Rename-Item -new {$_.name} | Если у передаваемого объекта $_ нет свойства (name), вы получите ошибку, так как параметр $_.name является null.  |
| Get-ChildItem \| Select-Object basename \| Sort-Object *       | Отображает список имен всех файлов, присутствующих в текущей папке, отсортированных в алфавитном порядке.         |
| Move-Item *.txt subdirectory                                   | Перемещает все файлы в подкаталог папки.                                                                          |
| Get-ChildItem *.txt \| Move-Item ..\                           | Выдает сообщение об ошибке, что Move-Item не имеет входа.                                                         |

##### Alias (Алиас)

Cmdlets поддерживают несколько псевдонимов.

| Команда                                                                                  | Описание                                                                           |
| :--------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| Add-Content                                                                              | Добавляет значение к файлу                                                         |
| Get-Content                                                                              | Поиск содержимого файла в массиве                                                  |
| Set-Location                                                                             | Изменение папки, ключа или диска PS                                                |
| Clear-Host                                                                               | Очищает консоль                                                                    |
| Remove-Item                                                                              | Удаление файлов                                                                    |
| Get-ChildItem -Path .\|                                                                  | Списки папок, ключей или дочерних элементов PSDrive                                |
| Write-Output                                                                             | Отправляет массив в консоль, конвейер или перенаправляет его в файл                |
| Foreach-Object                                                                           | Обход каждого объекта в конвейере                                                  |
| Format-Table                                                                             | Форматирует таблицу с выбранными свойствами для каждого объекта в каждом столбце   |
| Format-List                                                                              | Форматирует свойства процесса по имени                                             |
| Get-Alias                                                                                | Обеспечивает псевдоним командлета                                                  |
| Get-Command                                                                              | Предоставляет вам команды только из текущей сессии                                 |
| Get-Member                                                                               | Извлечение всех членов объекта                                                     |
| Get-ItemProperty .\data.txt \| Format-List                                               | Предоставляет свойства указанного элемента                                         |
| Get-ItemPropertyValue -Path '.\data.txt' -Name LastWriteTime                             | Получает текущее значение для указанного свойства при использовании параметра name |
| Get-Variable m*                                                                          | Находит имена переменных сеансов                                                   |
| New-Item -Path .\ -Name "testfile1.txt" -ItemType "file" -Value "This is a text string." | Создает новый файл, каталог, символическую ссылку, ключ реестра или запись реестра |
| Get-Process                                                                              | Выдает полный список всех запущенных процессов                                     |
| Get-Location                                                                             | Предоставляет местоположение текущего каталога или ключа реестра                   |
| Rename-Item -Path “old_name” -NewName “new_name”                                         | Переименовывает старое имя элемента в новое имя                                    |
| Remove-Item .\testfile1.txt                                                              | Удаляет указанный каталог, файлы или ключи реестра                                 |
| Remove-Variable                                                                          | Удаляет указанную переменную                                                       |
| Start-Sleep                                                                              | Приостанавливает деятельность на определенный период времени                       |

##### Операторы

###### Арифметические операторы

| Оператор | Описание                                                                 | Пример          |
| :------- | :----------------------------------------------------------------------- | :-------------- |
| +        | Складывает целые числа                                                   | 6 + 2           |
| +        | Объединяе строки                                                         | «file» + «name» |
| -        | Вычитание одного значения из другого                                     | 6 - 2           |
| -        | Вычисляет противоположное число                                          | - -6            |
| *        | Умножение чисел или копирование строк и массивов заданное количество раз | 6 * 2           |
| /        | Делит два значения                                                       | 6 / 2           |
| %        | Modulus — возвращает остаток от операции деления                         | 7 % 2           |
| -band    | Побитовое И                                                              | 5 -band 3       |
| -bnot    | Побитовое НЕ                                                             | -bnot 5         |
| -bor     | Побитовое ИЛИ                                                            | 5 -bor 0x03     |
| -bxor    | Побитовое XOR                                                            | 5 -bxor 3       |
| -shl     | Сдвигает биты влево                                                      | 102 -shl 2      |
| -shr     | Сдвигает биты вправо                                                     | 102 -shr 2      |

###### Приоритет оператора

| Приоритет | Оператор                                  | Описание                                        |
| :-------- | :---------------------------------------- | :---------------------------------------------- |
| 1         | ()                                        | Круглые скобки                                  |
| 2         | —                                         | Для отрицательного числа или унарного оператора |
| 3         | *, /, %                                   | Для умножения и деления                         |
| 4         | +,-                                       | Для сложения и вычитания                        |
| 5         | -band, -bnot, -bor, -bxor, -shr, and -shl | Для побитовых операций                          |

###### Операторы присваивания

| Оператор | Описание                                                                                                        |
| :------- | :-------------------------------------------------------------------------------------------------------------- |
| =        | Устанавливает значение переменной на указанное значение                                                         |
| +=       | Увеличивает значение переменной на указанное значение или добавляет указанное значение к существующему значению |
| -=       | Уменьшает значение переменной на заданную величину                                                              |
| *=       | Умножает значение переменной на указанное значение или добавляет указанное значение к существующему значению    |
| /=       | Делит значение переменной на заданное значение                                                                  |
| %=       | Делит значение переменной на заданное значение, а затем присваивает переменной остаток (модуль)                 |
| ++       | Увеличивает значение переменной, присваиваемого свойства или элемента массива на 1                              |
| --       | Уменьшает значение переменной, присваиваемого свойства или элемента массива на 1                                |

###### Операторы сравнения

=== "Равенство"

    | Оператор | Сравнительный тест   |
    | :------- | :------------------- |
    | -eq      | равно                |
    | -ne      | не равно             |
    | -gt      | больше, чем          |
    | -ge      | больше или равно     |
    | -lt      | меньше чем           |
    | -le      | меньше чем или равно |

=== "Соответствие"

    | Оператор  | Сравнительный тест                       |
    | :-------- | :--------------------------------------- |
    | -like     | строка соответствует шаблону подстановки |
    | -notlike  | строка не соответствует шаблону          |
    | -match    | строка соответствует regex-шаблону       |
    | -notmatch | строка не соответствует regex-шаблону    |

=== "Сдерживание"

    | Оператор     | Сравнительный тест               |
    | :----------- | :------------------------------- |
    | -contains    | коллекция содержит значение      |
    | -notcontains | коллекция не содержит значения   |
    | -in          | значение находится в коллекции   |
    | -notin       | значение отсутствует в коллекции |

=== "Тип"

    | Оператор | Сравнительный тест               |
    | :------- | :------------------------------- |
    | -is      | оба объекта имеют одинаковый тип |
    | -isnot   | объекты разного типа             |

=== "Замена"

    | Оператор | Сравнительный тест                             |
    | :------- | :--------------------------------------------- |
    | -replace | заменяет строки, соответствующие шаблону regex |

###### Логические операторы

| Оператор | Описание                                                                            | Пример                   |
| :------- | :---------------------------------------------------------------------------------- | :----------------------- |
| -and     | Логическое И. TRUE, когда оба утверждения истинны.                                  | (1 -eq 1) -and (1 -eq 2) |
| -or      | Логическое ИЛИ. TRUE, когда любое из утверждений истинно.                           | (1 -eq 1) -or (1 -eq 2)  |
| -xor     | Логическое ИСКЛЮЧАЮЩЕЕ ИЛИ. ИСТИНА, когда только одно утверждение является истиной. | (1 -eq 1) -xor (2 -eq 2) |
| -not     | Логическое не. Отрицает утверждение, которое следует за ним.                        | -not (1 -eq 1)           |
| !        | То же, что и -not                                                                   | !(1 -eq 1)               |

###### Оператор перенаправления

| Оператор | Описание                                        | Синтаксис |
| :------- | :---------------------------------------------- | :-------- |
| >        | Отправить указанный поток в файл                | n>        |
| >>       | Добавить указанный поток в файл                 | n>>       |
| >&1      | Перенаправляет указанный поток на поток Success | n>&1      |

###### Операторы типа

| Оператор | Описание                                                                          | Пример                       |
| :------- | :-------------------------------------------------------------------------------- | :--------------------------- |
| -isNot   | Возвращает TRUE, если входные данные не являются экземпляром указанного.NET типа. | (get-date) -isNot [DateTime] |
| -as      | Преобразует входные данные в указанный тип .NET.                                  | «5/7/07» -as [DateTime]      |

###### Другие операторы

| Оператор | Описание                                                                                               |
| :------- | :----------------------------------------------------------------------------------------------------- |
| ()       | Оператор группировки. Позволяет переопределить старшинство операторов в выражениях.                    |
| &()      | Оператор подвыражения. Выдает результат одного или нескольких утверждений.                             |
| @( )     | Оператор подвыражения массива. Возвращает результаты одного или нескольких операторов в виде массивов. |
| &        | Фоновый оператор. Конвейер перед & выполняется этой командой в задании Powershell.                     |
| []       | Cast оператор. Преобразует объекты к определенному типу.                                               |

###### Регулярные выражения

Регулярные выражения PowerShell по умолчанию не чувствительны к регистру.

| Метод            | Чувствительность к случаю                        |
| :--------------- | :----------------------------------------------- |
| Select-String    | use -CaseSensitive switch                        |
| switch statement | use the -casesensitive option                    |
| operators        | prefix with ‘c’ (-cmatch, -csplit, or -creplace) |

##### Управление потоком

###### ForEach-Object

###### For

###### Do

###### While

##### Переменные

PowerShell позволяет хранить все типы значений. Например, он может хранить результаты команд и элементы командных выражений, такие как имена, пути и параметры.

**Переменные, созданные пользователем**: Они создаются и поддерживаются пользователем. Переменные, которые вы создаете в командной строке PowerShell, будут существовать только до тех пор, пока открыто окно PowerShell. Когда вы закрываете окно PowerShell, эти переменные удаляются. Если вы хотите сохранить переменную, вам необходимо добавить ее в свой профиль PowerShell. Вы можете создавать переменные и объявлять их с тремя различными диапазонами: глобальным, скриптовым или локальным.

**Автоматические переменные**: Эти переменные хранят состояние PowerShell и создаются PowerShell. Только PowerShell может изменять их значения по мере необходимости для поддержания точности. Пользователи не могут изменять значение этих переменных. Например, переменная $PSHOME будет хранить путь к директории установки PowerShell.

**Переменные предпочтений**: Эти переменные хранят предпочтения пользователя для PowerShell и создаются PowerShell. Эти переменные заполнены значениями по умолчанию и могут быть изменены пользователями. Например, переменная $MaximumHistoryCount задает максимальное количество записей в истории сеансов.

!!! info ""
    Чтобы создать новую переменную, необходимо использовать оператор присваивания и присвоить переменной значение. Объявлять переменную перед ее использованием не нужно. Значение по умолчанию для всех переменных — ^^$null^^.

### 22.5 Некоторые команды awk

Awk полезен для разделения полей, подобного cut, но более мощным способом. Для получения других примеров поиск в этом документе. См., например, [gnulamp.com](http://www.gnulamp.com/awk.html) и [one-liners для awk](http://student.northpark.edu/pemente/awk/awk1line.txt) несколько примеров.

!!! example ""
    **awk '{ print \$2, \$1 }' file**                  - Вывести и инвертировать первые два столбца  
    **awk '{printf("%5d : %s\n", NR,\$0)}' file**     - Добавить номер строки слева  
    **awk '{print FNR "\t" \$0}' files**              - Добавить номер строки справа  
    **awk NF test.txt**                              - удалить пустые строки (то же самое, что и grep '.')  
    **awk 'length > 80'**                            - вывести строки длиннее 80 символов)  

### 22.6 Некоторые команды sed

Хорошее введение и учебник по [sed](http://www.grymoire.com/Unix/Sed.html).

!!! example ""
    **sed 's/string1/string2/g'**                          - Заменить string1 на string2  
    **sed -i 's/wroong/wrong/g' *.txt**                    - Заменить повторяющееся слово с помощью g  
    **sed 's/\\(.*\\)1/\12/g'**                            - Изменить anystring1 на anystring2  
    **sed '/&lt;p&gt;/,/&lt;/p&gt;/d' t.xhtml**                     - Удалить строки, начинающиеся с `<p>` и заканчивающиеся `</p>`  
    **sed '/ \*#/d; /\^ \*\$/d'**                              - Удалить комментарии и пустые строки  
    **sed 's/[ \t]\*\$//'**                                  - Удалить конечные пробелы (используйте вкладку вместо \t)  
    **sed 's/\^[ \t]\*//;s/[ \t]\*\$//'**                    - Удаление ведущих и завершающих пробелов  
    **sed 's/[\^\*]/[&amp;]/'**                              - Заключить первый символ в []  
    **sed = file | sed 'N;s/\n/\t/' &gt; file.num**        - Нумерация строк в файле  

### 22.7 Регулярные выражения

Некоторые базовые регулярные выражения, полезные также для sed. Для более подробной информации о синтаксисе основных регулярных выражений см. [Basic Regex Syntax](http://www.regular-expressions.info/reference.html).

!!! example ""
    **\[\\^\$.|?\*+()**                          - специальные символы, любой другой символ будет соответствовать самому себе  
    **\\**                                    - эскейпирование специальных символов и обработка их как литералов  
    **\***                                    - повтор предыдущего элемента ноль или более раз  
    **.**                                    - один символ, кроме символов переноса строки  
    **.***                                   - соответствует нулю или более символов  
    **^**                                    - соответствует началу строки/строки  
    **\$**                                    - соответствует концу строки/строки  
    **.\$**                                   - соответствует одному символу в конце строки/строки  
    **^ \$**                                  - соответствует строке со своим единственным пробелом  
    **[^A-Z]**                               - соответствует строке, начинающейся с любого символа от A до Z  

### 22.8 Некоторые полезные команды

Следующие команды полезно включить в скрипт или использовать в однострочных командах.

!!! example ""
    **sort -t. -k1,1n -k2,2n -k3,3n -k4,4n**                               - Сортировка IPv4 адресов  
    **echo 'Test' | tr '[:lower:]' '[:upper:]'**                           - Преобразование регистра  
    **echo foo.bar | cut -d . -f 1**                                       - Возвращает foo  
    **PID=\$(ps | grep script.sh | grep bin | awk '{print \$1}')**           - PID запущенного скрипта  
    **PID=\$(ps axww | grep [p]ing | awk '{print \$1}')**                    - PID ping (без grep pid)  
    **IP=\$(ifconfig \$INTERFACE | sed '/.\*inet /!d;s///;s/ .\*/ /')**      - Linux  
    **IP=\$(ifconfig \$INTERFACE | sed '/.\*inet /!d;s///;s/ .\*/ /')**      - FreeBSD  
    **if [ `diff file1 file2 | wc -l` != 0 ]; then [...] fi**              - Изменен файл?  
    **cat /etc/master.passwd | grep -v root | grep -v \\\*: | awk -F":" \\** - Создание http-пароля  
    **'{ printf("%s:%s\n", \$1, \$2) }' &gt; /usr/local/etc/apache2/passwd**  
    **testuser=\$(cat /usr/local/etc/apache2/passwd | grep -v \\**          - Проверка пользователя в файле паролей  
    **root | grep -v \\\*: | awk -F":" '{ printf("%s\n", \$1) }' | grep ^user\$)**  
    **tail +2 file &gt; file2**                                            - удалить первую строку из файла  

Используя этот маленький трюк, чтобы одновременно изменить расширение файла для множества файлов. Например, с .cxx на .cpp. Сначала протестируйте его без `| sh` в конце. Вы также можете сделать это с помощью команды `rename`, если она установлена. Или с помощью встроенных средств `bash`.

!!! example ""
    **# ls *.cxx | awk -F. '{print "mv "\$0" "\$1".cpp"}' | sh**  
    **# ls *.c | sed "s/.*/cp & &.\$(date "+%Y%m%d")/" | sh**      - например, копирование `*.c` в `*.c.20080401`  
    **# rename .cxx .cpp *.cxx**                                  - Переименовать все `.cxx` в `.cpp`  
    **# for i in *.cxx; do mv \$i \${i%%.cxx}.cpp; done**           - с помощью встроенных средств bash  
