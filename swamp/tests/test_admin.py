"""Admin tests for the ported sortable-admin pattern: drag handle placement,
the order field's add/change-form visibility, auto-numbering on save, the
renumber-on-drag behavior of the reorder endpoint, and the unsaved-row
drag-sortable inline wiring.

Adapted from ~/projects/gracie's portfolio/tests/test_admin.py for this app's
single sortable model (Work) and its sortable inline (WorkImage).
"""

import json

import pytest
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib.admin.sites import site
from django.test import RequestFactory
from django.urls import reverse

from swamp.admin import (
    ContactSubmissionAdmin,
    ResourceAdmin,
    TrainingAdmin,
    WorkAdmin,
    WorkImageInline,
)
from swamp.models import ContactSubmission, Work
from swamp.tests.factories import (
    ContactSubmissionFactory,
    ResourceFactory,
    TrainingFactory,
    WorkFactory,
)


def _instance():
    return WorkAdmin(Work, site)


# --- drag-and-drop wiring ---


def test_work_changelist_is_sortable():
    assert issubclass(WorkAdmin, SortableAdminMixin)


def test_work_image_inline_is_sortable():
    assert issubclass(WorkImageInline, SortableInlineAdminMixin)


@pytest.mark.django_db
def test_changelist_shows_drag_handle_on_the_left():
    # The drag handle is the leftmost column and the bare order column never
    # renders.
    request = RequestFactory().get("/")
    columns = _instance().get_list_display(request)
    assert columns[0] == "_reorder_"
    assert "order" not in columns


def test_order_is_not_inline_editable():
    # order is reordered by drag, never by an inline changelist input — it
    # isn't a displayed column, so listing it in list_editable would have
    # nowhere to render.
    assert "order" not in WorkAdmin.list_editable


# --- the order number stays typeable on the change form, not the add form ---


@pytest.mark.django_db
def test_change_form_keeps_editable_order():
    work = WorkFactory()
    request = RequestFactory().get("/change/")
    fields = _instance().get_fields(request, obj=work)
    assert "order" in fields


def test_add_form_omits_order():
    # New Works are auto-numbered to the end on save, so the add form hides
    # order.
    request = RequestFactory().get("/add/")
    fields = _instance().get_fields(request, obj=None)
    assert "order" not in fields


# --- new Works auto-number to the end on add (sortable2's save_model) ---


@pytest.mark.django_db
def test_new_work_lands_at_end():
    WorkFactory(order=5)
    obj = Work(title="New")
    _instance().save_model(None, obj, None, change=False)
    assert obj.order == 6


@pytest.mark.django_db
def test_first_work_gets_order_one():
    obj = Work(title="First")
    _instance().save_model(None, obj, None, change=False)
    assert obj.order == 1


@pytest.mark.django_db
def test_editing_existing_work_does_not_renumber():
    # On edit, save_model leaves the (possibly hand-typed) order untouched.
    work = WorkFactory(order=3)
    work.title = "Edited"
    _instance().save_model(None, work, None, change=True)
    assert work.order == 3


# --- the bulk reorder endpoint persists a drag in one request ---


@pytest.mark.django_db
def test_reorder_endpoint_persists_new_order(admin_client):
    first = WorkFactory(order=1)
    second = WorkFactory(order=2)
    url = reverse("admin:swamp_work_sortable_update")

    response = admin_client.post(
        url,
        data=json.dumps({"updatedItems": [[first.pk, 2], [second.pk, 1]]}),
        content_type="application/json",
    )

    assert response.status_code == 200
    first.refresh_from_db()
    second.refresh_from_db()
    assert (first.order, second.order) == (2, 1)


@pytest.mark.django_db
def test_reorder_cleans_up_gaps_across_whole_collection(admin_client):
    # A gappy collection (left by deletes / add-at-end). sortable2 alone would
    # only reindex the moved span; our override renumbers the whole collection.
    a = WorkFactory(order=1)
    b = WorkFactory(order=5)
    c = WorkFactory(order=9)
    url = reverse("admin:swamp_work_sortable_update")

    # Drag c to the front (the JS sends only the moved item's new span order).
    response = admin_client.post(
        url,
        data=json.dumps({"updatedItems": [[c.pk, 0]]}),
        content_type="application/json",
    )

    assert response.status_code == 200
    orders = dict(Work.objects.values_list("pk", "order"))
    assert sorted(orders.values()) == [1, 2, 3]  # no gaps anywhere
    assert orders[c.pk] == 1  # c is first
    assert orders[a.pk] < orders[b.pk]  # untouched relative order preserved


