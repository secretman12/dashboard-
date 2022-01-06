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

COPY --chown=appuser:appuser app/requirements.txt .

RUN pip install gunicorn
RUN pip install mysqlclient
RUN pip install mysql-connector-python

RUN pip install -r requirements.txt

# copy app
COPY --chown=appuser:appuser app/ ./
  
CMD [ "gunicorn", "--workers=5", "--threads=2", "-b 0.0.0.0:80", "app:server"]