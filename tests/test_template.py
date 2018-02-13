import pytest
import os
from deployes.es import Elasticsearch
from elasticsearch.helpers import bulk


@pytest.fixture()
def es():
    es_host = os.environ['ES_HOST']
    es = Elasticsearch(es_host)
    yield es.es


class TestEs(object):

    def test_sample_query_scripts_template(self, es):
        index_name = 'testindex'
        type_name = 'type'
        test_data = [
            {'_index': index_name, '_type': type_name, '_id': '1',
             '_source': {'title': 'title 1', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '2',
             '_source': {'title': 'title 2', 'description': 'description two'}},
            {'_index': index_name, '_type': type_name, '_id': '3',
             '_source': {'title': 'title 3', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '4',
             '_source': {'title': 'title 4', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '5',
             '_source': {'title': 'title 5', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '6',
             '_source': {'title': 'noise', 'description': 'noise test'}},
        ]
        bulk(es, test_data, refresh=True)

        result = es.search_template(
            index=index_name,
            body={'id': 'sample_query', 'params': {'query': 'description'}})

        assert result['hits']['total'] == 5
        for hit in result['hits']['hits']:
            assert hit['_id'] in ['1', '2', '3', '4', '5']

        es.indices.delete(index=index_name)

    def test_indexname_index_template(self, es):
        index_name = 'indexname-yyyymmdd'
        type_name = 'type'
        test_data = [
            {'_index': index_name, '_type': type_name, '_id': '1',
             '_source': {'title': 'title 1', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '2',
             '_source': {'title': 'title 2', 'description': 'description two'}},
            {'_index': index_name, '_type': type_name, '_id': '3',
             '_source': {'title': 'title 3', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '4',
             '_source': {'title': 'title 4', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '5',
             '_source': {'title': 'title 5', 'description': 'description one'}},
            {'_index': index_name, '_type': type_name, '_id': '6',
             '_source': {'title': 'noise', 'description': 'noise test'}},
        ]
        bulk(es, test_data, refresh=True)

        result = es.indices.get(index_name)
        index_data = result[index_name]
        properties = index_data['mappings'][type_name]['properties']

        assert len(properties['title']) == 2
        assert properties['title']['type'] == 'text'
        assert properties['title']['analyzer'] == 'japanese_analyzer'
        assert len(properties['description']) == 2
        assert properties['description']['type'] == 'text'
        assert properties['description']['analyzer'] == 'japanese_analyzer'

        analysis = index_data['settings']['index']['analysis']

        assert analysis['tokenizer']['japanese_search']['type'] == 'kuromoji_tokenizer'
        assert analysis['analyzer']['japanese_analyzer']['tokenizer'] == 'japanese_search'

    def test_testindex_index_template(self, es):
        index_name = 'testindex-yyyymmdd'
        type_name = 'type'
        test_data = [
            {'_index': index_name, '_type': type_name, '_id': '1',
             '_source': {'timestamp': '2018-02-13T18:21:00+0900', 'url': 'https://classmethod.jp/1'}},
            {'_index': index_name, '_type': type_name, '_id': '2',
             '_source': {'timestamp': '2017-01-01T00:22:00+0900', 'url': 'https://classmethod.jp/2'}},
            {'_index': index_name, '_type': type_name, '_id': '3',
             '_source': {'timestamp': '2018-01-31T19:20:00+0900', 'url': 'https://classmethod.jp/3'}},
        ]
        bulk(es, test_data, refresh=True)

        result = es.indices.get(index_name)
        index_data = result[index_name]
        properties = index_data['mappings'][type_name]['properties']

        assert len(properties) == 3
        assert properties['timestamp']['type'] == 'date'
        assert properties['url']['type'] == 'keyword'
