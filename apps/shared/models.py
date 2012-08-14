from django.conf import settings
from django.db import models

from product_details import product_details
from tower import ugettext as _


ENGLISH_LANGUAGE_CHOICES = sorted(
    [(key.lower(), u'{0} ({1})'.format(key, value['English']))
     for key, value in product_details.languages.items()]
)


class ModelBase(models.Model):
    """Common functions that models across the app will need."""

    def __init__(self, *args, **kwargs):
        super(ModelBase, self).__init__(*args, **kwargs)

        # Cache localized attributes
        self._localized_attrs = {}

    def localized(self, attr):
        """Return a localized version of the requested attribute."""
        if attr not in self._localized_attrs:
            self._localized_attrs[attr] = _(getattr(self, attr))

        return self._localized_attrs[attr]

    class Meta:
        abstract = True


class MultiTableParentModel(ModelBase):
    """
    Provides boilerplate for models that will be the parent in a multi-table
    inheritence relationship.
    """
    child_type = models.CharField(max_length=255, editable=False)

    def save(self, *args, **kwargs):
        """Set type to our classname on save."""
        if not self.child_type:
            self.child_type = self.__class__.__name__.lower()
        return super(MultiTableParentModel, self).save(*args, **kwargs)

    def child(self):
        """Return this instance's child model instance."""
        return getattr(self, self.child_type)

    class Meta:
        abstract = True


class LocaleField(models.CharField):
    description = ('CharField with locale settings specific to Affiliates '
                   'defaults.')

    def __init__(self, max_length=32, default=settings.LANGUAGE_CODE,
                 choices=ENGLISH_LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)


class LocaleImage(ModelBase):
    image = models.ImageField(upload_to=settings.LOCALE_IMAGE_PATH,
                              max_length=settings.MAX_FILEPATH_LENGTH)
    locale = LocaleField()

    class Meta:
        abstract = True


# South introspection rules for LocaleField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^shared\.models\.LocaleField'])
