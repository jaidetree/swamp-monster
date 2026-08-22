"""Forms for the `content` app."""

from django import forms


class ContactForm(forms.Form):
    """The public contact form: name/email/message, server-side validated.

    Backs both the `ContactSubmission` row and the Postmark notification
    email sent by `content.views.contact`.
    """

    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
