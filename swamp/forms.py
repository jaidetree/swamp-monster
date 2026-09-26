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
