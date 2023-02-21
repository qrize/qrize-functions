import os
from http import HTTPStatus

def main(args):
      redis_host = os.getenv('REDIS_HOST')
      redis_port = os.getenv('REDIS_PORT')
      redis_pass = os.getenv('REDIS_PASS')

      path = args.get('http')['path'] # e.g. "/some-hash"
      hash = path[1:] # remove first symbol (slash '/')

      # get URL by hash
      # TODO
      url = hash

      if url == 'empty':
            return {
                  "statusCode": HTTPStatus.NOT_FOUND
            }

      if url == 'redirect':
            return {
                  "statusCode": HTTPStatus.MOVED_PERMANENTLY,
                  "headers": {
                        "location": "https://example.com"
                  }
            }

      return { "body": "hash is %s. host is %s" % (hash, redis_host,) }
  