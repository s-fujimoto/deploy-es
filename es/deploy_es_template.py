#!/usr/bin/env python

import os
from classmethodjp.aws import get_auth
from classmethodjp.es import Elasticsearch


def main():
    es_host = os.environ['ES_HOST']
    region = os.environ.get('AWS_REGION')
    auth = get_auth(es_host, region)
    e = Elasticsearch(es_host, auth)
    e.deploy_search_template('es/search')
    e.deploy_index_template('es/index')


if __name__ == '__main__':
    main()
