# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'clustaar.webhook'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'

from .events_handler import EventsHandler
from .webhook import Webhook
