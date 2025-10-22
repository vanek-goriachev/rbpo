# Тесты SimpleBlog

Этот каталог содержит все тесты для приложения SimpleBlog.

## Структура

```
tests/
├── __init__.py
├── unit/                    # Unit тесты
│   ├── __init__.py
│   ├── test_postgres_repositories.py
│   └── test_transactions.py
├── acceptance/              # Acceptance тесты
│   ├── __init__.py
│   └── test_api.py
└── README.md
```

## Типы тестов

### Unit тесты (`tests/unit/`)
- **Назначение**: Тестируют отдельные компоненты в изоляции
- **Покрытие**: Репозитории, сервисы, модели
- **Моки**: Используют моки для внешних зависимостей
- **Скорость**: Быстрые (мгновенные)

### Acceptance тесты (`tests/acceptance/`)
- **Назначение**: Тестируют API end-to-end
- **Покрытие**: HTTP endpoints, интеграция с БД
- **Зависимости**: Требуют запущенного приложения
- **Скорость**: Медленные (требуют реального API)

## Запуск тестов

### Все тесты
```bash
./run_tests.sh
```

### Только unit тесты
```bash
python3 -m pytest tests/unit/ -v
```

### Только acceptance тесты
```bash
python3 -m pytest tests/acceptance/ -v
```

### Конкретный тест
```bash
python3 -m pytest tests/unit/test_postgres_repositories.py -v
```

## Требования

### Для unit тестов
- Python 3.8+
- pytest
- Зависимости из `requirements-dev.txt`

### Для acceptance тестов
- Запущенное приложение (см. `../run_dev.sh`)
- Доступ к API на `http://localhost:8000`

## Настройка

1. Установите зависимости для разработки:
   ```bash
   pip3 install -r requirements-dev.txt
   ```

2. Запустите приложение для acceptance тестов:
   ```bash
   ./run_dev.sh
   ```

3. В другом терминале запустите тесты:
   ```bash
   ./run_tests.sh
   ```

## Покрытие тестами

### Unit тесты покрывают:
- ✅ Создание, чтение, обновление, удаление в репозиториях
- ✅ Обработку ошибок (NotFoundError, AlreadyExistsError)
- ✅ Работу с транзакциями
- ✅ Различные уровни изоляции
- ✅ Методы с внешними сессиями

### Acceptance тесты покрывают:
- ✅ Health endpoint
- ✅ CRUD операции для постов
- ✅ CRUD операции для тегов
- ✅ HTTP статус коды
- ✅ Формат ответов API

## Добавление новых тестов

### Unit тест
```python
def test_new_feature(self):
    """Тест новой функциональности"""
    # Arrange
    # Act
    # Assert
    pass
```

### Acceptance тест
```python
def test_api_endpoint():
    """Тест API endpoint"""
    response = requests.get(f"{API_BASE_URL}/endpoint")
    assert response.status_code == 200
```
