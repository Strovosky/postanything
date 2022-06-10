from django.forms import Form, CharField, TextInput


class NewComment(Form):
    comment = CharField(max_length=300, label="", widget=TextInput(attrs={'placeholder':'Write your comment...'}))

class NewSubcomment(Form):
    comment = CharField(max_length=300, label="", widget=TextInput(attrs={'placeholder':'Write your comment...'}))

