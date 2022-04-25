import ast

from rest_framework import status
from rest_framework.test import APITestCase

from URLShortenerDjango import settings


class URLTest(APITestCase):

    def test_create_shortener_url(self):
        payload = {'url': 'https://google.com/'}
        res = self.client.post('/shorten', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = ast.literal_eval(res.content.decode('utf-8'))
        self.assertIn(settings.DOMAIN, data['shortURL'])
        self.assertEqual(len(data['shortURL'].split('/')[-1]), 6)

    def test_not_duplicate_urls(self):
        payload = {'url': 'https://google.com/'}
        res = self.client.post('/shorten', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = ast.literal_eval(res.content.decode('utf-8'))
        first_url = data['shortURL']

        res = self.client.post('/shorten', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = ast.literal_eval(res.content.decode('utf-8'))
        second_url = data['shortURL']

        self.assertEqual(first_url, second_url)

    def test_redirect(self):
        payload = {'url': 'https://google.com/'}
        res = self.client.post('/shorten', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = ast.literal_eval(res.content.decode('utf-8'))
        slug = data['shortURL'].split('/')[-1]

        res = self.client.get(f'/{slug}')

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res.url, payload['url'])

    def test_unshort(self):
        payload = {'url': 'https://google.com/'}
        res = self.client.post('/shorten', payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = ast.literal_eval(res.content.decode('utf-8'))
        full_url = data['shortURL']
        slug = full_url.split('/')[-1]

        res = self.client.get('/unshort', data={'url': full_url})
        self.assertEqual(res.status_code, 200)
        data = ast.literal_eval(res.content.decode('utf-8'))
        self.assertEqual(data['url'], payload['url'])

        res = self.client.get('/unshort', data={'url': slug})
        self.assertEqual(res.status_code, 200)
        data = ast.literal_eval(res.content.decode('utf-8'))
        self.assertEqual(data['url'], payload['url'])

    def test_wrong_slug(self):
        slug = 'random'
        res = self.client.get(f'/{slug}')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_unshort(self):
        full_url = f'{settings.DOMAIN}/random'
        slug = 'random'

        res = self.client.get('/unshort', data={'url': full_url})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        res = self.client.get('/unshort', data={'url': slug})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
