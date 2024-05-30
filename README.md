# SMS Microservice for Automated Delivery

## Project Overview

This project is a microservice designed to facilitate the automated sending of SMS messages directly from our business software. It includes a daemon that continuously monitors the database for new SMS entries and sends them using the Digital Virgo API. The primary focus is on ensuring high availability, meaning the system is built to handle errors gracefully without disrupting the overall service.

## Key Features

- **Automated SMS Sending**: The microservice automates the process of sending SMS messages as soon as they are recorded in the database.
- **Digital Virgo API Integration**: Uses Digital Virgo's API for reliable and efficient SMS delivery.
- **High Availability**: Designed to ensure that any errors are isolated and do not cause the entire system to fail.
- **Error Handling and Logging**: Includes robust error handling and logging mechanisms to track issues without interrupting service.

## How It Works

1. **Database Monitoring**:
   - A daemon runs continuously to monitor a specified database for any new SMS entries.
   - When a new SMS is detected, it is immediately queued for sending.

2. **SMS Sending**:
   - The queued SMS messages are sent using the Digital Virgo API.
   - The system logs the status of each message (sent, failed, etc.).

3. **Error Handling**:
   - Errors encountered during SMS sending are logged and managed without stopping the daemon.
   - Includes retry mechanisms for transient errors to enhance reliability.

## High Availability Design

- **Isolation of Errors**: The microservice ensures that individual errors do not cascade and affect the entire system.
- **Graceful Degradation**: If a part of the system fails, the service continues to run, possibly with reduced functionality, until the issue is resolved.
- **Monitoring and Alerts**: Implements monitoring tools to track the health and performance of the microservice and alert the team in case of failures.

## Technologies Used

- **Python**: The main programming language used for developing the microservice.
- **Digital Virgo API**: For sending SMS messages.
- **Database**: Compatible with MySQL, PostgreSQL, or other SQL databases.
- **Docker**: Used for containerizing the microservice to ensure consistent environments across different stages of deployment.
- **Logging and Monitoring Tools**: To ensure robust error tracking and system monitoring.

## Conclusion

This microservice is a robust solution for automating SMS sending from our business software, emphasizing high availability and reliability. By integrating with the Digital Virgo API and employing a resilient architecture, it ensures seamless and continuous operation even in the face of individual component failures.
