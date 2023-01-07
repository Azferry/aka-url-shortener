# FROM mcr.microsoft.com/appsvc/python:latest


# #WORKDIR /app
# COPY . /opt/app

# RUN pip install --no-cache-dir -r requirements.txt

# # ENV PORT 8080
# # EXPOSE 8080
# EXPOSE 5000

# ENTRYPOINT ["gunicorn", "--timeout", "600", "--access-logfile", "'-'", "--error-logfile", "'-'", "--chdir=/opt/app", "app:app"]

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install default-libmysqlclient-dev gcc -y
RUN apt-get install unixodbc-dev gnupg2 curl -y

## DB Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# RUN apt-get update
# RUN apt-get install odbcinst1debian2 libodbc1 -y
# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# # optional: for bcp and sqlcmd
# RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
# RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# ENTRYPOINT ["gunicorn", "--timeout", "600", "--access-logfile", "'-'", "--error-logfile", "app.main:app"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000","app.main:app"]
CMD ["/bin/sh"]

