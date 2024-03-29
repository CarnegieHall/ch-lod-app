from django.db.models import TextField
from wagtail.admin.panels import FieldPanel

class MarkdownField(TextField):
    def __init__(self, **kwargs):
        super(MarkdownField, self).__init__(**kwargs)

class MarkdownPanel(FieldPanel):
    def __init__(self, field_name, classname="", widget=None, **kwargs):
        super(MarkdownPanel, self).__init__(
            field_name,
            classname=classname,
            widget=widget,
            **kwargs
        )
        if self.classname:
            self.classname += "markdown"
