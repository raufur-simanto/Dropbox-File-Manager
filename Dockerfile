### official base image
FROM python:3.10-alpine

## Set working directory
WORKDIR /usr/src/app

### Install system dependencies
RUN apk update && apk add --no-cache python3-dev py3-pip


### set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

### Install necessary dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "manage:app"]
