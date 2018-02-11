import elasticsearch
import os
import json


class Elasticsearch(object):

    es = None

    def __init__(self, es_host, auth=None):
        if auth:
            self.es = elasticsearch.Elasticsearch(hosts=[es_host],
                                                  connection_class=elasticsearch.RequestsHttpConnection,
                                                  http_auth=auth)
        else:
            self.es = elasticsearch.Elasticsearch(hosts=[es_host])

    def get_template(self, template_dir):
        template = {}
        os.getcwd()
        files = os.listdir(template_dir)
        for file_name in files:
            template['{}/{}'.format(template_dir, file_name)] = file_name.rstrip('.json')
        return template

    def deploy_script_template(self, script_template_dir):
        script_template = self.get_template(script_template_dir)
        for path, name in script_template.items():
            with open(path) as f:
                body = json.load(f)
                self.es.put_script(id=name, body=body)

    def deploy_index_template(self, index_template_dir):
        index_template = self.get_template(index_template_dir)
        for path, name in index_template.items():
            with open(path) as f:
                body = json.load(f)
                self.es.indices.put_template(name=name, body=body)
