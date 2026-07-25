# RAG Production Setup

Production-ready RAG (Retrieval-Augmented Generation) система для вопросно-ответных задач по документам.

## Архитектура
- **Векторная БД**: Qdrant для хранения эмбеддингов
- **Реляционная БД**: PostgreSQL для метаданных
- **Оркестрация**: Docker Compose
- **Миграции**: Alembic

## Компоненты
1. Ingestion pipeline — загрузка и чанкинг документов
2. Embedding generation — генерация эмбеддингов (модель X)
3. Retrieval — поиск релевантных чанков в Qdrant
4. Generation — LLM для генерации ответа

## Быстрый старт
\`\`\`bash
docker-compose up -d
python app/main.py
\`\`\`