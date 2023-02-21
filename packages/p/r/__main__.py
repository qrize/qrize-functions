import os
import re
import redis
from urllib.parse import urlsplit, urlunsplit, quote, quote_plus
from http import HTTPStatus
from hashids import Hashids


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")
HASH_SALT = os.getenv("HASH_SALT")
COUNTER_KEY = "counter"

hashids = Hashids(salt=HASH_SALT)

url_regex = re.compile(
    r"^((?:http|ftp)s?://)?"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def validate_url(url):
    return True if url_regex.match(url) else False


def normalize_url(url):
    """
    Sometimes you get URLs that aren't real because they contain
    unsafe characters like ' ' and so on.
    This function can fix some of the problems in a similar way browsers
    handle data entered by the user.

    See: http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python
    """
    scheme, netloc, path, qs, anchor = urlsplit(url)
    path = quote(path, "/%")
    qs = quote_plus(qs, ":&=")
    return urlunsplit((scheme, netloc, path, qs, anchor))


def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASS,
        decode_responses=True,
    )


def get_hash_key(hash):
    return "hash::{}".format(hash)


def get_url_key(url):
    return "url::{}".format(url)


def get_hash_for_url(url):
    r = get_redis()
    url_key = get_url_key(url)
    hash = r.get(url_key)
    if not hash:
        id = r.incr(COUNTER_KEY)
        hash = hashids.encode(id)
        hash_key = get_hash_key(hash)
        r.set(hash_key, url)
        r.set(url_key, hash)
    return hash


def get_url_for_hash(hash):
    r = get_redis()
    hash_key = get_hash_key(hash)
    return r.get(hash_key)


def url_to_hash(url):
    # check if url is not empty
    if not url:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "No url provided",
        }

    # http://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    url = normalize_url(url[:2048])

    # check if url is valid
    if not validate_url(url):
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Invalid url",
        }

    # retrieve hash from db
    hash = get_hash_for_url(url)

    return {
        "body": {
            "url": url,
            "hash": hash,
        }
    }


def hash_to_url(hash):
    url = get_url_for_hash(hash)

    if not url:
        return {
            "statusCode": HTTPStatus.NOT_FOUND,
            "body": "No url found",
        }

    return {
        "body": {
            "url": url,
            "hash": hash,
        }
    }


def redirect(args):
    path = args.get("http")["path"]  # e.g. "/some-hash"
    hash = path[1:]  # remove first symbol (slash '/')

    url = get_url_for_hash(hash)

    if not url:
        return {
            "statusCode": HTTPStatus.NOT_FOUND,
            "body": "No url found",
        }

    return {
        "statusCode": HTTPStatus.MOVED_PERMANENTLY,
        "headers": {"location": url},
    }


def main(args):
    url = args.get("url", None)
    hash = args.get("hash", None)

    # get hash by url
    if url is not None:
        return url_to_hash(url)

    # get url by hash
    if hash is not None:
        return hash_to_url(hash)

    return redirect(args)
