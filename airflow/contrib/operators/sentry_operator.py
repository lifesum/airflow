# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Sentry operator
"""
from airflow.models import BaseOperator
from airflow.utils.sentry import send_msg_to_sentry
from airflow.utils.decorators import apply_defaults


class SentryOperator(BaseOperator):
    """
    Send sentry notification
    Notification level is fatal by default

    :param message: sentry notification message
    :param level: notification level (fatal, error, warning, info, debug)
    :param tags: dictionary of tag:value pairs
    :param environment: environment string, eg staging
    :param extra: dictionary of key:value metadata pairs
    :param fingerprint: list of strings for use in hierarchically categorising the error
    :param dsn: Sentry DSN (to allow this operator to be used without [sentry] in airflow.cfg)
    """

    template_fields = ('message', 'environment', 'tags', 'extra')
    ui_color = '#e6faf9'

    @apply_defaults
    def __init__(self, message, level='info', tags=None, environment=None, extra=None,
                 fingerprint=None, dsn=None, *args, **kwargs):
        super(SentryOperator, self).__init__(*args, **kwargs)
        self.message = message
        self.level = level
        self.tags = tags
        self.environment = environment
        self.extra = extra
        self.fingerprint = fingerprint
        self.dsn = dsn

    def execute(self, context):
        send_msg_to_sentry(message=self.message, level=self.level, tags=self.tags,
                           environment=self.environment, extra=self.extra,
                           fingerprint=self.fingerprint, sentry_kwargs=dict(dsn=self.dsn))
