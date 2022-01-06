FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# set user:group
RUN groupadd appuser && useradd -g users -G appuser appuser  --home /usr/src/app

# change permission on workdir
RUN chown -R appuser:appuser /usr/src/app


USER appuser:appuser
ENV PATH=$PATH:/usr/src/app/.local/bin

# install dependencies
RUN pip install --upgrade pip

COPY --chown=appuser:appuser requirements.txt .

RUN pip install -r requirements.txt 

ENV FLASK_APP=app.py

COPY --chown=appuser:appuser app.py .

ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD ["app.py"]

#CMD ["app.py", "run", "--host", "0.0.0.0"]
