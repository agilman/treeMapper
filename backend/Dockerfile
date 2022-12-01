# Use an official Python runtime based on Debian 11 "bullseye" as a parent image.
FROM python:3.11-bullseye

# Add user that will be used in the container.
RUN useradd treeuser


# Port used by this container to serve HTTP.
EXPOSE 8000


# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000


# Install the application server.
RUN pip install waitress

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt


# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown treeuser:treeuser /app


# Copy the source code of the project into the container.
COPY --chown=treeuser:treeuser . .

# Use user "treeuser" to run the build commands below and the server itself.
USER treeuser


# Collect static files.
#RUN python manage.py collectstatic --noinput --clear

#import initial data
RUN python manage.py migrate
RUN python dataImporter.py

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; waitress-serve --listen="0.0.0.0:8000" treeMapperAPI.wsgi:application