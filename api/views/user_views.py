from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from aws.dynamoDB.aws_dynamodb_operations_users import DynamodbUserOperations
from rest_framework import status

dynamodbUserOperations = DynamodbUserOperations()


class UserListView(APIView):

    @staticmethod
    def get(request):
        return Response(dynamodbUserOperations.query_users())

    @staticmethod
    def post(request):
        """
        request:{
            "name":"",
            "email":"",
            "artist_list":{},
            "genre_list":{},
            "album_list":{}
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'USER'
        data['SK'] = 'USER#' + data['name'] + '#' + data['email']
        dynamodbUserOperations.insert(data)
        return Response(data)


class UserDetailsView(APIView):
    dynamodbUserOperations = DynamodbUserOperations()

    @staticmethod
    def get(request):
        """
        request:{
            "user_id":""
        }
        """
        data = JSONParser().parse(request)
        key_data = {'PK': 'USER', 'SK': data['user_id']}
        return Response(dynamodbUserOperations.query_user_by_id(key_data))

    @staticmethod
    def put(request):
        """
        request:{
            "user_id":"",
            "artist_list":{},
            "genre_list":{},
            "album_list":{}
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'USER'
        data['SK'] = data['user_id']
        return Response(dynamodbUserOperations.update(data))

    @staticmethod
    def delete(request):
        """
        request:{
            "user_id":""
        }
        """
        data = JSONParser().parse(request)
        key_data = {'PK': 'USER', 'SK': data['user_id']}
        del data['user_id']
        dynamodbUserOperations.delete(key_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
