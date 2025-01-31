# Рекомендательная система

## Описание проекта
Проект представляет собой рекомендательную систему, разработанную с использованием Python, библиотеки CatBoost и других инструментов. Система предсказывает вероятности для двух классов (например, положительный/отрицательный отклик на рекомендацию) на основе данных о пользователях и их взаимодействиях с сервисом.

## Технологии
- **Язык программирования:** Python
- **Библиотека машинного обучения:** CatBoost
- **Среда разработки:** Jupyter Notebook, VS Code
- **Инструменты:** FastAPI, SQLAlchemy, PostgreSQL, Pandas, NumPy, scikit-learn, Matplotlib, GridSearchCV, CatBoost, git, uvicorn, psycopg, requests

## Результаты модели
Модель была обучена на тренировочном наборе данных и протестирована на тестовом наборе. Оценка качества модели измерялась с использованием метрик для классификации:
F-мера

- **Результаты на тесте:**  
  - Класс 1: 0.85  
  - Класс 2: 0.28  

- **Результаты на тренировочном наборе:**  
  - Класс 1: 0.85  
  - Класс 2: 0.31  

## Описание данных
Данные содержат информацию о пользователях и их взаимодействиях с сервисом. Признаки включают различные характеристики пользователей и постов. Целевая переменная представляет собой бинарную классификацию, где нужно предсказать отклик пользователя на рекомендацию.

## Структура проекта
1. **Обработка данных:** Обработка вещественных и категориальных признаков.
2. **Обучение модели:** Использование CatBoost для обучения модели классификации.
3. **Оценка модели:** Вычисление метрик качества на тестовых и тренировочных данных.
4. **Интерфейс:** Реализация сервиса на Python для интеграции модели в систему рекомендаций.

## Примечания
Здесь пропущен подбор гиперпараметров с помощью GridSearch. 
Проект все еще не закончен, из-за этого у него плохая архитектура и много лишних файлов
