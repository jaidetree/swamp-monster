"""Models for the `content` app — owner-editable site content (ADR: CMS Content
Model).

``Work`` is the first and most complex model, establishing the sortable-admin
pattern (ported from ~/projects/gracie) the rest of this app's models reuse:
an explicit ``order`` field, excluded from the admin changelist/list_editable
so a drag handle can occupy the leftmost column instead, renumbered 1..N after
every drag via ``content.ordering.renumber``.
"""

from django.db import models
from django.utils.text import slugify


class Work(models.Model):
    """A finished leather piece shown in the portfolio.

    Display order is entirely owner-controlled via ``order`` (never
    ``created_at``/``updated_at``); only ``published`` pieces are ever shown to
    visitors, and ``featured`` narrows that further to the Home page teaser.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated from the title; override for a custom URL.",
    )
    description = models.TextField(
        blank=True,
        help_text="Markdown; rendered via django-markdownify wherever displayed.",
    )
    published = models.BooleanField(
        default=True,
        help_text="Unpublished works are hidden from the public site.",
    )
    featured = models.BooleanField(
        default=False,
        help_text="Featured works appear in the Home page teaser.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manual display order; lower numbers appear first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self):
        """A slug unique across Works, appending -2, -3, ... on a clash."""
        base = slugify(self.title)
        slug = base
        siblings = Work.objects.exclude(pk=self.pk)
        n = 2
        while siblings.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    @property
    def thumbnail(self):
        """The order=1 gallery image — the thumbnail used wherever a Work
        appears without its full gallery. None when the gallery is empty."""
        return self.images.order_by("order").first()


def work_image_upload_to(instance, filename):
    return f"works/{instance.work_id}/{filename}"


class WorkImage(models.Model):
    """One image in a Work's gallery.

    ``order=1`` is the thumbnail used wherever the parent ``Work`` appears
    without its full gallery (``Work.thumbnail``).
    """

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=work_image_upload_to)
    caption = models.TextField(
        blank=True,
        help_text="Markdown; rendered via django-markdownify wherever displayed.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manual display order within the gallery; order=1 is the thumbnail.",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.work.title} image #{self.order}"


class Training(models.Model):
    """A training offering the owner has built out.

    Same shape as ``Work`` minus the gallery — a single ``image`` rather than
    an ordered set of ``WorkImage``s.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated from the title; override for a custom URL.",
    )
    description = models.TextField(
        blank=True,
        help_text="Markdown; rendered via django-markdownify wherever displayed.",
    )
    image = models.ImageField(upload_to="training/", blank=True)
    published = models.BooleanField(
        default=True,
        help_text="Unpublished training entries are hidden from the public site.",
    )
    featured = models.BooleanField(
        default=False,
        help_text="Featured training entries appear in the Home page teaser.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manual display order; lower numbers appear first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self):
        """A slug unique across Trainings, appending -2, -3, ... on a clash."""
        base = slugify(self.title)
        slug = base
        siblings = Training.objects.exclude(pk=self.pk)
        n = 2
        while siblings.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug


class Resource(models.Model):
    """A downloadable resource (e.g. a template) the owner offers visitors."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated from the title; override for a custom URL.",
    )
    description = models.TextField(
        blank=True,
        help_text="Markdown; rendered via django-markdownify wherever displayed.",
    )
    icon = models.ImageField(upload_to="resources/icons/", blank=True)
    file = models.FileField(upload_to="resources/files/")
    published = models.BooleanField(
        default=True,
        help_text="Unpublished resources are hidden from the public site.",
    )
    featured = models.BooleanField(
        default=False,
        help_text="Featured resources appear in the Home page teaser.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manual display order; lower numbers appear first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self):
        """A slug unique across Resources, appending -2, -3, ... on a clash."""
        base = slugify(self.title)
        slug = base
        siblings = Resource.objects.exclude(pk=self.pk)
        n = 2
        while siblings.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug


class ContactSubmission(models.Model):
    """A record of a contact-form submission, kept in addition to the
    outbound email so a failed delivery doesn't lose the message."""

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
