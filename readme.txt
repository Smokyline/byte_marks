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