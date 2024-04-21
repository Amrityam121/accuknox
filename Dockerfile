# Use an official Python runtime as a parent image
FROM  python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY ./ ./

WORKDIR /app/myproject/


# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

