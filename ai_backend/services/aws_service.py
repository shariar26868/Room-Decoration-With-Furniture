"""
AWS S3 Service
==============
Handle file uploads to S3 (without ACL)
"""

import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class AWSService:
    """AWS S3 file upload service"""
    
    def __init__(self, access_key: str, secret_key: str, bucket: str, region: str):
        self.bucket_name = bucket
        self.region = region
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
    
    def upload_file(self, file_path: str, object_name: str) -> str:
        """
        Upload file to S3 bucket (without ACL)
        
        Args:
            file_path: Local file path
            object_name: S3 object name (key)
        
        Returns:
            Public URL of uploaded file
        """
        try:
            # Determine content type
            content_type = 'image/jpeg'
            if file_path.endswith('.png'):
                content_type = 'image/png'
            
            # Upload file WITHOUT ACL (modern S3 buckets)
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs={
                    'ContentType': content_type
                    # Removed 'ACL': 'public-read' - causes the error
                }
            )
            
            # Construct public URL
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_name}"
            
            logger.info(f"✅ Uploaded: {object_name}")
            
            return url
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            logger.error(f"❌ S3 upload failed [{error_code}]: {error_msg}")
            raise Exception(f"Failed to upload to S3: {error_msg}")
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            raise Exception(f"Failed to upload file: {str(e)}")


# Global instance
_aws_instance = None


def init_aws_service(access_key: str, secret_key: str, bucket: str, region: str):
    """Initialize AWS service"""
    global _aws_instance
    _aws_instance = AWSService(access_key, secret_key, bucket, region)
    return _aws_instance


def get_aws_service() -> AWSService:
    """Get AWS service instance"""
    if _aws_instance is None:
        raise RuntimeError("AWS service not initialized")
    return _aws_instance