@pytest.mark.django_db
def test_reorder_endpoint_rejects_get(admin_client):
    url = reverse("admin:swamp_work_sortable_update")
    assert admin_client.get(url).status_code == 405


# --- unsaved inline rows are made drag-sortable too ---


def test_work_image_inline_ships_new_row_promoter():
    # The promoter script (which makes added-but-unsaved rows drag-sortable)
    # is wired through Media, so the change/add page actually loads it.
    media = WorkImageInline(Work, site).media
    assert "swamp/inline_sortable_new.js" in media._js


def test_work_image_inline_shows_no_blank_row_by_default():
    assert WorkImageInline.extra == 0


@pytest.mark.django_db
def test_work_add_form_renders_the_gallery_inline(admin_client):
    response = admin_client.get(reverse("admin:swamp_work_add"))
    assert response.status_code == 200
    assert "images-TOTAL_FORMS" in response.content.decode()


# --- Training/Resource reuse the same sortable-admin base as Work ---


def test_training_changelist_is_sortable():
    assert issubclass(TrainingAdmin, SortableAdminMixin)


def test_resource_changelist_is_sortable():
    assert issubclass(ResourceAdmin, SortableAdminMixin)


@pytest.mark.django_db
def test_training_reorder_endpoint_persists_new_order(admin_client):
    first = TrainingFactory(order=1)
    second = TrainingFactory(order=2)
    url = reverse("admin:swamp_training_sortable_update")

    response = admin_client.post(
        url,
        data=json.dumps({"updatedItems": [[first.pk, 2], [second.pk, 1]]}),
        content_type="application/json",
    )

    assert response.status_code == 200
    first.refresh_from_db()
    second.refresh_from_db()
    assert (first.order, second.order) == (2, 1)


@pytest.mark.django_db
def test_resource_reorder_endpoint_persists_new_order(admin_client):
    first = ResourceFactory(order=1)
    second = ResourceFactory(order=2)
    url = reverse("admin:swamp_resource_sortable_update")

    response = admin_client.post(
        url,
        data=json.dumps({"updatedItems": [[first.pk, 2], [second.pk, 1]]}),
        content_type="application/json",
    )

    assert response.status_code == 200
    first.refresh_from_db()
    second.refresh_from_db()
    assert (first.order, second.order) == (2, 1)


@pytest.mark.django_db
def test_training_add_form_renders(admin_client):
    response = admin_client.get(reverse("admin:swamp_training_add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_resource_add_form_renders(admin_client):
    response = admin_client.get(reverse("admin:swamp_resource_add"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_resource_change_form_serves_a_downloadable_file_link(admin_client):
    resource = ResourceFactory(title="Pattern")
    response = admin_client.get(reverse("admin:swamp_resource_change", args=[resource.pk]))
    assert response.status_code == 200
    assert resource.file.url in response.content.decode()


@pytest.mark.django_db
def test_resource_file_is_retrievable_via_its_storage():
    resource = ResourceFactory(title="Pattern")
    with resource.file.storage.open(resource.file.name) as fh:
        assert fh.read()


# --- ContactSubmission is read-only in admin ---


def test_contact_submission_admin_has_no_add_permission():
    admin_instance = ContactSubmissionAdmin(ContactSubmission, site)
    assert admin_instance.has_add_permission(RequestFactory().get("/")) is False


def test_contact_submission_admin_has_no_change_permission():
    admin_instance = ContactSubmissionAdmin(ContactSubmission, site)
    assert admin_instance.has_change_permission(RequestFactory().get("/")) is False


def test_contact_submission_admin_has_no_delete_permission():
    admin_instance = ContactSubmissionAdmin(ContactSubmission, site)
    assert admin_instance.has_delete_permission(RequestFactory().get("/")) is False


@pytest.mark.django_db
def test_contact_submission_is_visible_in_admin_changelist(admin_client):
    ContactSubmissionFactory(name="Jamie", email="jamie@example.com")
    response = admin_client.get(reverse("admin:swamp_contactsubmission_changelist"))
    assert response.status_code == 200
    assert "Jamie" in response.content.decode()
