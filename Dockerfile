FROM python:3.10


ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt /app/

# RUN pip install --no-cache-dir --no-dependencies -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/

EXPOSE 8001

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]