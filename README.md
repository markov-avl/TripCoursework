# TripCoursework

Реализация программного обеспечения на основе онтологической модели и прототипа интерфейса из курсовой работы

## Технологии

- Backend: Flask
- Frontend: Jinja2

## Фикстуры

Накатить фикстуры можно следующим образом:

```
GET http://{host:port}/fixtures/load
```

## Главная

Создание путешествия:

```
GET http://{host:port} --> http://{host:port}/trips/{trip_secret}
```

Главной страницы так таковой не существует: это просто перенаправление на редактирование нового путешествия

## Путешествия

Редактирование путешествия:

```
GET http://{host:port}/trips/{trip_secret}
```

Маршруты путешествия (**WIP**):

```
GET http://{host:port}/trips/{trip_secret}/routes
```

## Города

Редактирование городов:

```
GET http://{host:port}/cities
```

Редактирование дорог в городе:

```
GET http://{host:port}/cities/{city_id}/roads
```

Редактирование мест в городе:

```
GET http://{host:port}/cities/{city_id}/places
```

Просмотр карты города:

```
GET http://{host:port}/cities/{city_id}/map?roads=true&places=true&ids=true

# По умолчанию все параметры выставлены как true
```

Просмотр кратчайшего пути между местами в городе:

```
GET http://{host:port}/cities/{city_id}/shortest-path?start_id={start_id}&destination_id={destination_id}
```
