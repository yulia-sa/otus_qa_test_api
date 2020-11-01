## Описание

Задание курса «Python QA Engineer» (OTUS)

### Тестирование API

Цель:  
Тестирование API сервиса с помощью Python, используя библиотеки pytest, requests, jsonschema.

#### Задание 1

Тестирование сервиса jsonplaceholder.typicode.com.  
Написать тесты для todos — https://jsonplaceholder.typicode.com/todos  
Документация — https://jsonplaceholder.typicode.com/guide  
Где есть возможность нужно использовать параметризацию.

##### Список тестов:

a) positive/negative тесты для Getting a resource.  
В negative тестах нужно найти ситуацию, когда API возвращает код 400 и пустой массив данных и написать тесты для этого случая.

b) positive тесты для Listing all resources.

c) positive тесты для Creating a resource.

d) positive/negative тесты для Updating a resource with PUT.  
В negative тестах нужно найти ситуацию, когда API возвращает код 500 и написать тесты для этого случая

e) positive тесты для Updating a resource with PATCH.

f) positive тесты для Deleting a resource.

g) positive/negative тесты для Filtering resources.  
В negative тестах нужно убедиться, что при передаче в запросе невалидных значений полей “userId", “id”, “title” и “completed” - API возвращает код 200 и пустой массив данных и написать тесты для этого случая

Все тесты должны успешно проходить.

#### Установка

Python3 должен быть уже установлен. 
Затем используем `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```#!bash

pip install -r requirements.txt

```

#### Запуск
```#!bash

$ pytest test_api_todos.py

```