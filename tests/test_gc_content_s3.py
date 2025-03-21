import boto3
from moto import mock_aws
import pytest
import warnings

@mock_aws
def test_gc_content_s3():

    # Suppress an annoying DeprecationWarning from botocore
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)

        # Create a mock S3 bucket and upload a test FASTA file
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        key = 'test.fasta'
        
        # Create the bucket
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload a test FASTA file
        fasta_content = ">test_sequence\nGCCAAAT\nTTT\n"
        s3.put_object(Bucket=bucket_name, Key=key, Body=fasta_content)
        
        # Construct the S3 URL
        s3_url = f"s3://{bucket_name}/{key}"
        
        # Call the gc_content_s3 function
        from toy_gc_content.gc_content_s3 import gc_content_s3
        result = gc_content_s3(s3_url)
        
        # Check the GC content
        expected = 0.3  # 3 GC bases out of 10 total bases
        assert abs(result - expected) < 1e-10  # pytest's way of comparing floats
