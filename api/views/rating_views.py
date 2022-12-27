from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from aws.dynamoDB.aws_dynamodb_operations_rating import DynamodbRatingOperations
from rest_framework import status

dynamodbRatingOperations = DynamodbRatingOperations()


class RatingListView(APIView):

    @staticmethod
    def get(request):
        """
        request:{
          "user_id":""
        }
        """
        data = JSONParser().parse(request)
        print(data)
        data['PK'] = 'RATING#'+data['user_id']
        del data['user_id']
        return Response(dynamodbRatingOperations.query_ratings(data))

    @staticmethod
    def post(request):
        """
        request:{
        "song_id":"",
        "user_id":"",
        "rating":"",
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RATING#' + data['user_id']
        data['SK'] = data['song_id']
        del data['user_id']
        del data['song_id']
        dynamodbRatingOperations.insert(data)
        return Response(data)


class RatingDetailView(APIView):

    @staticmethod
    def get(request):
        """
        request: {
        "user_id":""
        "song_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RATING#' + data['user_id']
        data['SK'] = data['song_id']
        del data['user_id']
        del data['song_id']
        return Response(dynamodbRatingOperations.query_rating_by_id(data))

    @staticmethod
    def put(request):
        """
        request:{
        "song_id":"",
        "user_id":"",
        "rating":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RATING#' + data['user_id']
        data['SK'] = data['song_id']
        del data['user_id']
        del data['song_id']
        print(data)
        return Response(dynamodbRatingOperations.update(data))

    @staticmethod
    def delete(request):
        """
        request{
          "user_id":"",
          "song_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RATING#' + data['user_id']
        data['SK'] = data['song_id']
        del data['user_id']
        del data['song_id']
        dynamodbRatingOperations.delete(data)
        return Response(status=status.HTTP_204_NO_CONTENT)



