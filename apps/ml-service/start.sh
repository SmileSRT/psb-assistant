#!/bin/bash

# Build and start the services
docker-compose up --build -d

# Wait for the service to be ready
echo "Waiting for the service to start..."
sleep 10

# Check if the service is running
curl http://localhost:8000/
if [ $? -eq 0 ]; then
    echo "Service is running successfully!"
    echo "API documentation is available at http://localhost:8000/docs"
else
    echo "Service failed to start. Check docker logs for more information:"
    docker-compose logs
fi 