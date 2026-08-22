"""View/template tests for the Home page (ticket 14). Covers the acceptance
criteria: featured+published filtering per teaser section (Works/Training/
Resources), and graceful empty-state rendering when a section has zero
qualifying rows.
"""

import pytest
from django.urls import reverse

from content.tests.factories import ResourceFactory, TrainingFactory, WorkFactory


@pytest.mark.django_db
def test_home_renders_hero_and_section_headings(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert b"Swamp Monster Leather" in response.content
    assert b"Work" in response.content
    assert b"Training" in response.content
    assert b"Resources" in response.content
    assert b"About" in response.content


@pytest.mark.django_db
def test_home_works_teaser_shows_only_featured_published_works(client):
    shown = WorkFactory(title="Shown Work", published=True, featured=True)
    WorkFactory(title="Unfeatured Work", published=True, featured=False)
    WorkFactory(title="Unpublished Work", published=False, featured=True)

    response = client.get(reverse("home"))

    works = list(response.context["works"])
    assert works == [shown]
    assert b"Shown Work" in response.content
    assert b"Unfeatured Work" not in response.content
    assert b"Unpublished Work" not in response.content


@pytest.mark.django_db
def test_home_works_teaser_orders_by_order_ascending(client):
    second = WorkFactory(title="Second", published=True, featured=True, order=2)
    first = WorkFactory(title="First", published=True, featured=True, order=1)

    response = client.get(reverse("home"))

    works = list(response.context["works"])
    assert works == [first, second]


@pytest.mark.django_db
def test_home_training_teaser_shows_only_featured_published_trainings(client):
    shown = TrainingFactory(title="Shown Training", published=True, featured=True)
    TrainingFactory(title="Unfeatured Training", published=True, featured=False)
    TrainingFactory(title="Unpublished Training", published=False, featured=True)

    response = client.get(reverse("home"))

    trainings = list(response.context["trainings"])
    assert trainings == [shown]
    assert b"Shown Training" in response.content
    assert b"Unfeatured Training" not in response.content
    assert b"Unpublished Training" not in response.content


@pytest.mark.django_db
def test_home_resource_teaser_shows_only_featured_published_resources(client):
    shown = ResourceFactory(title="Shown Resource", published=True, featured=True)
    ResourceFactory(title="Unfeatured Resource", published=True, featured=False)
    ResourceFactory(title="Unpublished Resource", published=False, featured=True)

    response = client.get(reverse("home"))

    resources = list(response.context["resources"])
    assert resources == [shown]
    assert b"Shown Resource" in response.content
    assert b"Unfeatured Resource" not in response.content
    assert b"Unpublished Resource" not in response.content


@pytest.mark.django_db
def test_home_renders_without_breakage_when_all_teasers_empty(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert list(response.context["works"]) == []
    assert list(response.context["trainings"]) == []
    assert list(response.context["resources"]) == []
    # No CMS-editor-facing placeholder text should leak to visitors.
    assert b"no works" not in response.content.lower()
    assert b"no training" not in response.content.lower()
    assert b"no resources" not in response.content.lower()
