import json
import os

import pytest

from app.cloudfoundry_config import extract_cloudfoundry_config


@pytest.fixture
def vcap_services():
    return {
        'aws-elasticache-redis': [{
            'credentials': {
                'uri': 'redis://xxx:6379'
            }
        }],
        's3': [
            {
                'name': 'notifications-api-csv-upload-bucket-test',
                'credentials': {
                    'access_key_id': 'csv-access',
                    'bucket': 'csv-upload-bucket',
                    'secret_access_key': 'csv-secret'
                }
            },
            {
                'name': 'notifications-api-contact-list-bucket-test',
                'credentials': {
                    'access_key_id': 'contact-list-access',
                    'bucket': 'contact-list-bucket',
                    'secret_access_key': 'contact-list-secret'
                }
            }
        ],
    }


def test_extract_cloudfoundry_config_populates_other_vars(os_environ, vcap_services):
    os.environ['DEPLOY_ENV'] = 'test'
    os.environ['VCAP_SERVICES'] = json.dumps(vcap_services)
    extract_cloudfoundry_config()

    assert os.environ['REDIS_URL'] == 'rediss://xxx:6379'
    assert os.environ['CSV_UPLOAD_BUCKET_NAME'] == 'csv-upload-bucket'
    assert os.environ['CONTACT_LIST_BUCKET_NAME'] == 'contact-list-bucket'
