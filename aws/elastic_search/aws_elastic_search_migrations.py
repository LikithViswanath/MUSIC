from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3


class ElasticSearch:
    host = 'search-music-hyvh5yeq2dekocivhftzehnfei.us-east-1.es.amazonaws.com'
    region = 'us-east-1'

    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region)
    index_name = 'songs'

    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    def create_index(self):
        return self.client.indices.create(index=self.index_name)

    def elastic_search_client(self):
        return self.client

    def create_mappings(self):
        mappings = {
            "properties": {
                "name": {"type": "text", "index": True},
                "album": {"type": "text", "index": True},
                "artist": {"type": "text", "index": True},
                "genre": {"type": "text", "index": True},
                "rating": {"type": "text", "index": True},
                "rating_num": {"type": "text", "index": True},
            }
        }
        return self.client.indices.put_mapping(index=self.index_name, body=mappings)




