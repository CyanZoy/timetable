from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SchedulerConfig(AppConfig):
    # verbose_name = _("图书预订")
    verbose_name = "课表管理"
    name = 'scheduler'
