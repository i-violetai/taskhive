# Base Image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
