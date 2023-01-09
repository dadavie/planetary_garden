FROM python:3.8.6-buster
COPY main.py /main.py
COPY requirements.txt /requirements.txt
COPY get_current_plants_from_latlon.py /get_current_plants_from_latlon.py
COPY kmeans_model.sav /kmeans_model.sav
COPY scaler.save /scaler.save
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn main:app --host 0.0.0.0 --port $PORT