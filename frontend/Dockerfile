# Use an official Python runtime based on Debian 11 "bullseye" as a parent image.
FROM node:18-bullseye

# Add user that will be used in the container.
#RUN useradd treeui


# Port used by this container to serve HTTP.
EXPOSE 3000


# Use /app folder as a directory where the source code is stored.
RUN mkdir -p /app


# Copy the source code of the project into the container.
COPY . /app

# Collect static files.
#RUN python manage.py collectstatic --noinput --clear
WORKDIR "/app"
RUN npm install
RUN npm run build
#import initial data
#RUN python dataImporter.py

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; node build