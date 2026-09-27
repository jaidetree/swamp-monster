"""Forms for the `swamp` app."""

from django import forms

#: Blank first choice acts as a placeholder — required=True below rejects it,
#: so visitors must actively pick a subject.
SUBJECT_CHOICES = [
    ("", "Select a subject"),
    ("Question", "Question"),
    ("Business Inquiry", "Business Inquiry"),
    ("Training", "Training"),
    ("Other", "Other"),
]


class ContactForm(forms.Form):
    """The public contact form: subject/name/email/message, server-side
    validated.

    Backs both the `ContactSubmission` row and the Mailjet notification
    email sent by `swamp.views.contact`. Field order here drives the
    rendered order in `templates/swamp/contact.html`, which loops over
    `form` fields as declared.
    """

    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class MultipleDateInput(forms.DateInput):
    """A date input repeatable under one shared name (`target_dates` in
    `training.html`'s "add another date" rows), so it must collect every
    submitted value rather than just the last — the way `SelectMultiple`
    collects every selected `<option>` instead of one.
    """

    def value_from_datadict(self, data, files, name):
        return [value for value in data.getlist(name) if value]

    def value_omitted_from_data(self, data, files, name):
        return name not in data


class MultipleDateField(forms.Field):
    """One or more target dates for a `TrainingRequestForm`.

    Not `forms.MultiValueField`, which splits *one* logical value across
    several differently-purposed widgets (e.g. a date split into
    year/month/day) — this is N repeats of the same widget instead.
    """

    widget = MultipleDateInput

    def to_python(self, value):
        if not value:
            return []
        date_field = forms.DateField()
        return [date_field.clean(raw) for raw in value]

    def validate(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages["required"], code="required")


class TrainingRequestForm(forms.Form):
    """The training-request form at the bottom of the Training landing page.

    Same shape as `ContactForm` (name/email/message) but `subject` is fixed
    to "Training" by `swamp.views.training` rather than visitor-chosen, and
    adds `target_dates` so a visitor can propose one or more session dates.
    """

    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    target_dates = MultipleDateField()
    message = forms.CharField(widget=forms.Textarea)
