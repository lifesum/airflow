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
Sentry notifier
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from raven import Client as sentry_client

from airflow import configuration
from airflow.exceptions import AirflowConfigException


def get_sentry_client():
    """
    Method that create a sentry client and return it
    :return: Object -- sentry client
    """
    client = None
    try:
        sentry_dsn_key = configuration.get("sentry", "SENTRY_KEY")
        sentry_env = configuration.get("sentry", "SENTRY_ENVIRONMENT")
        client = sentry_client(sentry_dsn_key, environment=sentry_env)
    except AirflowConfigException:
        logging.debug("Sentry DSN is not found in the configuration")
    return client


def send_msg_to_sentry(msg):
    """
    Method that propagate(send) message to sentry
    :param client: object -- sentry client object
    :param msg: string -- message
    :return: None
    """
    client = get_sentry_client()
    if not client:
        logging.warning("Sentry client is not found, please check sentry configuration")
        return
    sentry_client.captureMessage(msg)
