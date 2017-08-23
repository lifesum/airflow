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

    :param sentry_dsn: sentry DSN
    :type sentry_dsn: string 
    :param message: sentry notification message
    :type message: string
    :param environment: sentry environment
    :type environment: string
    :param level: notification level (fatal, error, warning, debug)
    :type level: string
    """

    template_fields = ('message',)
    template_ext = ('.html',)
    ui_color = '#e6faf9'

    @apply_defaults
    def __init__(
            self,
            sentry_dsn,
            message,
            environment='',
            level='fatal',
            *args, **kwargs):
        super(SentryOperator, self).__init__(*args, **kwargs)
        self.sentry_dsn = sentry_dsn
        self.message = message
        self.environment = environment
        self.level = level
        

    def execute(self, context):
        send_msg_to_sentry(msg=self.message, environment=self.environment, level=self.level)
