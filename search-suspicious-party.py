import boto3
from bs4 import BeautifulSoup
import os
import re
import urllib.request

BUCKET_NAME = os.getenv('S3_BUCKET')

s3 = boto3.client('s3')

def get_receiving_entity_from_url(start_url):

    response = urllib.request.urlopen(
        urllib.request.Request(url=start_url, method='GET'),
        timeout=5)

    soup = BeautifulSoup(response.read(), 'html.parser')

    # Extract page title
    title = soup.title.string if soup.title else 'Untitled'

    # Extract page content for specific HTML elements
    content = ' '.join(p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']))

    content = re.sub(r'\s+', ' ', content).strip()

    s3.put_object(Body=content, Bucket=BUCKET_NAME, Key=f"docs/{title}.txt")

return content