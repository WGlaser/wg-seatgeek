"""A credential block for seatgeek containing a key and secret for login."""

from typing import Optional

from prefect.blocks.core import Block
from pydantic import SecretStr


class SeatGeekCredentials(Block):
    """
    Block used for storign Summit Learning Credentials

    Attributes::
        key: key for use with seatgeek API
        secret: secret ffor use with seatgeek API
    Example:
        Load stored seatgeek Credentials:
        ```python
        from credentials import SeatGeekCredentials
        SeatGeekCredentials = SeatGeekCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "SeatGeek Credentials"
    _logo_url = "https://seatgeek.com/images/sg-Spotlight-new.png"
    key: Optional[str] = None
    secret: Optional[SecretStr] = None
