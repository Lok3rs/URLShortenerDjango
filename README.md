# URLShortenerDjango

**python manage.py test** to see if everything works as intended

**POST**

http://localhost:8000/shorten/ 

Expected payload:
{
  'url': SOME_URL
}




**GET**

http://localhost:8000/<SHORTENED_SLUG>

Will redirect, if exist, to website for which given slug was previously generated

http://localhost:8000/unshort?url=<SHORTENED_SLUG OR SHORTENED_URL>

Will return full url path (if exist) for given slug/shortened url.
