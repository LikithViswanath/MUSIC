from aws.elastic_search.aws_elastic_search_migrations import ElasticSearch


class ElasticSearchOperations:
    """
    song_id:,
    name:,
    genre:,
    artist:,
    album:,
    rating:,
    rating_num:,
    """
    index_name = 'songs'
    client = ElasticSearch().elastic_search_client()

    def get_index(self):
        return self.client.indices.get_mapping()

    def insert(self, data):
        return self.client.index(index=self.index_name, id=data['song_id'], body=data)

    def delete(self, data):
        return self.client.delete(index=self.index_name, id=data['song_id'])

    def query_by_id(self, song_id):
        response = self.client.get(index=self.index_name, id=song_id)
        return response['_source']

    def query_all(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        response = self.client.search(index=self.index_name, body=query)
        return response['hits']['hits']

    def query(self, search_string):
        prefix_query = {
            'query': {
                'bool': {
                    'should': [
                        {'prefix': {'name': search_string}},
                        {'prefix': {'genre': search_string}},
                        {'prefix': {'album': search_string}},
                        {'prefix': {'artist': search_string}}
                    ]
                }
            }
        }

        fuzzy_query = {
            'query': {
                'bool': {
                    'should': [
                        {'fuzzy': {'name': search_string}},
                        {'fuzzy': {'genre': search_string}},
                        {'fuzzy': {'album': search_string}},
                        {'fuzzy': {'artist': search_string}}
                    ]
                }
            }
        }

        prefix_query_res = self.client.search(index=self.index_name, body=prefix_query, ignore=400)
        fuzzy_query_res = self.client.search(index=self.index_name, body=fuzzy_query, ignore=400)

        res = {}

        if 'hits' in prefix_query_res['hits'].keys():
            for x in prefix_query_res['hits']['hits']:
                res[x['_source']['song_id']] = {'score': x['_score'], 'data': x['_source']}
        else:
            res[prefix_query_res['hits']['song_id']] = {
                'score': prefix_query_res['hits']['_score'],
                'data': prefix_query_res['hits']['_source']
            }

        if 'hits' in fuzzy_query_res['hits'].keys():
            for x in fuzzy_query_res['hits']['hits']:
                res[x['_source']['song_id']] = {'score': x['_score'], 'data': x['_source']}
        else:
            res[prefix_query_res['hits']['song_id']] = {
                'score': fuzzy_query_res['hits']['_score'],
                'data': fuzzy_query_res['hits']['_source']
            }

        result = []

        for x in res.values():
            result.append(x)

        return result

    def recommendation(self, data):
        print(list(data['genre_list'].keys()), list(data['album_list'].keys()), list(data['artist_list'].keys()))
        query = {
            'query': {
                'bool': {
                    'should': [
                        {'terms': {'genre.keyword': list(data['genre_list'].keys())}},
                        {'terms': {'album.keyword': list(data['album_list'].keys())}},
                        {'terms': {'artist.keyword': list(data['artist_list'].keys())}}
                    ]
                }
            }
        }
        response = self.client.search(index=self.index_name, body=query, ignore=400)
        return response['hits']

    def bucket_aggregations(self):
        query = {
            'aggs': {
                'playlists': {
                    'terms': {'field': 'album.keyword'}
                }
            }
        }
        return self.client.search(index=self.index_name, body=query, ignore=400)
