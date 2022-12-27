import boto3
from boto3.dynamodb.conditions import Key


class DynamodbUserOperations:
    """
    PK: USER
    SK: USER#name#email ( user_id )
    name:
    email:
    artist_list {}
    album_list {}
    genre_list {}
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('MUSIC')

    def insert(self, data):
        self.table.put_item(Item=data)

    def delete(self, key_data):
        self.table.delete_item(Key=key_data)

    def update(self, data):
        self.table.update_item(
            Key={
                'PK': data['PK'],
                'SK': data['SK']
            },
            UpdateExpression='SET artist_list = :val1, genre_list = :val2, album_list = :val3',
            ExpressionAttributeValues={
                ':val1': data['artist_list'],
                ':val2': data['genre_list'],
                ':val3': data['album_list']
            }
        )
        response = self.table.get_item(
            Key={
                'PK': data['PK'],
                'SK': data['SK']
            }
        )

        return response['Item']

    def query_users(self):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq('USER')
        )
        return response['Items']

    def query_user_by_id(self, data):
        response = self.table.get_item(Key=data)
        return response["Item"]
