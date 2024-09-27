# Use an official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the new requirements file
COPY new_req.txt .

# Install Python dependencies from new_req.txt
RUN pip install --upgrade pip && pip install -r new_req.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
