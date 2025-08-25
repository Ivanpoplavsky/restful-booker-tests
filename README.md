# RESTful Booker — API автотесты (PyTest + Requests + Pydantic)

📌 Тестовое задание: автоматизация публичного API [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html)  
Стек: **Python 3.10+, PyTest, Requests, Pydantic, Faker**


🔗 Репозиторий на GitHub: [Ivanpoplavsky/restful-booker-tests](https://github.com/Ivanpoplavsky/restful-booker-tests)


---

## Покрытие тестов
- **CRUD** сценарии для `/booking`
- **Авторизация** `/auth` (cookie `token`)
- **Негативные сценарии**: неверные креды, действия без токена, несуществующий ID
- **Валидация JSON-схемы** через Pydantic
- **Генерация данных** через Faker
- **Нагрузочное тестирование** Locust

---

## Особенности API (важно!)
- `POST /auth`  
  ⮕ при неверных кредах возвращает `200 OK` + `{ "reason": "Bad credentials" }` (а не `401`).  
- `PUT /booking/{id}`, `PATCH /booking/{id}`  
  ⮕ по документации должны возвращать **`200 OK`** с обновлённым объектом.  
- `DELETE /booking/{id}`  
  ⮕ спецификация ожидает **`201 Created`**, хотя в REST обычно используют `204 No Content`.  
- `DELETE` для несуществующего id иногда даёт `405 Method Not Allowed` (особенность демо-сервиса).  


---

## Установка
```bash
git clone https://github.com/Ivanpoplavsky/restful-booker-tests.git
cd restful-booker-tests

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

---

## Запуск тестов
- `pytest`                # все тесты
- `pytest -m smoke`       # быстрые проверки
- `pytest -m crud`        # только CRUD
- `pytest -m negative`    # негативные сценарии

## Locust (нагрузочное тестирование)
Запуск через терминал:
```aiignore
locust -f perf/locustfile.py --host https://restful-booker.herokuapp.com
```
После старта открой http://localhost:8089
 и задай количество пользователей + скорость.
Сценарий выполняет полный цикл: POST → GET → PUT → PATCH → DELETE с авторизацией и токеном.