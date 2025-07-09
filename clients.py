import httpx
import os

v1_client = httpx.Client(base_url=os.getenv('SONARCLOUD_HOST', 'https://sonarcloud.io/api/'),
                         headers={'Authorization': 'Bearer ' + os.environ['SONARQUBE_TOKEN']})
v2_client = httpx.Client(base_url=os.getenv('SONARCLOUD_API_HOST', 'https://api.sonarcloud.io/'),
                         headers={'Authorization': 'Bearer ' + os.environ['SONARQUBE_TOKEN']})