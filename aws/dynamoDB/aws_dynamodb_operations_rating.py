import boto3
from boto3.dynamodb.conditions import Key


class DynamodbRatingOperations:
    """"
    PK: RATING#user_id
    SK: song_id
    rating
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('MUSIC')

    def insert(self, data):
        self.table.put_item(Item=data)

    def query_ratings(self, data):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(data['PK'])
        )
        return response['Items']

    def update(self, data):
        self.table.update_item(
            Key={
                'PK': data['PK'],
                'SK': data['SK']
            },
            UpdateExpression='SET rating = :val1',
            ExpressionAttributeValues={
                ':val1': data['rating'],
            }
        )
        response = self.table.get_item(
            Key={
                'PK': data['PK'],
                'SK': data['SK']
            }
        )

        return response['Item']

    def delete(self, data):
        self.table.delete_item(Key=data)

    def query_rating_by_id(self, data):
        response = self.table.get_item(Key=data)
        return response['Item']
