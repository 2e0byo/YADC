import logging
from datetime import datetime
from pathlib import Path
import coloredlogs

from yadc.browser import Browser, TorBrowser
from yadc.scraper import Driver, Scraper, Test, Centre

coloredlogs.increase_verbosity()  # for testing


def notify(msg):
    """Put notification code here."""
    print(msg)
    play_loud_aler_sound()


# define a driver.  You can define as many as you like.
# note that the code will only search for one driver at a time.
driver = Driver(
    licence_number="YOUR_NUMBER",
    booking_ref="YOUR_REF",
    not_before=datetime(2021, 12, 10),
    not_after=datetime(2022, 3, 1),
    name="",
    centres=[
        Centre(centre="Gateshead", not_after=datetime(2022, 1, 1)),
        Centre(centre="Durham"),
    ],
)

# get a scraper for a driver or drivers.
s = Scraper(
    TorBrowser(
        buster=Path("buster"),
        chrome="chromium",
        tor=Path("/path/to/tor"),  # probably not needed on *nix
    ),
    [driver],
    notify=notify,
    reserve=True,  # reserve a test if we find it
)

# run the scraper.  I'm a bit too addicted to callable objects...
s()
