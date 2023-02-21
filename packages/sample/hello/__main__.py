def main(args):
      name = args.get("name", "stranger")
      greeting = "Hello " + name + "!"
      if name == 'redirect':
            return { "statusCode": 301, "headers": { "location": "https://example.com"}}
      print(greeting)
      return {"body": greeting}
  