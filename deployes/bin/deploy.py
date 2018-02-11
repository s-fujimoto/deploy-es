#!/usr/bin/env python

import os
from deployes.aws import get_auth, get_region
from deployes.es import Elasticsearch


def main():
    es_host = os.environ['ES_HOST']
    region = get_region()
    auth = get_auth(es_host, region)
    e = Elasticsearch(es_host, auth)
    e.deploy_script_template('settings/script')
    e.deploy_index_template('settings/index')


if __name__ == '__main__':
    main()
