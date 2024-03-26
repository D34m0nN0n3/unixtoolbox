## 17 Конвертирование медиафайлов

!!! abstract ""
    [Текст](#171-кодирование-текста) | [Перевод строки](#172-unix---dos-переводы-строк) | [PDF](#173-преобразование-pdf-в-jpeg-и-объединение-файлов-pdf) | [Видео](#174-преобразование-видео) | [Аудио CD](#175-копирование-аудио-cd)

Иногда просто требуется преобразовать видео-, аудиофайл или документ в другой формат.

### 17.1 Кодирование текста

Кодирование текста может идти совершенно неправильно, особенно когда язык требует специальных символов, таких как àäç. Команда iconv может конвертировать из одной кодировки в другую.

!!! example ""
    **# iconv -f <исходная_кодировка> -t <целевая_кодировка> <входной_файл>**  
    **# iconv -f ISO8859-1 -t UTF-8 -o file.input &gt; file_utf8**  
    **# iconv -l**                           - Список известных кодировок символов  

Если не указывать опцию `-f`, iconv будет использовать локальный набор символов, что обычно подходит, если документ отображается правильно.
Преобразовать имена файлов из одной кодировки в другую (не контент файла). Работает также, если только некоторые файлы уже в формате `utf8`.

!!! example ""
    **# convmv -r -f utf8 --nfd -t utf8 --nfc /путь/к/директории/\* --notest**  

### 17.2 Unix - DOS переводы строк

Преобразовать переводы строк из формата DOS (`CR/LF`) в формат Unix (`LF`) и обратно в оболочке Unix. Обратите также внимание на `dos2unix` и `unix2dos`, если они установлены.

!!! example ""
    **# sed 's/.$//' dosfile.txt &gt; unixfile.txt**                  - DOS в UNIX  
    **# awk '{sub(/\r$/,"");print}' dosfile.txt &gt; unixfile.txt**   - DOS в UNIX  
    **# awk '{sub(/$/,"\r");print}' unixfile.txt &gt; dosfile.txt**   - UNIX в DOS  

Преобразовать переводы строк из формата Unix в формат DOS в среде Windows. Используйте `sed` или `awk` из `mingw` или `cygwin`.

!!! example ""
    **# sed -n p unixfile.txt &gt; dosfile.txt**  
    **# awk 1 unixfile.txt &gt; dosfile.txt**     - UNIX в DOS (с помощью оболочки cygwin)  

Удалить `^M` из файла в формате mac и заменить их на перевод строк в формате Unix. Для получения `^M `используйте ++ctrl+v++, а затем ++ctrl+m++.

!!! example ""
    **# tr '^M' '\n' &lt; macfile.txt**

### 17.3 Преобразование PDF в Jpeg и объединение файлов PDF

Преобразование PDF-документа с помощью gs (GhostScript) в изображения jpeg (или png) для каждой страницы. Также можно использовать convert и mogrify (из ImageMagick или GraphicsMagick), которые гораздо короче.

!!! example ""
    **# gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r150 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \\**  
     **-dMaxStripSize=8192 -sOutputFile=unixtoolbox_%d.jpg unixtoolbox.pdf**  
    **# convert unixtoolbox.pdf unixtoolbox-%03d.png**  
    **# convert *.jpeg images.pdf**                                                          - Создание простого PDF с изображениями  
    **# convert image000* -resample 120x120 -compress JPEG -quality 80 images.pdf**  
    **# mogrify -format png *.ppm**                                                          - Конвертировать все изображения в формате ppm в png формат  

Ghostscript также может объединять несколько pdf файлов в один. Это работает только в случае, если PDF файлы "хорошо сформирован".

!!! example ""
    **# gs -q -sPAPERSIZE=a4 -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=all.pdf \\**  
    **file1.pdf file2.pdf ...**              - На Windows используйте '#' вместо '='  

Извлечение изображений из документа pdf с помощью `pdfimages` из `poppler` или [xpdf](http://foolabs.com/xpdf/download.html)

!!! example ""
    **# pdfimages document.pdf dst/**        - Извлечь все изображения и поместить их в папку `dst`  
    **# yum install poppler-utils**          - Установка `poppler-utils` при необходимости, или:  
    **# apt-get install poppler-utils**  

### 17.4 Преобразование видео

Сжатие видео с камеры Canon с использованием кодека `mpeg4` и исправление некачественного звука.

!!! example ""
    **# mencoder -o videoout.avi -oac mp3lame -ovc lavc -srate 11025 \\**  
    **-channels 1 -af-adv force=1 -lameopts preset=medium -lavcopts \\**  
    **vcodec=msmpeg4v2:vbitrate=600 -mc 0 vidoein.AVI**  

Подробнее о звуковой обработке можно узнать здесь: `sox`.

### 17.5 Копирование аудио CD

Программа [cdparanoia](http://xiph.org/paranoia/) может сохранить аудио дорожки (порт FreeBSD в audio/cdparanoia/), `oggenc` может кодировать в формат Ogg Vorbis, lame конвертирует в mp3.

!!! example ""
    **# cdparanoia -B**                        - Копировать дорожки в wav файлы в текущей директории  
    **# lame -b 256 in.wav out.mp3**           - Кодирование в mp3 с битрейтом 256 кб/с  
    **# for i in *.wav; do lame -b 256 $i `basename $i .wav`.mp3; done**  
    **# oggenc in.wav -b 256 out.ogg**         - Кодирование в Ogg Vorbis с битрейтом 256 кб/с  
