# RESTful Booker — API автотесты (PyTest + Requests + Pydantic)

📌 Тестовое задание: автоматизация публичного API [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html)  
Стек: **Python 3.10+, PyTest, Requests, Pydantic, Faker**

---

## Покрытие тестов
- **CRUD** сценарии для `/booking`
- **Авторизация** `/auth` (cookie `token`)
- **Негативные сценарии**: неверные креды, действия без токена, несуществующий ID
- **Валидация JSON-схемы** через Pydantic
- **Генерация данных** через Faker
- (опционально) нагрузочное тестирование Locust

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
git clone https://github.com/<your-username>/restful-booker-tests.git
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