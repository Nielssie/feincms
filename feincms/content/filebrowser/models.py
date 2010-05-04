# Based on the Media File CT

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from feincms.admin.editor import ItemEditorForm

from filebrowser.fields import FileBrowseField

# FeinCMS connector
class FileBrowserContent(models.Model):
    feincms_item_editor_includes = {
        'head': ['admin/content/filebrowser/init.html'],
    }

    class Meta:
        abstract = True
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    @classmethod
    def initialize_type(cls, POSITION_CHOICES=None):
        if 'filebrowser' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured, 'You have to add \'filebrowser\' to your INSTALLED_APPS before creating a %s' % cls.__name__

        if POSITION_CHOICES is None:
            POSITION_CHOICES=(
                ('block', _('block')),
                ('left', _('left')),
                ('right', _('right')),
            )

        cls.add_to_class('file', FileBrowseField("File", max_length=200, blank=True, null=True))

        cls.add_to_class('position', models.CharField(_('position'), max_length=10, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]))

        class FileBrowserContentAdminForm(ItemEditorForm):
            position = forms.ChoiceField(choices=POSITION_CHOICES, initial=POSITION_CHOICES[0][0],
                                         label=_('position'), widget=AdminRadioSelect(attrs={'class': 'radiolist'}))

        cls.feincms_item_editor_form = FileBrowserContentAdminForm

    def render(self, **kwargs):
        return render_to_string([
            'content/filebrowser/%s_%s.html' % (self.file.filetype, self.position),
            'content/filebrowser/%s.html' % self.file.filetype,
            'content/filebrowser/%s.html' % self.position,
            'content/filebrowser/default.html',
            ], {'content': self})
