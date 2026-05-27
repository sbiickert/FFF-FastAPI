FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn[standard] \
    sqlalchemy pymysql python-dotenv pydantic[email] \
    aiomysql python-jose[cryptography] \
    python-multipart bcrypt

# Adjust if you have a requirements.txt
# RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]