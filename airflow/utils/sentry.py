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
from airflow import configuration, __version__
from airflow.exceptions import AirflowConfigException

HAS_RAVEN = False
try:
    from raven import Client
    from raven.versioning import fetch_git_sha
    HAS_RAVEN = True
except ImportError:
    logging.info("raven is not installed.")


def get_sentry_client(dsn=None, site=None, name=None, release=None,
                      environment=None, tags=None, **kwargs):
    """
    Create a sentry client and return it. Options are taken (in order) from function arguments,
    environment variables (`AIRFLOW__SENTRY__SENTRY_DSN`) or airflow.cfg ([sentry];sentry_dsn=...)

    :param dsn: Sentry DSN secret
    :param site: String identifying the installation
    :param name: Overrides the servers hostname if specified
    :param release: Version string; defaults to SHA1 hash of the HEAD git commit in dags_folder
    :param environment: Environment string, eg staging or production
    :param tags: Dictionary of default tag:value pairs (merged when sending a message)
    :param kwargs: Extra arguments are passed to raven.Client()
    :return: Object -- sentry client
    """

    def try_get_config(k):
        try:
            return configuration.get("sentry", "sentry_{}".format(k))
        except AirflowConfigException:
            pass

    if dsn is None:
        dsn = try_get_config("dsn")
    if site is None:
        site = try_get_config("site")
    if name is None:
        name = try_get_config("name")
    if release is None:
        release = try_get_config("release")
        if release is None:
            dags_folder = try_get_config("core", "dags_folder")
            release = fetch_git_sha(dags_folder)
    if environment is None:
        environment = try_get_config("environment")
    # tags is a dictionary and cannot be fetched from env/config

    return Client(dsn=dsn, site=site, name=name, release=release,
                  environment=environment, tags=tags, **kwargs)


def send_msg_to_sentry(message, level="info", extra=None, tags=None, fingerprint=None,
                       culprit=None, time_spent=None, sentry_kwargs=None, **kwargs):
    """
    Send a message to sentry.

    In addition to the message, the following parameters can be provided:
     - level: fatal, error, warning, info, debug
     - tags: dict of tag: value pairs
     - environment: current env - eg, staging
     - modules: dict of module: version pairs, for relevant software versions
     - fingerprint: list of strings used to hierarchically classify events
     - extra: dict of arbitrary metadata
    :param message: sentry message
    :type message: string
    :param level: logging level - fatal, error, warning, info, debug
    :param extra: dict of metadata to pass with this message
    :param tags: dict of tags to pass with this message
    :param fingerprint: list of strings for use in hierarchically categorising the error
    :param sentry_kwargs: dict of parameters to sentry.Client
    :param time_spent: integer number of milliseconds for the duration of the error
    :param sentry_kwargs: dictionary of keyword arguments to sentry.Client
    :param kwargs: extra arguments are passed to captureMessage()
    :return: None
    """
    if not HAS_RAVEN:
        return

    if sentry_kwargs is None:
        sentry_kwargs = {}
    try:
        client = get_sentry_client(**sentry_kwargs)
        client.captureMessage(message=message, level=level, extra=extra, tags=tags,
                              fingerprint=fingerprint, time_spent=time_spent, **kwargs)
    except Exception as ex:
        logging.error("Failed to send message to sentry. Reason: %s", str(ex))
