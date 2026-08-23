"""View/template tests for the public Works listing and gallery pages
(ticket 13). Covers the acceptance criteria: the published filter and order
on `/works`, and gallery rendering (images in order, Markdown captions) on
a Work's detail page.
"""

import pytest
from django.urls import reverse

from swamp.tests.factories import WorkFactory, WorkImageFactory


@pytest.mark.django_db
def test_work_list_shows_only_published_works(client):
    published = WorkFactory(title="Published Work", published=True)
    WorkFactory(title="Unpublished Work", published=False)

    response = client.get(reverse("swamp:work_list"))

    assert response.status_code == 200
    works = list(response.context["works"])
    assert works == [published]
    assert b"Published Work" in response.content
    assert b"Unpublished Work" not in response.content


@pytest.mark.django_db
def test_work_list_orders_by_order_ascending(client):
    second = WorkFactory(title="Second", order=2)
    first = WorkFactory(title="First", order=1)
    third = WorkFactory(title="Third", order=3)

    response = client.get(reverse("swamp:work_list"))

    works = list(response.context["works"])
    assert works == [first, second, third]


@pytest.mark.django_db
def test_work_detail_returns_404_for_unpublished_work(client):
    work = WorkFactory(published=False)

    response = client.get(reverse("swamp:work_detail", args=[work.slug]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_work_detail_renders_images_in_order(client):
    work = WorkFactory(published=True)
    second = WorkImageFactory(work=work, order=2, caption="Second caption")
    first = WorkImageFactory(work=work, order=1, caption="First caption")

    response = client.get(reverse("swamp:work_detail", args=[work.slug]))

    assert response.status_code == 200
    images = list(response.context["images"])
    assert images == [first, second]


@pytest.mark.django_db
def test_work_detail_renders_caption_as_markdown(client):
    work = WorkFactory(published=True)
    WorkImageFactory(work=work, order=1, caption="**bold** caption")

    response = client.get(reverse("swamp:work_detail", args=[work.slug]))

    assert b"<strong>bold</strong> caption" in response.content
