# 🛒 WebStore API

REST API интернет-магазина на Django REST Framework с JWT аутентификацией.

---

## 🚀 Технологии

- **Python 3.12**
- **Django 6.x**
- **Django REST Framework**
- **SimpleJWT** — JWT аутентификация
- **django-cors-headers** — CORS
- **python-decouple** — конфигурация через `.env`

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ShakH_/webstore.git
cd WebStore
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить `.env`

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
```

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

---

## 📁 Структура проекта

```
WebStore/
├── apps/
│   ├── user/           # Регистрация, аутентификация
│   ├── category/       # Категории товаров
│   └── product/        # Товары и изображения
├── WebStore/
│   ├── settings.py
│   └── urls.py
├── .env
├── manage.py
└── requirements.txt
```

---

## 🔑 Аутентификация

API использует **JWT токены**. После получения токена передавайте его в заголовке:

```
Authorization: Bearer <access_token>
```

---

## 📡 Endpoints

### Пользователи

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| `POST` | `/api/v1/user/register/` | Регистрация | Все |
| `POST` | `/api/token/` | Получить токен (логин) | Все |
| `POST` | `/api/refresh/` | Обновить токен | Все |

### Категории

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| `GET` | `/api/v1/category/` | Список категорий | Все |
| `POST` | `/api/v1/category/` | Создать категорию | Только Admin |
| `GET` | `/api/v1/category/<id>/` | Детали категории | Все |
| `PUT/PATCH` | `/api/v1/category/<id>/` | Обновить категорию | Только Admin |

### Товары

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| `GET` | `/api/v1/product/` | Список товаров | Все |
| `POST` | `/api/v1/product/` | Создать товар | Авторизованные |
| `GET` | `/api/v1/product/<id>/` | Детали товара | Все |
| `PUT/PATCH` | `/api/v1/product/<id>/` | Обновить товар | Только владелец |

#### Параметры запроса для товаров

| Параметр | Описание | Пример |
|----------|----------|--------|
| `search` | Поиск по имени и описанию | `?search=iPhone` |
| `page` | Пагинация | `?page=2` |

---

## 📦 Примеры запросов

### Регистрация

```http
POST /api/v1/user/register/
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

### Логин

```http
POST /api/token/
Content-Type: application/json

{
  "username": "john",
  "password": "securepass123"
}
```

### Создать товар

```http
POST /api/v1/product/
Authorization: Bearer <token>
Content-Type: multipart/form-data

name=Название товара (мин 10 символов)
description=Описание товара
price=99.99
category=1
images=<file1>
images=<file2>
```

> ⚠️ При создании товара обязательно минимум **2 изображения**

---

## 🔒 Права доступа

| Роль | Возможности |
|------|-------------|
| **Анонимный** | Просмотр товаров и категорий |
| **Авторизованный** | + Создание товаров |
| **Владелец товара** | + Редактирование своих товаров |
| **Admin (is_staff)** | + Управление категориями |

---

## ⚡ Настройки API

- **Пагинация**: 3 элемента на страницу
- **Троттлинг**: 10 запросов/минуту для анонимных
- **Токен доступа**: 7 день
- **Refresh токен**: 30 день
