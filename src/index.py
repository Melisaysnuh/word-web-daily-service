import os
import motor.motor_asyncio
from pymongo.errors import PyMongoError

async def connect_db() -> dict[str, int | str]:
    url = os.getenv('mongodb://localhost:27017')

    if url:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(url)
            db = client['wordweb']

            await db.command('ping')

            print('Successfully connected to the database.')
            return {
                'statusCode': 200,

            }
        except PyMongoError as e:
            print('Internal server error:', e)
            return {
                'statusCode': 500,
                'message': 'Internal server error.'
            }
    else:
        return {
            'statusCode': 500,
            'message': 'Error retrieving URL from environment variables.'
        }
