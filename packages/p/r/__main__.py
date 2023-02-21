import os
import redis
from http import HTTPStatus
from hashids import Hashids


redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_pass = os.getenv('REDIS_PASS')

hashids = Hashids()

def hashids_encode(url_id):
    return hashids.encrypt(url_id)

def get_url_to_hash_response(url_to_hash):
      return { "body": "url_to_hash: %s" % url_to_hash }
def get_hash_to_url_response(hash_to_url):
      return { "body": "hash_to_url: %s" % hash_to_url }

def main(args):
      url_to_hash = args.get('url_to_hash', None)
      hash_to_url = args.get('hash_to_url', None)

      if url_to_hash is not None:
            return get_url_to_hash_response(url_to_hash)

      if hash_to_url is not None:
            return get_hash_to_url_response(hash_to_url)


      return { "body": "hash, %s" % hashids_encode(123) }

      # r = redis.Redis(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)

      # path = args.get('http')['path'] # e.g. "/some-hash"
      # hash = path[1:] # remove first symbol (slash '/')

      # # get URL by hash
      # # TODO
      # url = hash

      # if url == 'empty':
      #       return {
      #             "statusCode": HTTPStatus.NOT_FOUND
      #       }

      # if url == 'redirect':
      #       return {
      #             "statusCode": HTTPStatus.MOVED_PERMANENTLY,
      #             "headers": {
      #                   "location": "https://example.com"
      #             }
      #       }

      # return { "body": "hash is %s. host is %s" % (hash, redis_host,) }
  