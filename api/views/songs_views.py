from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from aws.elastic_search.aws_elastic_search_operations import ElasticSearchOperations

elasticSearchOperations = ElasticSearchOperations()


class Aggregation(APIView):

    @staticmethod
    def get(request):
        return Response(elasticSearchOperations.bucket_aggregations())


class AutoRecommendation(APIView):

    @staticmethod
    def get(request):
        """
        request:{
        "PK": "USER",
        "SK": "USER#name#email",
        "name":"",
        "email":"",
        "artist_list": {}
        "album_list": {}
        "genre_list": {}
        }
        """
        data = JSONParser().parse(request)
        return Response(elasticSearchOperations.recommendation(data))


class SongsListView(APIView):

    @staticmethod
    def get(request):
        return Response(elasticSearchOperations.query_all())

    @staticmethod
    def put(request):
        """
        request:{
        "song_id":"",
        "name":"",
        "genre":"",
        "artist":"",
        "album":"",
        "rating":"",
        "rating_num":"",
        }
        """
        data = JSONParser().parse(request)
        return Response(elasticSearchOperations.insert(data))


class SongsDetailView(APIView):

    @staticmethod
    def get(request):
        """
        request:{
        "search_string":""
        }
        """
        data = JSONParser().parse(request)
        return Response(elasticSearchOperations.query(data['search_string']))

    @staticmethod
    def delete(request):
        """
        request:{
        "id":""
        }
        """
        data = JSONParser().parse(request)
        return Response(elasticSearchOperations.query(data['id']))
