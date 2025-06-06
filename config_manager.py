from google.auth import compute_engine
from google.cloud import storage
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self):
        self.config = None

        logger.info(f"Setting up config manager")
        
        # Check for required project variables
        required_vars = ['GOOGLE_PROJECT_ID', 'GOOGLE_REGION', 'GOOGLE_APPLICATION_CREDENTIALS']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise OSError(f"Missing one or more required Google environment variables: {', '.join(missing_vars)}")
        
        # Get credentials for a specific service account
        credentials = compute_engine.Credentials(
            service_account_email=os.getenv('SERVICE_ACCOUNT')
        )

        # Initialize client with these credentials
        logger.info(f"Initializing storage client for project: {os.getenv('PROJECT_ID')}")
        self.storage_client = storage.Client(
            project=os.getenv('PROJECT_ID'),
            credentials=credentials
        )
        
        self.bucket_name = os.getenv('CONFIG_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("CONFIG_BUCKET_NAME environment variable is not set")
        self.bucket = self.storage_client.bucket(self.bucket_name)
        self.blob = self.bucket.blob('config.json')
        # Load initial config
        self.refresh_config()
    
    def refresh_config(self):
        """Manually refresh the config from GCS"""
        try:
            # Get a fresh blob reference without generation
            self.blob = self.bucket.blob('config.json')
            config_data = self.blob.download_as_string()
            self.config = json.loads(config_data)
            return True, "Config refreshed successfully"
        except Exception as e:
            error_msg = f"Error refreshing config: {str(e)}"
            print(error_msg)
            return False, error_msg

    def get_config(self):
        """Get the current config"""
        if self.config is None:
            success, _ = self.refresh_config()
            if not success:
                raise RuntimeError("Failed to load config")
        return self.config 