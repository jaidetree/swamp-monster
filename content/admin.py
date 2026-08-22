from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from django.contrib import admin

from .models import ContactSubmission, Resource, Training, Work, WorkImage
from .ordering import renumber


class DragNewRowsInline(SortableTabularInline):
    """A sortable inline whose *unsaved* rows are drag-sortable too.

    Ported from ~/projects/gracie's ``portfolio.admin.DragNewRowsInline``.
    django-admin-sortable2 only drives saved rows (``tr.has_original``): a row
    added via "Add another" has neither the class nor the handle markup, so it
    can't be dragged until it's saved. ``inline_sortable_new.js`` promotes each
    new row on ``formset:added`` so sortable2's existing Sortable picks it up —
    see that file for the seam. Loaded via ``Media`` here so every sortable
    inline that subclasses this inherits it; the listener is global and no-ops
    outside ``fieldset.sortable``.
    """

    class Media:
        js = ("content/inline_sortable_new.js",)


class WorkImageInline(DragNewRowsInline):
    """Drag-sortable gallery images for a Work; order=1 is the thumbnail."""

    model = WorkImage
    extra = 0
    fields = ("order", "image", "caption")


class RenumberingSortableAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Base drag-to-reorder changelist shared by every sortable ``content``
    model (``Work``, ``Training``, ``Resource``, ...).

    Ported from ~/projects/gracie's ``portfolio.admin.SortableProjectAdmin``.
    django-admin-sortable2 inserts a drag handle (``_reorder_``) as the leftmost
    column and strips ``order`` from the change form. ``order`` is left out of
    ``list_display`` so the handle lands on the left (keeping ``order`` there
    would only shift the handle inward). ``get_fields`` re-adds ``order`` on the
    change form so an editor can still type a number by hand when editing an
    existing row; new rows are auto-numbered to the end on add (sortable2's
    ``save_model``), so the add form omits ``order``.

    ``order`` is deliberately *not* in ``list_editable`` (it isn't a displayed
    column, so an inline input would have nowhere to render);
    ``published``/``featured`` stay inline-editable.
    """

    list_display = ("title", "slug", "published", "featured", "updated_at")
    list_editable = ("published", "featured")
    list_filter = ("published", "featured")
    search_fields = ("title",)
    ordering = ("order", "title")
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # Narrow sortable2's 50px-wide drag-handle column.
        css = {"all": ("content/sortable_admin.css",)}

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if obj is not None and "order" not in fields:
            fields.append("order")
        return fields

    def _update_order(self, updated_items, extra_model_filters):
        """Apply the dragged span, then renumber the whole collection 1..N.

        sortable2's drag only reindexes the rows between the drag's start and
        end position, so gaps elsewhere (left by deletes or the add-at-end
        default) survive. After the library applies the move, renumber every
        row by its resulting position so the whole collection stays gapless.
        ``order`` has no unique constraint, so the bulk update can't collide.
        """
        super()._update_order(updated_items, extra_model_filters)
        field = self.default_order_field
        rows = list(self.model.objects.filter(**extra_model_filters).order_by(field, "pk"))
        renumbered = renumber(rows, field)
        self.model.objects.bulk_update(renumbered, [field])
        return len(renumbered)


@admin.register(Work)
class WorkAdmin(RenumberingSortableAdmin):
    """Drag-to-reorder changelist for Works, with its drag-sortable gallery
    inline."""

    inlines = [WorkImageInline]


@admin.register(Training)
class TrainingAdmin(RenumberingSortableAdmin):
    """Drag-to-reorder changelist for Trainings. No inline: unlike Work,
    Training has a single plain ``image`` rather than a gallery."""


@admin.register(Resource)
class ResourceAdmin(RenumberingSortableAdmin):
    """Drag-to-reorder changelist for Resources (icon + downloadable file)."""


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Read-only, list-only view of contact-form submissions: a log, not
    owner-curated content, so no add/change permissions are needed."""

    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
