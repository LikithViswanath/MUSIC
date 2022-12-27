import boto3
from boto3.dynamodb.conditions import Key, Attr


class DynamodbPlaylistOperations:
    """
    PK: PLAYLIST#user_id
    SK: playlist_name#song_id
    playlist_name
    song_id
    """
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('MUSIC')

    def insert(self, data):
        self.table.put_item(Item=data)
        return data

    def delete(self, data):
        self.table.delete_item(Key=data)

    def query_playlists(self, data):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(data['PK'])
        )
        return response['Items']

    def query_playlist_by_name(self, data):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(data['PK']) & Key('SK').begins_with(data['BEGIN_SK'])
        )
        return response['Items']
