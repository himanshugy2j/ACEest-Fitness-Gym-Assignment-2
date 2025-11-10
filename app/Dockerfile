# Use official Python base image
FROM python:3.11-slim


WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
ENV FLASK_APP=ACEest_Fitness.py
ENV APP_VERSION=v1.0


EXPOSE 5000
CMD ["python", "ACEest_Fitness.py"]