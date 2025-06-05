# llm-comparator

TODO: I need to update all of this. It's GitHub Copilot-generated.

## Setup and Run the App Locally

1. Clone the repository:
    ```sh
    git clone https://github.com/gallimorej/llm-comparator.git
    cd llm-comparator
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add the following environment variables:
    ```sh
    DOCKER_IMAGE=your_docker_image_name
    DOCKER_CONTAINER=your_docker_container_name
    PORT=your_port_number
    PROJECT_ID=your_google_cloud_project_id
    APP_NAME=your_app_name
    REGION=your_google_cloud_region
    REACT_APP_OPENAI_API_KEY=your_openai_api_key
    REACT_APP_ANTHROPIC_API_KEY=your_anthropic_api_key
    SERVICE_ACCOUNT=your_google_cloud_service_account
    SLACK_TOKEN=your_slack_token (if applicable)
    CONFIG_BUCKET_NAME=your_google_cloud_storage_bucket_name  # Name of the GCS bucket where config.json is stored
    ```

5. Run the Flask app:
    ```sh
    python app.py
    ```

6. Open your web browser and go to `http://127.0.0.1:5000` to access the app.

## Build and Deploy the App using Docker and Google Cloud Run

1. Build the Docker image:
    ```sh
    docker build -t gcr.io/[PROJECT_ID]/[IMAGE_NAME] .
    ```

2. Push the Docker image to Google Container Registry:
    ```sh
    docker push gcr.io/[PROJECT_ID]/[IMAGE_NAME]
    ```

3. Deploy the container to Google Cloud Run:
    ```sh
    gcloud run deploy [SERVICE_NAME] --image gcr.io/[PROJECT_ID]/[IMAGE_NAME] --platform managed --region [REGION] --allow-unauthenticated
    ```

4. Retrieve the service URL:
    ```sh
    gcloud run services describe [SERVICE_NAME] --platform managed --region [REGION] --format "value(status.url)"
    ```

5. Open the service URL in your web browser to access the deployed app.
