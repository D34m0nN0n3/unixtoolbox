## 21 Оболочки

!!! abstract ""
    [Bash](#211-bash) | [tcsh](#212-tcsh) | [Горячии клавиши](#213-горячии-клавиши)

Большинство дистрибутивов Linux используют оболочку `bash`, в то время как в BSD используется `tcsh`, `bourne shell` используется только для сценариев. Фильтры очень полезны и могут быть использованы в конвейере:

!!! info ""
    **grep** &nbsp; Поиск по шаблону  
    **sed** &nbsp; Поиск и замена строк или символов  
    **cut** &nbsp; Вывод определенных столбцов из маркера  
    **sort** &nbsp; Сортировка в алфавитном или числовом порядке  
    **uniq** &nbsp; Удаление повторяющихся строк из файла  

Например, использование всех сразу:

!!! example ""
    **# ifconfig | sed 's/  / /g' | cut -d" " -f1 | uniq | grep -E "[a-z0-9]+" | sort -r**  - получить сортированный список всех интерфейсов  
    **# ifconfig | sed '/.*inet /!d;s///;s/ .*//'|sort -t. -k1,1n -k2,2n -k3,3n -k4,4n**    - получить сортированный список всех IP адресов  

Первый символ в шаблоне `sed` - табуляция. Чтобы написать табуляцию в консоли, используйте ++ctrl+v++ ++ctrl+tab++.

### 21.1 bash

Перенаправление и конвейеры для `bash` и `sh`:

!!! example ""
    **# cmd 1&gt; file**                                - Перенаправить stdout в файл  
    **# cmd 2&gt; file**                                - Перенаправить stderr в файл  
    **# cmd 1&gt;&gt; file**                            - Перенаправить и добавить stdout в файл  
    **# cmd &amp;&gt; file**                            - Перенаправить как stdout, так и stderr в файл  
    **# cmd &gt;file 2&gt;&amp;1**                      - Перенаправить stderr в stdout, а затем в файл  
    **# cmd1 | cmd2**                                     - Передать stdout в cmd2  
    **# cmd1 2&gt;&amp;1 | cmd2**                         - Передать stdout и stderr в cmd2  

Измените свою конфигурацию в `~/.bashrc` (она также может быть `~/.bash_profile`). Следующие записи полезны, перезагрузите с помощью ". .bashrc". С cygwin используйте `~/.bash_profile`; в `rxvt` вставьте с помощью shift + left-click.

В `.bashrc`

!!! example "Удобная работа с историей команд"
    **bind '"\e[A"':history-search-backward** - Используйте стрелки вверх для поиска  
    **bind '"\e[B"':history-search-forward**  - Используйте стрелки вниз для поиска  
    **set -o emacs**                          - Установите режим эмуляции emacs в bash (см. ниже)  
    **set bell-style visible**                - Не издавать звукового сигнала, инвертировать цвета  

!!! example "Установить хорошую строку приглашения вида [user@host]/path/todir&gt;"
    **PS1="\\[\033[1;30m\\][\\[\033[1;34m\\]\u\\[\\033[1;30m\\]"**  
    **PS1="\$PS1&commat;\\[\033[0;33m\\]\\h\\[\033[1;30m\\]]\\[\033[0;37m\\]"**  
    **PS1="\$PS1\w\\[\033[1;30m\\]&gt;\\[\033[0m\\]"**  

!!! example "Установить хорошую строку приглашения вида `Mon Sep 11-user@host:~ `"
    **PS1="\\[\e[33m\\]\d\\[\e[m\\]-\\[\e[m\\]\\[\e[31m\\]\u\\[\e[m\\]@\\[\e[32m\\]\H\\[\e[m\\]:\\[\e[34m\\]\W\\[\e[m\\]\\[\e[34m\\]\\`parse_git_branch\`\\[\e[m\\]\\[\e[32m\\]\\`nonzero_return\`\\[\e[m\\] \\\\$**

!!! example "Чтобы проверить текущие активные псевдонимы, просто введите alias"
    **alias ls='ls -aF'**                    - Добавить индикатор (один из */=&gt;@|)  
    **alias ll='ls -aFls'**                  - Список  
    **alias la='ls -all'**  
    **alias ..='cd ..'**  
    **alias ...='cd ../..'**  
    **export HISTFILESIZE=5000**              - Больший размер истории  
    **export CLICOLOR=1**                     - Использовать цвета (при возможности)  
    **export LSCOLORS=ExGxFxdxCxDxDxBxBxExEx**  

### 21.2 tcsh
Перенаправления и трубы для `tcsh` и `csh` (простое &gt; и &gt;&gt; такое же, как в `sh`):

!!! example ""
    **# cmd &gt;&amp; file**                         - Перенаправить как stdout, так и stderr в файл  
    **# cmd &gt;&gt;&amp; file**                     - Добавить stdout и stderr в файл  
    **# cmd1 | cmd2**                                  - Передать stdout в cmd2  
    **# cmd1 |&amp; cmd2**                             - Передать stdout и stderr в cmd2  


Настройки для csh/tcsh устанавливаются в файле `~/.cshrc`, перезагружаются с помощью `source .cshrc`. Примеры:

!!! example ""
    **alias ls 'ls -aF'**  
    **alias ll 'ls -aFls'**  
    **alias la 'ls -all'**  
    **alias .. 'cd ..'**  
    **alias ... 'cd ../..'**  
    **set prompt = "%B%n%b@%B%m%b%/> "**    - вроде user@host/path/todir&gt;  
    **set history = 5000**  
    **set savehist = (6000 merge)**  
    **set autolist**                        - Предлагать возможные варианты при нажатии на ++tab++  
    **set visiblebell**                     - Не издавать звуковой сигнал, инверсные цвета  

!!! example "Привязка клавиш и цвета"
    **bindkey -e     Select Emacs bindings**  - Использовать клавиши emacs для изменения строки командной строки  
    **bindkey -k up history-search-backward** - Использовать стрелку вверх и вниз для поиска  
    **bindkey -k down history-search-forward**  
    **setenv CLICOLOR 1**                     - Использовать цвета (при возможности)  
    **setenv LSCOLORS ExGxFxdxCxDxDxBxBxExEx**  

### 21.3 Горячии клавиши

Режим emacs позволяет использовать сокращения клавиш emacs для изменения строки командной строки. Это крайне полезно (не только для пользователей emacs). Самые используемые команды это:

!!! example ""
    *C-a* &nbsp; &nbsp; &nbsp; Переместить курсор в начало строки  
    *C-e* &nbsp; &nbsp; &nbsp; Переместить курсор в конец строки  
    *M-b* &nbsp; &nbsp; &nbsp; Переместить курсор назад на одно слово  
    *M-f* &nbsp; &nbsp; &nbsp; Переместить курсор вперед на одно слово  
    *M-d* &nbsp; &nbsp; &nbsp; Вырезать следующее слово  
    *C-w* &nbsp; &nbsp; &nbsp; Вырезать последнее слово  
    *C-u* &nbsp; &nbsp; &nbsp; Вырезать все перед курсором  
    *C-k* &nbsp; &nbsp; &nbsp; Вырезать все после курсора (остаток строки)  
    *C-y* &nbsp; &nbsp; &nbsp; Вставить последнюю вырезанную часть (просто вставить)  
    *C-_* &nbsp; &nbsp; &nbsp; Отменить  

Примечание: C- = удерживайте клавишу ++ctrl++, M- = удерживайте клавишу Meta (которая обычно является клавишей ++alt++ или ++escape++).
