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

HAS_RAVEN = False
try:
    from raven import Client
    HAS_RAVEN = True
except ImportError:
    logging.info("raven is not installed.")


def get_sentry_client(**kwargs):
    """
    Create a sentry client and return it. Options are read (in order)
    from **kwargs, environment variables and the airflow config file.

    Known options: dsn, site, name, release, environment, tags
    :param kwargs: keyword options understood by raven.Client
    :return: Object -- sentry client
    """
    arg_names = ["dsn", "site", "name", "release", "environment", "tags"]
    for arg in arg_names:
        if arg not in kwargs:
            config_arg_name = "sentry_{}".format(arg.upper())
            if configuration.has_option("sentry", config_arg_name):
                kwargs[arg] = configuration.get("sentry", config_arg_name)

    if "release" not in kwargs:
        kwargs["release"] = __version__

    return Client(**kwargs)


def send_msg_to_sentry(message, sentry_kwargs=None, **kwargs):
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
    :param sentry_kwargs: dict of parameters to sentry.Client
    :param kwargs: parameters to sentry.captureMessage
    :return: None
    """
    if not HAS_RAVEN:
        return

    if sentry_kwargs is None:
        sentry_kwargs = {}
    try:
        client = get_sentry_client(**sentry_kwargs)
        client.captureMessage(message=message, **kwargs)
    except Exception as ex:
        logging.error("Failed to send message to sentry. Reason: %s", str(ex))
