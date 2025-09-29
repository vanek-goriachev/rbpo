# Все импорты ниже помечены как noqa потому что они сделаны для применения сайд-эффектов.
# Питон это проклятый язык.

from app.transport.rest.fast_api.public.app import *  # noqa: F403
from app.transport.rest.fast_api.public.exception_handlers import *  # noqa: F403
from app.transport.rest.fast_api.public.post import *  # noqa: F403
