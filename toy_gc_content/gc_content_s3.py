import boto3
from io import StringIO
from urllib.parse import urlparse

from toy_gc_content.gc_content import gc_content


def gc_content_s3(fasta_s3_url: str) -> float:
    """Calculate the GC content from a FASTA input containing DNA sequences.
    Args:
        fasta_s3_url: S3 URL of a FASTA format input with DNA sequences. Each sequence should
            have a header line starting with '>' followed by one or more lines of sequence.
        
    Returns:
        float: The GC content as a fraction (0.0 to 1.0)
        
    Raises:
        BadFastaInput: If the input is bad, e.g., no DNA sequences are found in the input
    """  
    # Create an S3 client
    s3 = boto3.client('s3')

    # Parse the S3 URL to extract bucket and key
    if fasta_s3_url.startswith('s3://'):
        parsed = urlparse(fasta_s3_url)
        bucket_name = parsed.netloc
        key = parsed.path.lstrip('/')
    elif 's3.amazonaws.com' in fasta_s3_url:
        parsed = urlparse(fasta_s3_url)
        parts = parsed.netloc.split('.')
        bucket_name = parts[0]
        key = parsed.path.lstrip('/')
    else:
        raise ValueError(f"Invalid S3 URL format: {fasta_s3_url} . Expected s3:// or https://bucket.s3.amazonaws.com/ format.")

    # Stream the file from S3 rather than downloading it, to reduce memory usage
    response = s3.get_object(Bucket=bucket_name, Key=key)
    streaming_body = response['Body']
    # Convert streaming_body into an iterable of strings (lines)
    lines = (line.decode('utf-8') for line in streaming_body.iter_lines())

    # Calculate gc_content
    return gc_content(lines)


# Include a manual test here so that we can test the code on a real S3 bucket.
# Run this file as a script like so:
# python -m gc_content.gc_content_s3
if __name__ == "__main__":
    # Example usage
    fasta_s3_url = "s3://dog-exa-1/test.fasta"
    result = gc_content_s3(fasta_s3_url)
    # Check the GC content
    expected = 0.3  # 3 GC bases out of 10 total bases
    assert abs(result - expected) < 1e-10  # pytest's way of comparing floats
