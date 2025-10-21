#!/usr/bin/env python3
"""
Скрипт для тестирования API SimpleBlog
"""
import sys
import time

import requests

# Конфигурация
API_BASE_URL = "http://localhost:8000"
MAX_RETRIES = 30
RETRY_DELAY = 2


def wait_for_api():
    """Ждем, пока API станет доступным"""
    print("⏳ Ожидаем запуска API...")

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API доступно!")
                return True
        except requests.exceptions.RequestException:
            pass

        print(f"   Попытка {attempt + 1}/{MAX_RETRIES}...")
        time.sleep(RETRY_DELAY)

    print("❌ API не стало доступным за отведенное время")
    return False


def test_health_endpoint():
    """Тестируем health endpoint"""
    print("\n🔍 Тестируем health endpoint...")

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


def test_post_creation():
    """Тестируем создание поста"""
    print("\n📝 Тестируем создание поста...")

    post_data = {
        "title": "Тестовый пост",
        "body": "Это тестовый пост для проверки API",
        "status": "draft",
    }

    try:
        response = requests.post(f"{API_BASE_URL}/posts", json=post_data)
        print(f"   Статус: {response.status_code}")

        if response.status_code == 201:
            post = response.json()
            print(f"   ✅ Пост создан: {post['title']} (ID: {post['id']})")
            return post
        else:
            print(f"   ❌ Ошибка создания поста: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


def test_post_retrieval(post_id):
    """Тестируем получение поста"""
    print(f"\n📖 Тестируем получение поста {post_id}...")

    try:
        response = requests.get(f"{API_BASE_URL}/posts/{post_id}")
        print(f"   Статус: {response.status_code}")

        if response.status_code == 200:
            post = response.json()
            print(f"   ✅ Пост получен: {post['title']}")
            return post
        else:
            print(f"   ❌ Ошибка получения поста: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


def test_post_list():
    """Тестируем получение списка постов"""
    print("\n📋 Тестируем получение списка постов...")

    try:
        response = requests.get(f"{API_BASE_URL}/posts")
        print(f"   Статус: {response.status_code}")

        if response.status_code == 200:
            posts = response.json()
            print(f"   ✅ Получено постов: {len(posts)}")
            return posts
        else:
            print(f"   ❌ Ошибка получения списка постов: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


def test_post_tag_creation():
    """Тестируем создание тега"""
    print("\n🏷️ Тестируем создание тега...")

    tag_data = {"name": "тест"}

    try:
        response = requests.post(f"{API_BASE_URL}/post-tags", json=tag_data)
        print(f"   Статус: {response.status_code}")

        if response.status_code == 201:
            tag = response.json()
            print(f"   ✅ Тег создан: {tag['name']} (ID: {tag['id']})")
            return tag
        else:
            print(f"   ❌ Ошибка создания тега: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


def test_post_tag_list():
    """Тестируем получение списка тегов"""
    print("\n🏷️ Тестируем получение списка тегов...")

    try:
        response = requests.get(f"{API_BASE_URL}/post-tags")
        print(f"   Статус: {response.status_code}")

        if response.status_code == 200:
            tags = response.json()
            print(f"   ✅ Получено тегов: {len(tags)}")
            return tags
        else:
            print(f"   ❌ Ошибка получения списка тегов: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование API SimpleBlog")
    print("=" * 50)

    # Ждем запуска API
    if not wait_for_api():
        sys.exit(1)

    # Тестируем health endpoint
    if not test_health_endpoint():
        print("❌ Health endpoint не работает")
        sys.exit(1)

    # Тестируем создание поста
    post = test_post_creation()
    if not post:
        print("❌ Создание поста не работает")
        sys.exit(1)

    # Тестируем получение поста
    if not test_post_retrieval(post["id"]):
        print("❌ Получение поста не работает")
        sys.exit(1)

    # Тестируем получение списка постов
    if not test_post_list():
        print("❌ Получение списка постов не работает")
        sys.exit(1)

    # Тестируем создание тега
    tag = test_post_tag_creation()
    if not tag:
        print("❌ Создание тега не работает")
        sys.exit(1)

    # Тестируем получение списка тегов
    if not test_post_tag_list():
        print("❌ Получение списка тегов не работает")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 Все тесты прошли успешно!")
    print("✅ API работает корректно")
    print(f"🌐 API доступно по адресу: {API_BASE_URL}")
    print(f"📚 Документация: {API_BASE_URL}/docs")


if __name__ == "__main__":
    main()
