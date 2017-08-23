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


def _get_config(section, key):
    """
    Get airflow key from the configurtion section
    :param section: configuration section
    :type section: string
    :param key: key in airflow configuration
    :type key: string
    :returns string
    """
    value = None
    try:
        value = configuration.get(section, key)
    except AirflowConfigException as ex:
        logging.debug(
            "Error getting key %s from section %s. Reason: %s", key, section, str(ex))
    return value


def get_sentry_client(sentry_dsn='', environment=''):
    """
    Method that create a sentry client and return it
    :param sentry_dsn: Sentry DSN
    :type sentry_dsn: string
    :param environment: sentry environment
    :type environment: string
    :return: Object -- sentry client
    """
    if not sentry_dsn:
        sentry_dsn = _get_config("sentry", "SENTRY_DSN")
    if not environment:
        environment = _get_config("sentry", "SENTRY_ENVIRONMENT")
    client = sentry_client(sentry_dsn, environment=environment)
    return client


def send_msg_to_sentry(msg, environment='', level='fatal'):
    """
    Method that propagate(send) message to sentry
    :param msg: sentry message
    :type msg: string
    :param environment: sentry environment
    :type environment: string
    :param level: level of the message (fatal, error, warning, debug)
    :type level: string
    :return: None
    """
    client = get_sentry_client(environment=environment)
    try:
        client.captureMessage(message=msg, level=level)
    except Exception as ex:
        logging.error("Failed to send message to sentry. Reason: %s", str(ex))
        