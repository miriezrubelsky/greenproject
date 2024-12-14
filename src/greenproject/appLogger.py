import logging

import base64
from elasticsearch import Elasticsearch
from python_elastic_logstash import ElasticHandler, ElasticFormatter
import sys
import os
from urllib.parse import urlparse

class AppLogger():

    def __init__(self):

        self.logger = logging.getLogger('python-elastic-logstash')
        self.logger.setLevel(logging.DEBUG)

        elasticsearch_endpoint = os.getenv('ES_HOST', 'http://localhost:9200')

        #elasticsearch_endpoint = 'http://node01:9200'
        token = base64.b64encode(b'elastic:12345')

        # Example of creating an index manually (if required)
        parsed_url = urlparse(elasticsearch_endpoint)
        self.logger.info(f"Connecting to Elasticsearch with the following parameters: scheme={parsed_url.scheme}, host={parsed_url.hostname}, port={parsed_url.port}")

        es = Elasticsearch([{'scheme': parsed_url.scheme, 'host': parsed_url.hostname, 'port': parsed_url.port}])

        #es = Elasticsearch([{'scheme': 'http', 'host': 'node01', 'port': 9200}])
       # es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        index_name = 'green-project'

        # Create an index if it does not exist
        if not es.indices.exists(index=index_name):
              es.indices.create(index=index_name)

        elastic_handler = ElasticHandler(elasticsearch_endpoint,token=token.decode('ascii'),elastic_index=index_name)
        elastic_handler.setFormatter(ElasticFormatter())

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(elastic_handler)
        self.logger.addHandler(console_handler)

        extra = {
          'elastic_fields': {
          'version': 'python version: ' + repr(sys.version_info),
          'value' : 42
           }
          
        }

        

        self.logger.debug("Python elastic logstash configured", extra=extra)

    def getLogger(self):
        return self.logger







