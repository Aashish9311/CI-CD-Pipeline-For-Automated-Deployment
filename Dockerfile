# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy media files into the container
#COPY media /app/media/

# Copy the requirements file into the container
COPY requirements.txt .

# # Create a directory for the SQLite database inside the container
# RUN mkdir -p /app/database

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

COPY media /app/media


# Apply migrations to create tables in the database
RUN python manage.py migrate --noinput

# Expose port 8000 for Django
EXPOSE 8888

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]


