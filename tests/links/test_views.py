from urllib.parse import urljoin

import pytest
from nose.tools import eq_

from django.core.urlresolvers import reverse

from linkanywhere.apps.links.models import Category, Link, Tag
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_create_link(client):
    category_1 = f.CategoryFactory.create()
    tag_1 = f.TagFactory.create()
    tag_2 = f.TagFactory.create()

    url = reverse('links:link-list')
    data = {
        'title': 'Test link',
        'url': 'https://testlink.com',
        'description': 'Test link description',
        'category': category_1.name,
        'tags': [tag_1.name, tag_2.name]
    }

    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, 201)
    eq_(response_content['category'], category_1.name)
    eq_(response_content['tags'], [tag_1.name, tag_2.name])


def test_create_link_with_not_created_tags(client):
    category_1 = f.CategoryFactory.create()

    url = reverse('links:link-list')
    data = {
        'title': 'Test link',
        'url': 'https://testlink.com',
        'description': 'Test link description',
        'category': category_1.name,
        'tags': ['some tag 1', 'some tag 2']
    }
    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, 201)
    eq_(response_content['tags'], ['some tag 1', 'some tag 2'])


def test_create_category(client, admin_client):
    url = reverse('links:category-list')
    data = {'name': 'Test category'}

    response = client.post(url)
    eq_(response.status_code, 403)

    response = admin_client.post(url, data)
    response_content = response.data
    eq_(response.status_code, 201)
    eq_(response_content['name'], 'Test category')


def test_create_tag(client):
    url = reverse('links:tag-list')
    data = {'name': 'Test tag'}

    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, 201)
    eq_(response_content['name'], 'Test tag')


def test_list_links(client):
    link_1 = f.LinkFactory.create()
    f.LinkFactory.create()

    url = reverse('links:link-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(link_1.id))


def test_list_links_filtered_by_category_and_tag(client):
    category_1 = f.CategoryFactory.create()
    tag_1 = f.TagFactory.create()
    f.LinkFactory.create(category=category_1)
    f.LinkFactory.create(tags=[tag_1])
    f.LinkFactory.create(category=category_1, tags=[tag_1])
    f.LinkFactory.create()

    # by category

    url = urljoin(reverse('links:link-list'),
                  '?category={}'.format(category_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)

    # by tag

    url = urljoin(reverse('links:link-list'),
                  '?tag={}'.format(tag_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)

    # by category & tag

    url = urljoin(reverse('links:link-list'),
                  '?category={}&tag={}'.format(category_1.name, tag_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 1)


def test_list_categories(client):
    category_1 = f.CategoryFactory.create()
    f.CategoryFactory.create()

    url = reverse('links:category-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(category_1.id))


def test_list_tags(client):
    tag_1 = f.TagFactory.create()
    f.TagFactory.create()

    url = reverse('links:tag-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(tag_1.id))


def test_destroy_link(client):
    category_1 = f.CategoryFactory.create()
    link_1 = f.LinkFactory.create(category=category_1)

    url = reverse('links:link-detail', kwargs={'pk': link_1.id})
    response = client.delete(url)

    eq_(response.status_code, 204)
    eq_(Link.objects.count(), 0)
    eq_(category_1.links.count(), 0)


def test_destroy_category(client, admin_client):
    category_1 = f.CategoryFactory.create()

    url = reverse('links:category-detail', kwargs={'pk': category_1.id})

    response = client.delete(url)
    eq_(response.status_code, 403)

    response = admin_client.delete(url)
    eq_(response.status_code, 204)
    eq_(Category.objects.count(), 0)


def test_destroy_tag(client):
    tag_1 = f.TagFactory.create()

    url = reverse('links:tag-detail', kwargs={'pk': tag_1.id})
    response = client.delete(url)

    eq_(response.status_code, 204)
    eq_(Tag.objects.count(), 0)


def test_search_links(client):
    f.LinkFactory.create(description='some description here')
    f.LinkFactory.create()

    url = urljoin(reverse('links:link-list'),
                  '?search=some+description')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, 200)
    eq_(len(response_content), 1)
