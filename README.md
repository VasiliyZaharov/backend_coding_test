# Запуск проекта

Если нет Docker, то нужно его установить, ссылка на скачивание:
```
https://www.docker.com/products/docker-desktop/
```
<hr>

1. Склонируйте репозиторий:
```
git clone https://github.com/VasiliyZaharov/backend_coding_test.git
```
2. Перейдите в папку проекта:
```
cd backend_coding_test
```
3. Создайте виртуальное окружение:

Для Windows
```
python -m venv myenv
```
```
myenv\Scripts\activate
```
Для Macos и Linux:
```
python3 -m venv myenv
```
```
source myenv/bin/activate
```
4. Установите зависимости:
```
pip install -r requirements.txt
```
5. Запустите программу Docker
6. Запустите проект:
```
docker-compose up --build
```

<b>Проект будет доступен по адресу:</b>
```
http://localhost:8000/courses
```
<hr>

## API Endpoints

### 1. '/courses': 

Главная страница проекта на которой выводятся все требуемые валютные пары:

<em>BTC-RUB,BTC-USD,ETH-RUB, ETH-USD, USDTTRC-RUB, USDTTRC-USD, USDTERC-RUB, USDTERC-USD</em>
```
http://localhost:8000/courses
```

### 2. '/courses/{symbol}':

Страница с информацией о валютной паре, где {symbol} - это символ валютной пары.
Пример:
```
http://localhost:8000/courses/btcusdt
```
<hr>

## Нагрузочное тестирование

Вы можете провести нагрузочное тестирование с использованием инструмента Locust. Для этого выполните следующие шаги:
1. Нужно убедиться, что вы активировали виртуальное окружение

Для Windows:
```
echo %VIRTUAL_ENV%
```
Если виртуальное окружение активировано, вы увидите имя каталога вашего виртуального окружения. Если виртуальное окружение не активировано, вы увидите пустое значение.

Для macOS/Linux:
```
echo $VIRTUAL_ENV
```
Если виртуальное окружение активировано, вы увидите имя каталога вашего виртуального окружения. Если виртуальное окружение не активировано, вы увидите пустое значение.

Если виртуальное окружение вами не было сделано, то воспользуйтесь следующими командами:

Для Windows
```
python -m venv myenv
```
```
myenv\Scripts\activate
```
Для Macos и Linux:
```
python3 -m venv myenv
```
```
source myenv/bin/activate
```
2. Запустите тесты Locust:
```
locust -f locustfile.py --host=http://localhost:8000
```
3. Откройте браузер и перейдите по адресу, чтобы настроить и запустить тесты.
```
http://localhost:8089
```
### Тесты:
<img width="1355" alt="Снимок экрана 2023-11-07 в 14 22 31" src="https://github.com/VasiliyZaharov/backend_coding_test/assets/109171276/f7ce6dbc-4f53-4e11-91e9-08e099cd1a6b">
<img width="901" alt="Снимок экрана 2023-11-07 в 14 23 30" src="https://github.com/VasiliyZaharov/backend_coding_test/assets/109171276/e4a35b39-bbf2-439a-8a3c-3217ed31fa0b">
<img width="1340" alt="Снимок экрана 2023-11-07 в 14 24 21" src="https://github.com/VasiliyZaharov/backend_coding_test/assets/109171276/5559a01e-249d-44d8-84ca-ef2dc25725de">






