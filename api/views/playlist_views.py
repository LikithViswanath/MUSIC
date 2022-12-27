from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from aws.dynamoDB.aws_dynamodb_operations_playlist import DynamodbPlaylistOperations
from aws.dynamoDB.aws_dynamodb_operations_users import DynamodbUserOperations
from aws.elastic_search.aws_elastic_search_operations import ElasticSearchOperations
from rest_framework import status

dynamodbPlaylistOperations = DynamodbPlaylistOperations()
dynamodbUserOperations = DynamodbUserOperations()
elasticSearchOperations = ElasticSearchOperations()


class PlaylistListView(APIView):

    @staticmethod
    def get(request):
        """
        request:{
        "user_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'PLAYLIST#' + data['user_id']

        del data['user_id']
        return Response(dynamodbPlaylistOperations.query_playlists(data))

    @staticmethod
    def post(request):
        """
        request:{
        "user_id":"",
        "song_id":"",
        "playlist_name":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'PLAYLIST#' + data['user_id']
        data['SK'] = data['playlist_name'] + '#' + data['song_id']
        print(data)

        user_data = dynamodbUserOperations.query_user_by_id({'PK': 'USER', 'SK': data['user_id']})
        song_data = elasticSearchOperations.query_by_id(data['song_id'])

        if 'artist' not in user_data['artist_list'].keys():
            user_data['artist_list'][song_data['artist']] = 1
        else:
            user_data['artist_list'][song_data['artist']] += 1

        if 'album' not in user_data['artist_list'].keys():
            user_data['album_list'][song_data['album']] = 1
        else:
            user_data['album_list'][song_data['album']] += 1

        if 'album' not in user_data['artist_list'].keys():
            user_data['genre_list'][song_data['genre']] = 1
        else:
            user_data['genre_list'][song_data['genre']] += 1

        dynamodbUserOperations.update(user_data)

        del data['user_id']
        return Response(dynamodbPlaylistOperations.insert(data))


class PlayListDetailView(APIView):

    @staticmethod
    def get(request):
        """
        request:{
        "user_id":"",
        "playlist_name":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'PLAYLIST#' + data['user_id']
        data['BEGIN_SK'] = data['playlist_name']
        del data['playlist_name']
        del data['user_id']
        return Response(dynamodbPlaylistOperations.query_playlist_by_name(data))

    @staticmethod
    def delete(request):
        """
        return:{
        "user_id":"",
        "song_id":"",
        "playlist_name":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'PLAYLIST#' + data['user_id']
        data['SK'] = data['playlist_name'] + '#' + data['song_id']

        user_data = dynamodbUserOperations.query_user_by_id({'PK': 'USER', 'SK': data['user_id']})
        song_data = elasticSearchOperations.query_by_id(data['song_id'])
        user_data['artist_list'][song_data['artist']] -= 1
        user_data['album_list'][song_data['album']] -= 1
        user_data['genre_list'][song_data['genre']] -= 1

        if user_data['artist_list'][song_data['artist']] == 0:
            del user_data['artist_list'][song_data['artist']]
        if user_data['album_list'][song_data['album']] == 0:
            del user_data['album_list'][song_data['album']]
        if user_data['genre_list'][song_data['genre']] == 0:
            del user_data['genre_list'][song_data['genre']]

        dynamodbUserOperations.update(user_data)

        del data['playlist_name']
        del data['user_id']
        del data['song_id']
        dynamodbPlaylistOperations.delete(data)
        return Response(status=status.HTTP_204_NO_CONTENT)
