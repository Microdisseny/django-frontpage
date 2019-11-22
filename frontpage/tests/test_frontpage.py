import pytest
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


def test_frontpage_anonymous_user(client):
    url = reverse('frontpage')
    response = client.get(url)

    assert response.status_code == 200
    assert 'You are about to enter a private area.' in response.content.decode('utf-8')


def test_frontpage_authenticated_staff_user(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password, is_staff=True)
    client.login(username=username, password=password)

    url = reverse('frontpage')
    response = client.get(url)

    admin_url = reverse('admin:index')

    assert response.status_code == 302
    assert response.url == admin_url


def test_frontpage_authenticated_no_staff_user(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    url = reverse('frontpage')
    response = client.get(url)

    assert response.status_code == 200
    assert 'Please log in with a different user.' in response.content.decode('utf-8')


def test_admin_anonymous_user(client):
    admin_url = reverse('admin:index')
    response = client.get(admin_url)

    frontpage_url = reverse('frontpage')

    assert response.status_code == 302
    assert response.url == '{frontpage_url}?{next}={admin_url}'.format(
        frontpage_url=frontpage_url,
        next=REDIRECT_FIELD_NAME,
        admin_url=admin_url
    )


def test_admin_authenticated_staff_user(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password, is_staff=True)
    client.login(username=username, password=password)

    admin_url = reverse('admin:index')
    response = client.get(admin_url)

    assert response.status_code == 200
    assert 'Site administration' in response.content.decode('utf-8')


def test_admin_authenticated_no_staff_user(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    admin_url = reverse('admin:index')
    response = client.get(admin_url)

    frontpage_url = reverse('frontpage')

    assert response.status_code == 302
    assert response.url == '{frontpage_url}?{next}={admin_url}'.format(
        frontpage_url=frontpage_url,
        next=REDIRECT_FIELD_NAME,
        admin_url=admin_url
    )


def test_frontpage_bad_middleware_configuration(client, settings):
    settings.MIDDLEWARE = []

    frontpage_url = reverse('frontpage')
    with pytest.raises(ImproperlyConfigured) as excinfo:
        client.get(frontpage_url)

    assert 'AuthenticationMiddleware not in MIDDLEWARE?' in str(excinfo.value)


def test_admin_bad_middleware_configuration(client, settings):
    settings.MIDDLEWARE = [
        'frontpage.middleware.FrontpageMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]

    admin_url = reverse('admin:index')
    with pytest.raises(ImproperlyConfigured) as excinfo:
        client.get(admin_url)

    assert 'Frontpage middleware should appear after AuthenticationMiddleware' in str(excinfo.value)
