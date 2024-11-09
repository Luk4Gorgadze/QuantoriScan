FROM python:3.10

# Install netcat for database checking
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /luka

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Make the start script executable
COPY start.sh .
RUN chmod +x start.sh

# Use the start script as the entry point
CMD ["./start.sh"]