# Setup Guide

Follow these steps to set up the project:

## Prerequisites
- Clone the repository:

    ```bash
    git clone git@github.com:AtharvBhujbal/medigenie.git
    cd medigenie
    ```

## Installation
1. Create python enviornment
    ```bash
    pip install virtualenv
    python3 -m venv .venv
    source .venv/bin/activate
    ```
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set up environment variables:
    - Copy the `.env.example` file to `app/.env`:
      ```bash
      cp .env.example app/.env
      ```
    - Update the `.env` file with your configuration.

## Database Setup
1. Create Medigenie database:
    ```bash
    psql -U postgres -W -c "CREATE DATABASE medigenie;"
    ```
2. Initialize the database:

    ```bash
    python3 setup_db.py
    ```

## Running the Application
- Start the development server:

    ```bash
    python3 run.py
    ```

## Testing

- Use Postman's [collection](https://atharvbhujbal.postman.co/workspace/Atharv-Bhujbal's-Workspace~349517e4-4b00-4422-8e36-9e5c17935361/collection/44363547-e98c53ff-51d2-4c84-8a87-1afbc544b977?action=share&creator=44363547) for API testing