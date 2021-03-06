from django.db import models
from django.db.models import query
from datetime import datetime

from premises.constants import FEATURED_CONTENT_COUNT


class DeletePreventionQueryset(query.QuerySet):
    def delete(self):
        return super(DeletePreventionQueryset, self).update(
            is_deleted=True, deleted_at=datetime.now())

    def hard_delete(self):
        return super(DeletePreventionQueryset, self).delete()


class DeletePreventionManager(models.Manager):

    def get_queryset(self):
        queryset = DeletePreventionQueryset(self.model, using=self._db)
        return queryset.filter(is_deleted=False)

    def deleted_set(self):
        queryset = DeletePreventionQueryset(self.model, using=self._db)
        return queryset.filter(is_deleted=True)

    def all_with_deleted(self):
        return DeletePreventionQueryset(self.model, using=self._db)


class ContentionManager(DeletePreventionManager):
    def featured(self):
        return self.filter(is_featured=True)
