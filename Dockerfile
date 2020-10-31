FROM python:3.8-slim
LABEL MAINTAINER="Jonathan Villanueva frik_ej2v@hotmail.com"
WORKDIR /app/
ADD . /app/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--workers", "2", "--host", "0.0.0.0" ]