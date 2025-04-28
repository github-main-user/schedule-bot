from itertools import chain

from .schedule import schedule_handlers
from .special import special_handlers
from .subscribers import command_handlers

all_handlers = list(chain(schedule_handlers, special_handlers, command_handlers))
