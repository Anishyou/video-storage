# ---- Base image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY app app/
COPY application-local.yml ./

# ---- Create videos directory ----
RUN mkdir -p videos


EXPOSE 8081

# ---- Start FastAPI app ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
