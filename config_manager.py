from google.cloud import storage
import json
import os

class ConfigManager:
    def __init__(self):
        self.config = None
        
        # Only require GOOGLE_APPLICATION_CREDENTIALS locally
        if os.getenv('K_SERVICE'):
            required_vars = ['GOOGLE_PROJECT_ID', 'GOOGLE_REGION']
        else:
            required_vars = ['GOOGLE_PROJECT_ID', 'GOOGLE_REGION', 'GOOGLE_APPLICATION_CREDENTIALS']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise OSError(f"Missing one or more required Google environment variables: {', '.join(missing_vars)}. Please refer to the setup guide: /guides/google.md")
        
        # Initialize the storage client
        if os.getenv('K_SERVICE'):  # K_SERVICE is set when running on Cloud Run
            # Use the default credentials (Cloud Run service account)
            self.storage_client = storage.Client(project=os.getenv('GOOGLE_PROJECT_ID'))
        else:
            # For local development, use the service account key file
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
            self.storage_client = storage.Client.from_service_account_json(credentials_path)
        
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