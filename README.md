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

## Города

```
# Просмотр карты города:
GET http://{host:port}/cities/{city_id}/map?places=true&roads=true&ids=true

# По умолчанию все параметры выставлены как true
```

```
# Просмотр ближайших дорог:
GET http://{host:port}/cities/{city_id}/nearest-roads?place_id={place_id}&ids=true

# По умолчанию параметр ids выставлен как true
```

```
# Просмотр кратчайшего пути между местами:
GET http://{host:port}/cities/{city_id}/shortest-path?start_id={start_id}&destination_id={destination_id}
```