import factory

from content.models import Work, WorkImage


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
