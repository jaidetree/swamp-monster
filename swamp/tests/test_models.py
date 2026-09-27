"""Model-level tests for Work/WorkImage/Resource: published/featured/order
filtering (the query behavior the Home/Works/Resource views rely on) plus
slug/thumbnail seams. Training and ContactSubmission are request logs rather
than owner-curated content, so their coverage is just shape (str/ordering),
further down.
"""

from datetime import date

import pytest

from swamp.models import ContactSubmission, Resource, Training, Work
from swamp.tests.factories import (
    ContactSubmissionFactory,
    ResourceFactory,
    TrainingFactory,
    WorkFactory,
    WorkImageFactory,
)

pytestmark = pytest.mark.django_db


def test_published_defaults_to_true():
    assert Work().published is True


def test_featured_defaults_to_false():
    assert Work().featured is False


def test_published_filters_out_unpublished_works():
    WorkFactory(title="Visible", published=True)
    WorkFactory(title="Hidden", published=False)

    titles = list(Work.objects.filter(published=True).values_list("title", flat=True))

    assert titles == ["Visible"]


def test_featured_filters_to_only_featured_works():
    WorkFactory(title="Featured", featured=True)
    WorkFactory(title="Not featured", featured=False)

    titles = list(Work.objects.filter(featured=True).values_list("title", flat=True))

    assert titles == ["Featured"]


def test_default_queryset_orders_by_order_then_title():
    WorkFactory(title="Z", order=2)
    WorkFactory(title="A", order=1)
    WorkFactory(title="B", order=1)

    titles = list(Work.objects.values_list("title", flat=True))

    assert titles == ["A", "B", "Z"]


def test_slug_is_auto_generated_from_title_when_blank():
    work = WorkFactory(title="Hand-Stitched Wallet", slug="")
    assert work.slug == "hand-stitched-wallet"


def test_slug_is_unique_on_clash():
    WorkFactory(title="Wallet", slug="wallet")
    second = WorkFactory(title="Wallet", slug="")
    assert second.slug == "wallet-2"


def test_slug_is_left_untouched_when_explicitly_set():
    work = WorkFactory(title="Wallet", slug="custom-slug")
    assert work.slug == "custom-slug"


def test_thumbnail_is_the_order_one_gallery_image():
    work = WorkFactory()
    WorkImageFactory(work=work, order=2)
    thumb = WorkImageFactory(work=work, order=1)

    assert work.thumbnail == thumb


def test_thumbnail_is_none_when_gallery_is_empty():
    work = WorkFactory()
    assert work.thumbnail is None


def test_work_image_str_includes_work_title_and_order():
    image = WorkImageFactory(order=1, work__title="Satchel")
    assert str(image) == "Satchel image #1"


# --- Training ---


def test_training_target_dates_defaults_to_empty_list():
    assert Training(name="Jamie", email="jamie@example.com", message="Hi").target_dates == []


def test_training_str_includes_name_and_email():
    submission = TrainingFactory(name="Jamie", email="jamie@example.com")
    assert str(submission) == "Jamie <jamie@example.com>"


def test_training_default_queryset_orders_newest_first():
    older = TrainingFactory(name="Older")
    newer = TrainingFactory(name="Newer")

    names = list(Training.objects.values_list("name", flat=True))

    assert names == [newer.name, older.name]


def test_training_target_dates_stores_multiple_dates_in_order():
    submission = TrainingFactory(target_dates=[date(2026, 10, 1), date(2026, 10, 15)])
    submission.refresh_from_db()

    assert submission.target_dates == [date(2026, 10, 1), date(2026, 10, 15)]


# --- Resource ---


def test_resource_published_defaults_to_true():
    assert Resource(file="resources/files/placeholder.pdf").published is True


def test_resource_featured_defaults_to_false():
    assert Resource(file="resources/files/placeholder.pdf").featured is False


def test_resource_published_filters_out_unpublished_resources():
    ResourceFactory(title="Visible", published=True)
    ResourceFactory(title="Hidden", published=False)

    titles = list(Resource.objects.filter(published=True).values_list("title", flat=True))

    assert titles == ["Visible"]


def test_resource_featured_filters_to_only_featured_resources():
    ResourceFactory(title="Featured", featured=True)
    ResourceFactory(title="Not featured", featured=False)

    titles = list(Resource.objects.filter(featured=True).values_list("title", flat=True))

    assert titles == ["Featured"]


def test_resource_default_queryset_orders_by_order_then_title():
    ResourceFactory(title="Z", order=2)
    ResourceFactory(title="A", order=1)
    ResourceFactory(title="B", order=1)

    titles = list(Resource.objects.values_list("title", flat=True))

    assert titles == ["A", "B", "Z"]


def test_resource_slug_is_auto_generated_from_title_when_blank():
    resource = ResourceFactory(title="Pattern Template", slug="")
    assert resource.slug == "pattern-template"


def test_resource_slug_is_unique_on_clash():
    ResourceFactory(title="Template", slug="template")
    second = ResourceFactory(title="Template", slug="")
    assert second.slug == "template-2"


# --- ContactSubmission ---


def test_contact_submission_str_includes_name_and_email():
    submission = ContactSubmissionFactory(name="Jamie", email="jamie@example.com")
    assert str(submission) == "Jamie <jamie@example.com>"


def test_contact_submission_default_queryset_orders_newest_first():
    older = ContactSubmissionFactory(name="Older")
    newer = ContactSubmissionFactory(name="Newer")

    names = list(ContactSubmission.objects.values_list("name", flat=True))

    assert names == [newer.name, older.name]
