"""View/template tests for the public Works listing (ticket 13). Covers the
acceptance criteria: the published filter and order on `/works`.
"""

import pytest
from django.urls import reverse

from swamp.tests.factories import WorkFactory, WorkImageFactory


@pytest.mark.django_db
def test_work_list_shows_only_published_works(client):
    published = WorkFactory(title="Published Work", published=True)
    WorkImageFactory(work=published, order=1)
    WorkFactory(title="Unpublished Work", published=False)

    response = client.get(reverse("swamp:work_list"))

    assert response.status_code == 200
    works = list(response.context["works"])
    assert works == [published]
    assert b"Published Work" in response.content
    assert b"Unpublished Work" not in response.content


@pytest.mark.django_db
def test_work_list_orders_newest_first(client):
    first = WorkFactory(title="First")
    second = WorkFactory(title="Second")
    third = WorkFactory(title="Third")

    response = client.get(reverse("swamp:work_list"))

    works = list(response.context["works"])
    assert works == [third, second, first]

