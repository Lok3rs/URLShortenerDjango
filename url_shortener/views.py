import json
import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from rest_framework.decorators import api_view

from URLShortenerDjango import settings
from url_shortener.models import Url


def get_unique_string():
    return uuid.uuid4().hex[:6].lower()


@csrf_exempt
@api_view(['POST'])
def shorten_url(request):
    try:
        params = json.loads(request.body.decode('utf-8'))
        url = params['url']
    except KeyError:
        response = {'status': "error", 'message': "URL Not Provided"}
        return HttpResponse(json.dumps(response), "application/json", status=status.HTTP_400_BAD_REQUEST)

    try:
        url = Url.objects.get(url=url)
    except Url.DoesNotExist:
        url = Url(url=url, slug=get_unique_string())
        url.save()

    return HttpResponse(json.dumps({'shortURL': f'{settings.DOMAIN}/{url.slug}'}))


@csrf_exempt
@api_view(['GET'])
def redirect_from_shortened_url(request, slug):
    url_object = get_object_or_404(Url, slug=slug)
    return HttpResponseRedirect(url_object.url)


@csrf_exempt
@api_view(['GET'])
def unshort_url(request):
    url_param = request.GET.get('url')
    if len(url_param) == 6:
        url = get_object_or_404(Url, slug=url_param)
        return HttpResponse(json.dumps({'url': url.url}), status=status.HTTP_200_OK)
    else:
        try:
            slug = url_param.split('/')[-1]
            url = get_object_or_404(Url, slug=slug)
            return HttpResponse(json.dumps({'url': url.url}), status=status.HTTP_200_OK)
        except IndexError:
            return HttpResponse(json.dumps({'message': 'Wrong URL provided'}), status=status.HTTP_400_BAD_REQUEST)
