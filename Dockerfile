FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY frontend/ frontend/
COPY .streamlit/ .streamlit/

EXPOSE 8000

CMD ["sh", "-c", "(cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000) & streamlit run frontend/streamlit_app.py --server.address=0.0.0.0 --server.port ${PORT:-8501}"]
