import factory

from content.models import ContactSubmission, Resource, Training, Work, WorkImage


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Work

    title = factory.Sequence(lambda n: f"Work {n}")
    order = factory.Sequence(lambda n: n)
    published = True


class WorkImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkImage

    work = factory.SubFactory(WorkFactory)
    order = factory.Sequence(lambda n: n)
    # A real (Pillow-generated) image so ImageField validation passes.
    image = factory.django.ImageField(width=800, height=600, format="JPEG")


class TrainingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Training

    title = factory.Sequence(lambda n: f"Training {n}")
    order = factory.Sequence(lambda n: n)
    published = True


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    title = factory.Sequence(lambda n: f"Resource {n}")
    order = factory.Sequence(lambda n: n)
    published = True
    # A real file (with content) so FileField validation and reads pass.
    file = factory.django.FileField(
        filename="resource.pdf", data=b"%PDF-1.4 sample resource content"
    )


class ContactSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactSubmission

    name = factory.Sequence(lambda n: f"Contact {n}")
    email = factory.Sequence(lambda n: f"contact{n}@example.com")
    message = "Hello, I'm interested in a custom piece."
