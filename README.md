# Scrap - парсер для Авито!

Внимание! Это мой первый, осознанный и пока ещё песочный проект


**Scrap -** в частности скрипт, который парсит доску с определённой категорией  товаров. Пока что рано говорить, что любой может им легко  воспользоваться, но для меня это мотивация довести проект до конца.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
## Установка и инструкции к эксплуатации:

1) Клонируем репозитрий на локальный компьютер
```console
$ git clone "https://github.com/ChehST/scrap.git"
```

2) Устанавливаем настраиваем виртуальное окружение, тянем зависимости
```console
$ cd scrap
$ python -m venv venv
$ source venv/bin/adctivate    # Активируем venv
$ pip install -r reguirements.txt
$ deactivate     # Деактивируем venv
```

3) Приступаем к эксплуатации:
   Не забываем активировать venv перед запуском,
```console
$ source venv/bin/adctivate    # Активируем venv
$ python main/scrap_cli.py [URL]
```
На место URL вставляем полную ссылку с интересующей вас категорией
**пример:**
```console
$ python main/scrap_cli.py https://www.avito.ru/habarovsk/bytovaya_elektronika
```

Если есть прокси, нужно их указать как:
```console
$ python main/scrap_cli.py https://www.avito.ru/your/request -p path/to/proxy_list.csv
```

На выходе получаем файл *parsed_data.csv* в корневой папке scrap/
![Data csv file](https://github.com/ChehST/scrap/blob/develop/docs/images/data_csv.png)
