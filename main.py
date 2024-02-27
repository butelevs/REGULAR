import csv
import re
from pprint import pprint

## Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
re_pattern = r"^(?P<lastname>\w+)[\s,]*(?P<firstname>\w+)[\s,]*(?P<surname>\w*)[\s,]*(?P<organization>[\w]*),(?P<position>[\w\s\-\–]*),(?P<phone>[\w\d\s\(\)\-\+\.]*),(?P<email>[\w\d\.\-\_@]*)"
re_pattern_replace = r"\g<lastname>,\g<firstname>,\g<surname>,\g<organization>,\g<position>,\g<phone>,\g<email>"
re_contacts = re.compile(re_pattern)
contacts_list_fixed = [re_contacts.sub(re_pattern_replace, ','.join(contact)).split(',') for contact in contacts_list]
pprint(contacts_list_fixed)

# 2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
re_phone_long = r"(\+7|8)?[\s\(]*(\d{3})[\)\s\-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\sдоб\.\(]+(\d*)\)*"
re_phone_long_rep = r"+7(\2)\3-\4-\5 доб.\6"
re_phone = r"(\+7|8)?[\s\(]*(\d{3})[\)\s\-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
re_phone_rep = r"+7(\2)\3-\4-\5"
re_phone_long = re.compile(re_phone_long)
re_phone = re.compile(re_phone)

for i, contact in enumerate(contacts_list_fixed):
    phone = contact[5]
    if re_phone_long.match(phone):
        contacts_list_fixed[i][5] = re_phone_long.sub(re_phone_long_rep, phone)
    else:
        contacts_list_fixed[i][5] = re_phone.sub(re_phone_rep, phone)
pprint(contacts_list_fixed)

# 3. Объединить все дублирующиеся записи о человеке в одну.
contacts_fixed = {}
for contact in contacts_list_fixed:
    if contacts_fixed.get(contact[0]+contact[1]) is None:
        contacts_fixed[contact[0]+contact[1]] = contact
    else:
        for i in range(7):
            contacts_fixed[contact[0]+contact[1]][i] = max(contact[i], contacts_fixed[contact[0]+contact[1]][i])
pprint(contacts_fixed)
pprint(contacts_fixed.values())

## 4. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w" ,encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')

## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_fixed.values())