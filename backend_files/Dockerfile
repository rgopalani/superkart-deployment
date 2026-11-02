# Base image: slim Python
FROM python:3.10-slim

# Working directory inside the container
WORKDIR /app

# Copy all backend files (app.py, model, requirements) into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Flask runs on port 7860
EXPOSE 7860

# Start the app with gunicorn (only the last CMD in a Dockerfile takes effect)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:superkart_api"]
