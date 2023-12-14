from django.utils.translation import gettext_lazy as _


class Role:
    ADMIN = "admin"
    INVESTOR = "investor"

    choices = (
        (ADMIN, _("admin")),
        (INVESTOR, _("investor")),
    )
