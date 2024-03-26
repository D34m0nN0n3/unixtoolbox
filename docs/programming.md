## 23 Программирование

!!! abstract ""
    [Основы C](#231-основы-c) | [Примеры C](#232-пример-на-c) | [Основы C++](#233-основы-c) | [Пример C++](#234-пример-на-c) | [Makefile](#235-простой-makefile) | [Python](#236-python) | [Golang](#237-golang)

### 23.1 Основы C

!!! example ""
    ```c
    strcpy(newstr, str)                                                            /* копирование str в newstr */
    expr1 ? expr2 : expr3                                                          /* если (expr1) то expr2 иначе expr3 */
    x = (y > z) ? y : z;                                                           /* если (y > z) то x = y иначе x = z */
    int a[] = {0, 1, 2};                                                           /* Инициализированный массив (или a[3] = {0, 1, 2};) */
    int i = 12345;                                                                 /* Преобразование в i в char str */
    char str[10];
    sprintf(str, "%d", i);
    ```

### 23.2 Пример на C

Простая программа на C:

!!! example ""
    ```c
    #include <stdio.h>
    int main() {
        int number = 42;
        printf("Ответ: %i\n", number);  
    }
    ```

Компиляция:

!!! example ""
    ```bash
    # gcc simple.c -o simple
    # ./simple
    ```
    Ответ: 42

### 23.3 Основы C++

!!! example ""
    ```cpp
    *pointer                                  // Объект, на который указывает указатель
    &obj                                      // Адрес объекта obj
    obj.x                                     // Член x класса obj (объект obj)
    pobj->x                                   // Член x класса, на который указывает pobj
                                              // (*pobj).x и pobj->x - это одно и то же
    ```

### 23.4 Пример на C++

Вот немного более реалистичная программа на C++: класс в своем заголовочном файле (IPv4.h) и реализация (IPv4.cpp), а также программа, которая использует функциональность класса. Класс преобразует IP-адрес в целочисленном формате в известный квадратный формат.

Класс IPv4:

!!! example "IPv4.h"
    ```cpp
    #ifndef IPV4_H
    #define IPV4_H
    #include <string>
    
    namespace GenericUtils {                          // создание пространства имен
    class IPv4 {                                      // определение класса
    public:
        IPv4();
        ~IPv4();
        std::string IPint_to_IPquad(unsigned long ip); // интерфейс члена класса
    };
    } // namespace GenericUtils
    #endif // IPV4_H
    ```

!!! example "IPv4.cpp"
    ```cpp
    #include "IPv4.h"
    #include <string>
    #include <sstream>
    using namespace std;                              // использование пространств имен
    using namespace GenericUtils;
    
    IPv4::IPv4() {}                                   // конструктор/деструктор по умолчанию
    IPv4::~IPv4() {}
    string IPv4::IPint_to_IPquad(unsigned long ip) {  // реализация метода класса
        ostringstream ipstr;                          // используем stringstream
        ipstr << ((ip & 0xff000000) >> 24)            // побитовый сдвиг вправо
              << "." << ((ip & 0x00ff0000) >> 16)
              << "." << ((ip & 0x0000ff00) >> 8)
              << "." << ((ip & 0x000000ff));
        return ipstr.str();
    }
    ```

Программа simplecpp.cpp

!!! example ""
    ```cpp
    #include "IPv4.h"
    #include <iostream>
    #include <string>
    using namespace std;
    int main (int argc, char* argv[]) {
        string ipstr;                                 // определение переменных
        unsigned long ipint = 1347861486;             // IP в целочисленной форме
        GenericUtils::IPv4 iputils;                   // создание объекта класса
        ipstr = iputils.IPint_to_IPquad(ipint);       // вызов метода класса
        cout << ipint << " = " << ipstr << endl;      // вывод результата
    
        return 0;
    }
    ```

Компиляция и выполнение:

!!! example ""
    **# g++ -c IPv4.cpp simplecpp.cpp**                - компиляция в объектные файлы  
    **# g++ IPv4.o simplecpp.o -o simplecpp.exe**      - связывание объектных файлов в исполняемый файл  
    **# ./simplecpp.exe**  
    *1347861486 = 80.86.187.238*  

Используйте `ldd`, чтобы проверить, какие библиотеки используются исполняемым файлом и где они находятся. Также используется для проверки, отсутствует ли общая библиотека или является ли исполняемый файл статическим.

!!! example ""
    **# ldd /sbin/ifconfig**                           - список зависимостей от динамических объектов  
    **# ar rcs staticlib.a *.o**                       - создание статического архива  
    **# ar t staticlib.a**                             - печать списка объектов из архива  
    **# ar x /usr/lib/libc.a version.o**               - извлечение объектного файла из архива  
    **# nm version.o**                                 - показать функции, предоставляемые объектом  

### 23.5 Простой Makefile

Ниже приведен минимальный Makefile для многофайловой программы. Строки с инструкциями должны начинаться с табуляции! Обратный слеш "\" можно использовать для разделения длинных строк.

!!! example ""
    ```makefile
    CC = g++
    CFLAGS = -O
    OBJS = IPv4.o simplecpp.o
    
    simplecpp: ${OBJS}
    	${CC} -o simplecpp ${CFLAGS} ${OBJS}
    clean:
    	rm -f ${TARGET} ${OBJS}
    ```

### 23.6 Python



### 23.7 Golang


