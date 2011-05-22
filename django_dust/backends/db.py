from django_dust.backends.base import BaseRetryStorage
from django_dust.models import Retry

class RetryStorage(BaseRetryStorage):
    """Database storage for the retry queue, using a Django model."""

    fields = BaseRetryStorage.fields + ['id']

    def count(self):
        return Retry.objects.count()

    def all(self):
        return map(self._to_dict, Retry.objects.all())

    def create(self, **kwargs):
        for key in kwargs.iterkeys():
            if key not in self.field:
                raise ValueError('Illegal retry object field: %s', key)
        Retry.objects.create(**kwargs)

    def delete(self, retry):
        Retry.objects.get(pk=retry['id']).delete()

    def filter_by_filename(self, filename):
        return map(self._to_dict, Retry.objects.filter(filename=filename))

    def _to_dict(self, instance):
        return dict((field, getattr(instance, field)) for field in self.fields)
