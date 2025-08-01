FROM python:3.9-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем конфигурацию Streamlit
COPY .streamlit/ .streamlit/

# Копируем код приложения
COPY main.py .

# Открываем порт
EXPOSE 8501

# Команда запуска
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
