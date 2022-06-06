from django.forms import Form, CharField, TextInput


class NewComment(Form):
    comment = CharField(max_length=300, required=True, label="", widget=TextInput(attrs={'placeholder':'Write your comment...'}))
