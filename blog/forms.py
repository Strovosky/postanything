from django.forms import Form, CharField


class NewComment(Form):
    comment = CharField(max_length=300, required=True)

