import os

from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv()
TOKEN = os.getenv('TOKEN')

database = RedisDict('exam_4_modul')
