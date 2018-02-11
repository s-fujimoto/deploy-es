from botocore.utils import ContainerMetadataFetcher
from botocore.session import Session
from botocore import credentials
from aws_requests_auth.aws_auth import AWSRequestsAuth
import os


def get_auth(host, region):
    credential = credentials.get_credentials(Session())
    if hasattr(credential, 'access_key'):
        return AWSRequestsAuth(aws_access_key=credential.access_key,
                               aws_secret_access_key=credential.secret_key,
                               aws_token=credential.token,
                               aws_host=host.split(':')[0],
                               aws_region=region,
                               aws_service='es')

    if os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"):
        credential = ContainerMetadataFetcher().retrieve_uri()
        return AWSRequestsAuth(aws_access_key=credential['access_key'],
                               aws_secret_access_key=credential['secret_key'],
                               aws_token=credential['token'],
                               aws_host=host.split(':')[0],
                               aws_region=region,
                               aws_service='es')

    return None


def get_region():
    region_name = Session().get_config_variable('region')
    if region_name:
        return region_name
