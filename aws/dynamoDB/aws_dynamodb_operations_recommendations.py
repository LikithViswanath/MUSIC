import boto3
from boto3.dynamodb.conditions import Key


class DynamodbRecommendationsOperations:
    """
    PK: RECOMMENDATION#to_user_id
    SK: RECOMMENDATION#from_user_id#song_id
    song_id
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('MUSIC')

    def insert(self, data):
        self.table.put_item(Item=data)
        return data

    def delete(self, key_data):
        self.table.delete_item(Key=key_data)

    def query_recommendations(self, data):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(data['PK'])
        )
        return response['Items']

    def query_recommendation(self, data):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(data['PK']) & Key('SK').begins_with(data['SK_BEGIN']),
        )
        return response['Items']
