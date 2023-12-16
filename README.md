# Knihi

## Патрабаванні да ўсталёўкі:
1) ОС: Windows (выкарыстоўваецца path)
2) Python 3.12.0 
3) Бібліятэкі Python: PyQt5, sqlite3, json

## Як запусціць:
1) спампаваць архіў і разархіваваць
2) запусціць main.py (cmd: python main.py)

## Гайд па скарыстанню:
Пасля запуска праграмы, з'явіцца акно з адзінаю кнопка -- "Load DB".
У акне выбару файла, якое з'яўляецца па націску на кнопк, трэба абраць файл .JSON, які апісвае структуру базы дадзеных і шлях да яе. 

**Шлях да базы дадзеных(.db) патрэбна ўказваць адносна файлу з апісаннем(.json)!**

Прыклады падобных файлаў можна знайсці ў праекце ў папках "db_main", "db_test". Кожны ўтрымлівае:
* init.sql -- скрыпт для стварэння бд і напаўнення першымі дадзенымі
* description.json -- файл-апісанне структуры бд
* database.db -- база дадзеных

Асноўным з'яўляецца "db_main". На ім будзе паказаная работа праграмы.

## Апісанне работы праграмы:
Праграма пасля загрузкі БД:
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/first_look.png)
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/first_look_db.png)

#### 1) *" Выбирать справочник из списка. "* -- я заўважыла занадта позна, але ў інтэрфейсе існуе спіс, што пакажа, што я ўмею з імі працаваць.
Пераключэнне паміж табліцамі ажыццяўляецца з дапамогаю ўкладак зверху.



#### 2) *"Отображать выбранный справочник в виде таблички. Обеспечить сортировку по колонкам (честно! т.е. числа сортируются как числа, даты выводятся в формате ДД.ММ.ГГГГ и сортируются)."*
Сартыроўка паводле даты рэлізу. Можна заўважыць, што яна выконваецца не лексікаграфічна.

![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/sort_rd.png)

Сартыроўка існуе і ў іншых калонак.

#### 3) *Добавлять, редактировать, удалять, просматривать значения справочника*

Для таго, каб дадаць новы радок у табліцу, трэба абраць укладку з табліцаю і ці націснуць на кнопку "Add new row", ці абраць пункт "Add row" з выпадаючага меню, што з'яўляецца па націску правай кнопкі мышы.

Для таго, каб выдаліць ці правіць радок у табліцы, трэба абраць патрэбны радок і націснуць адпаведны пункт у меню.
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/menus.png)

**1) Дадаць радок**

Радок будзем дадаваць у табліцу "Books". На скрыншоце ніжэй, можна заўважыць наступныя палі:
* многострочное текстовое поле (Title)
* однострочное текстовые и/или числовое поле (Cost, Number of copys)
* выпадающий список/ множественный выбор из другого справочника(Author name)  *абяцаны спіс*
*календарь для выбора/ввода даты (Release Date)
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/add_row_dialog.png)

Прычым заўважым наступную суадноснасць дадзеных у View. Такім чынам мы дакладна ведаем, што дадаем як аўтара "Biba, 12.08.1985"
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/suadn.png)

Абнаўленне табліцы і базы дадзеных:
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/after_add.png)
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/after_add_db.png)

**2) Выдаліць радок**

Пасля выдалення радка "Famous Author" з табліцы "Authors"
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/after_del.png)

Цяпер яго нельга абраць як аўтара падчас стварэння/рэдагавання запісу:
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/after_del_menu.png)

Адпаведны запіс у БД:
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/after_del_db.png)

**3) Правіць радок**

Дыялогавае акно падобнае да акна "Add new row". Загаддзя прастаўленыя папярэднія дадзеныя. Зменім "Number of copys" 1000 -> 300
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/image.png)

Рэзультат:
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/image-1.png)
![Alt text](https://github.com/Lina-Ras/Knihi/blob/main/imgs/image-2.png)
