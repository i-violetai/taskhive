# Image Processing App

### Note

This task-based approach can easily be swapped with more complex image transformations. In cases where image processing is resource-intensive(e.g. processing with ML/DL models, batch image processing, video processing), the task-based approach allows  to efficiently manage workload distribution and failure recovery.

This project allows users to upload an image, convert it to greyscale, then blur using Celery, and then view the processed image. The application is built using Django and utilizes Redis as a message broker for Celery tasks.


## Setup Instructions

### 1. **Clone the repository and run Docker Compose**:
   Clone the repository and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Project Workflow

### 2. **Asynchronous Processing with Celery**
   - Once the image is uploaded, Celery tasks are triggered.
   - These tasks run in chain in the background and process the image by converting it to greyscale and then blurs the image.

### Benefits of Task-based Approach

1. **Asynchronous Execution**: Offloading processing to background workers ensures the main application remains responsive.
2. **Scalability**: Celery can distribute tasks across multiple workers, allowing the system to scale.
3. **Failure Handling**: Tasks can be retried automatically in case of failure (e.g., if the image processing fails).
4. **Long-running Task Isolation**: Separates image processing from the main flow, ensuring that users are not waiting for long operations to complete.
 