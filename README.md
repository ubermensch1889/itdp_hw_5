## Дано
- Развернутый на 3 нодах кластер HDFS
- Все ноды проименованы (tmpl-nn, tmpl-dn-00, tmpl-dn-00)
- Yarn поднят
- Apache Hive развернут
- Apache Spart установлен и настроен в соответствии с предыдущей инструкцией
- На hdfs загружен csv файл. Пусть он имеет стуктуру, как у файла по [ссылке](https://www.kaggle.com/datasets/abdulmalik1518/mobiles-dataset-2025). Название - mobiles.csv. 


## Инструкция

Загружаем скрипт.
```
git clone https://github.com/ubermensch1889/itdp_hw_5.git
cd itdp_hw_5
```

Создаем виртуальную среду.
```
python3 -m venv venv
source venv/bin/activate
```

Выполняем скрипт. Он установит нужные зависимости, преобразует загруженный csv файл и выгрузит его в таблицу.
```
sh script.sh
```

