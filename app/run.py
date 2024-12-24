import os
import webbrowser
import time

# Define Docker Compose commands
DOCKER_COMPOSE_UP = "docker-compose up --build -d"
DOCKER_COMPOSE_DOWN = "docker-compose down"

# URLs to open
urls = [
    "http://localhost:5000/browser/",
]

# Function to run a shell command


def run_command(command):
    print(f"Running: {command}")
    result = os.system(command)
    if result != 0:
        print(f"Command failed: {command}")
    else:
        print(f"Command succeeded: {command}")


# Start Docker Compose
run_command(DOCKER_COMPOSE_DOWN + "&&" + DOCKER_COMPOSE_UP)

# Wait for services to start
print("Waiting for services to start...")
time.sleep(30)  # Adjust this time as needed based on your services

# Open URLs in Chrome
for url in urls:
    print(f"Opening URL: {url}")
    webbrowser.open(url)

# Provide user instructions
print("Services are up and URLs opened. Run the following command to stop Docker Compose:")
print(DOCKER_COMPOSE_DOWN)
