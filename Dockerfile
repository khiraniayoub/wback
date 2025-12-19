FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /home/wback

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/home/src
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Copy the project into the image
RUN mkdir /home/wback/staticfiles
RUN mkdir /home/wback/logs
COPY wback/ /home/wback/
COPY pyproject.toml uv.lock /home/
COPY scripts/ /home/scripts/
RUN chmod +x /home/scripts/entrypoint.sh

# Install dependencies using uv
WORKDIR /home
RUN uv sync
WORKDIR /home/wback

# create the app user
RUN groupadd -r app
RUN useradd -g app app

# Set permissions for the app user
RUN chown -R app:app /home/
USER app

# Expose port
EXPOSE 8000

CMD ["/bin/sh", "-c", "/home/scripts/entrypoint.sh && uv run gunicorn wback.asgi:application --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker --workers 4 --reload"]
