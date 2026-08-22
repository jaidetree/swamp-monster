"""Model-level tests for Work/WorkImage: published/featured/order filtering
(the query behavior the eventual Home/Works views rely on) plus slug/thumbnail
seams.
"""

import pytest

from content.models import Work
from content.tests.factories import WorkFactory, WorkImageFactory

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
