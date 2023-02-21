def main(args):
      path = args.get('http')['path'] # e.g. "/some-hash"
      hash = path[1:] # remove first symbol (slash '/')

      # get URL by hash
      # TODO
      url = hash

      if url == 'empty':
            return {
                  "statusCode": 404
            }

      if url == 'redirect':
            return {
                  "statusCode": 301,
                  "headers": {
                        "location": "https://example.com"
                  }
            }

      return { "body": "hash is %s" % hash }
  