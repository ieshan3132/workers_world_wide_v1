from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    featured_image = forms.FileField()
    
    # To Assign a class to the field so that it can be edit using CSS.
    # Here we assigned the class as input.
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        #self.fields['title'].widget.attrs.update({'class': 'input'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Vote here!',
            'body': 'Add a comment'
        }

        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)

            # self.fields['title'].widget.attrs.update({'class': 'input'})

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

