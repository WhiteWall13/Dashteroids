# Use a base Python image
FROM python:3.10

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install system dependencies required for GDAL
RUN apt-get update && apt-get install -y libgdal-dev

# Set the working directory to /app
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy the source files into the container
COPY . /app

# Expose the port on which the Dash application is listening
EXPOSE 8050

# Command to run the Dash application
CMD ["python", "main.py"]
