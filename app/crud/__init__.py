# This file makes the crud directory a Python package
from .plazas import (
    get_plaza,
    get_plazas,
    create_plaza,
    update_plaza,
    delete_plaza
)

from .locales import (
    get_locale,
    get_locales,
    create_locale,
    update_locale,
    delete_locale
)
