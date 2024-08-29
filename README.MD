# Сервис для обновления или добавления BAD меток в SQL таблицу

## Описание сервиса

Сервис позволяет добавлять или обновлять BAD метки в SQL таблицу через HTTP запросы.

### Добавить или обновить данные в таблице

**Метод:** POST  
**URL:** `http://host:8002/push/`  
**Формат данных:** JSON  

**Ключи реквеста:**
- `code`: трехбуквенный код обсерватории, string, регистр не важен
- `date0`: время с, в unix time, секунды
- `date1`: время до, включительно, в unix time, секунды
- `action`: 1 - добавить метку, 0 - убрать метку
- `comp`: выбор компоненты магнитного вектора, v1, v2, v3, f
- `freq`: размерность времени, min и sec

**Пример запроса:**
```json
{
    "code": "KLI",
    "date0": 1659330000,
    "date1": 1659333600,
    "action": 0,
    "comp": "v3",
    "freq": "min"
}
```

**Ответ:**
- Успех: `{'status': 0}`
- Ошибка: `{'status': 1}`

## Развертывание с использованием Docker

### Локальное развертывание

1. **Сборка Docker образа:**
    ```sh
    docker build . -t docker-byte-marks-v0.1
    ```

2. **Запуск контейнера:**
    ```sh
    docker run -p 8002:8002 docker-byte-marks-v0.1
    ```

### Развертывание на сервере `gm.gcras.ru`

1. **Сборка Docker образа:**
    ```sh
    docker build . -t docker-byte-marks-v0.1
    ```

2. **Тегирование образа:**
    ```sh
    docker tag %TAG% docker.gcras.ru/docker-byte-marks-v0.1
    ```

3. **Пуш образа на сервер:**
    ```sh
    docker push docker.gcras.ru/docker-byte-marks-v0.1
    ```

4. **Подключение к серверу и запуск контейнера:**
    ```sh
    ssh gm.....
    docker pull docker.gcras.ru/docker-byte-marks-v0.1
    docker run -d -p 8002:8002 docker.gcras.ru/docker-byte-marks-v0.1
    ```

Теперь сервис готов к использованию через указанный URL.