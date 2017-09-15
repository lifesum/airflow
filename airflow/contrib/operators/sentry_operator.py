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
    :type message: string
    :param level: notification level (fatal, error, warning, info, debug)
    :type level: string
    :param sentry_kwargs: dict of arguments to raven.Client (eg, "dsn")
    :param message_kwargs: dict of arguments to sendMessage (eg, "fingerprint")
    """

    template_fields = ('message', )
    ui_color = '#e6faf9'

    @apply_defaults
    def __init__(self, message, level='info',
                 sentry_kwargs=None, message_kwargs=None,
                 *args, **kwargs):
        super(SentryOperator, self).__init__(*args, **kwargs)
        self.message = message
        self.level = level
        self.sentry_kwargs = sentry_kwargs
        self.message_kwargs = message_kwargs
        if message_kwargs is None:
            self.message_kwargs = {}

    def execute(self, context):
        send_msg_to_sentry(message=self.message, level=self.level,
                           sentry_kwargs=self.sentry_kwargs, **self.message_kwargs)
