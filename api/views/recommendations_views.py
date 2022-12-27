from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from aws.dynamoDB.aws_dynamodb_operations_recommendations import DynamodbRecommendationsOperations
from rest_framework import status

dynamodbRecommendationsOperations = DynamodbRecommendationsOperations()


class RecommendationsListView(APIView):

    @staticmethod
    def get(request):
        """
        request:{
        "user_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RECOMMENDATION#' + data['user_id']
        del data['user_id']
        return Response(dynamodbRecommendationsOperations.query_recommendations(data))

    @staticmethod
    def post(request):
        """
        request:{
        "to_user_id":"",
        "from_user_id":"",
        "song_id":"",
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RECOMMENDATION#' + data['to_user_id']
        data['SK'] = data['from_user_id']+'#'+data['song_id']
        del data['to_user_id']
        del data['from_user_id']
        return Response(dynamodbRecommendationsOperations.insert(data))


class RecommendationsDetailView(APIView):

    @staticmethod
    def get(request):
        """
        return:{
        "to_user_id":"",
        "from_user_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RECOMMENDATION#' + data['to_user_id']
        data['SK_BEGIN'] = data['from_user_id']
        del data['to_user_id']
        del data['from_user_id']
        return Response(dynamodbRecommendationsOperations.query_recommendations(data))

    @staticmethod
    def delete(request):
        """
        return:{
        "to_user_id":"",
        "from_user_id":"",
        "song_id":""
        }
        """
        data = JSONParser().parse(request)
        data['PK'] = 'RECOMMENDATION#' + data['to_user_id']
        data['SK'] = data['from_user_id'] + '#' + data['song_id']
        del data['to_user_id']
        del data['song_id']
        del data['from_user_id']
        dynamodbRecommendationsOperations.delete(data)
        return Response(status=status.HTTP_204_NO_CONTENT)
