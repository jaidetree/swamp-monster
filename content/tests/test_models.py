"""Model-level tests for Work/WorkImage/Training/Resource: published/featured/
order filtering (the query behavior the eventual Home/Works/Training/Resource
views rely on) plus slug/thumbnail seams.
"""

import pytest

from content.models import ContactSubmission, Resource, Training, Work
from content.tests.factories import (
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


def test_training_published_defaults_to_true():
    assert Training().published is True


def test_training_featured_defaults_to_false():
    assert Training().featured is False


def test_training_published_filters_out_unpublished_trainings():
    TrainingFactory(title="Visible", published=True)
    TrainingFactory(title="Hidden", published=False)

    titles = list(Training.objects.filter(published=True).values_list("title", flat=True))

    assert titles == ["Visible"]


def test_training_featured_filters_to_only_featured_trainings():
    TrainingFactory(title="Featured", featured=True)
    TrainingFactory(title="Not featured", featured=False)

    titles = list(Training.objects.filter(featured=True).values_list("title", flat=True))

    assert titles == ["Featured"]


def test_training_default_queryset_orders_by_order_then_title():
    TrainingFactory(title="Z", order=2)
    TrainingFactory(title="A", order=1)
    TrainingFactory(title="B", order=1)

    titles = list(Training.objects.values_list("title", flat=True))

    assert titles == ["A", "B", "Z"]


def test_training_slug_is_auto_generated_from_title_when_blank():
    training = TrainingFactory(title="Saddle Stitching Basics", slug="")
    assert training.slug == "saddle-stitching-basics"


def test_training_slug_is_unique_on_clash():
    TrainingFactory(title="Basics", slug="basics")
    second = TrainingFactory(title="Basics", slug="")
    assert second.slug == "basics-2"


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
