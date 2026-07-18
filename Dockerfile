FROM python:3.13

WORKDIR /app

ARG TestEnv

ENV TestEnv=$TestEnv

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
