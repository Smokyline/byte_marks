Сервис для обновления или добавления BAD меток в SQL таблицу

1) Добавить или обновить данные в таблице
JSON реквест посылать по адресу http://host:8002/push/
Ключи реквеста
code - трехбуквенный код обсерватории, string, регистр не важен
date0 - время с, в unix time, секунды
date1 - время до, включительно, в unix time, секунды
action - 1 добавить метку, 0 - убрать метку
comp - выбор компоненты магнитного вектора, v1, v2, v3, f
frec - размерность времени, min и sec

{
    "code":"KLI",
    "date0":1659330000,
    "date1":1659333600,
    "action":0,
    "comp":"v3",
    "frec":"min"

}

Если все прошло успешно, возвращает в ответ за запрос {'status':0}, если нет - {'status':1}





HOW TO DOCKER THIS

# забилдить и запустить локально
docker build . -t docker-byte-marks-v0.1
docker run -p 8002:8002 docker-byte-marks-v0.1

# забилдить и запустить на gm.gcras.ru
docker build . -t docker-byte-marks-v0.1
docker tag %TAG% docker.gcras.ru/docker-byte-marks-v0.1
docker push docker.gcras.ru/docker-byte-marks-v0.1
ssh gm.....
docker pull docker.gcras.ru/docker-byte-marks-v0.1
docker run -d -p 8002:8002 docker.gcras.ru/docker-byte-marks-v0.1