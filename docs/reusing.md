# Reusing YADC in other projects.

YADC supplies two basic components: a scraper which does the work, and a browser
which tries to behave like `selenium.webdriver.Chrome`.  Both of these are
reusable, but since reuse of the Scraper is somewhat specialist you are advised
simply to read the source if you want to do so.  Here we focus on the `Browser`
which is of more generic interest.

## Overview

A `Browser()` object launches Chrome, setup for remote controlling.  When used
in a context manager it yields a driver (which is also available on the Browser
object as `._driver`, although as the `_` suggests this is subject to change).
This driver is a subclassed `Chrome()` object: specifically, subclassed to
automatically solve captchas.

Depending on the particular `Browser` you choose to use there are various
combinations:

| Browser                                     | Driver                            | Description                                                                           |
|---------------------------------------------+-----------------------------------+---------------------------------------------------------------------------------------|
| `Browser()`                                 | `CaptchaChrome(webdriver.Chrome)` | A Browser, which will try to solve captchas.                                          |
| `TorBrowser()`                              | `CaptchaChrome(webdriver.Chrome)` | ditto, tunnelled through tor.                                                         |
| `UndetectedBrowser(Browser)`                | `CatpchaChrome(uc.Chrome)`        | ditto, using undetected_chromedriver.                                                 |
| `UndetectedTorBrowser(Browser)`             | `CaptchaChrome(uc.Chrome)`        | ditto, tunnelled through tor.                                                         |
| `ManualBusterUndetectedBrowser(Browser)`    | `CaptchaChrome(uc.Chrome)`        | ditto, manually installing buster on first run and using same profile dir after that. |
| `ManualBusterUndetectedTorBrowser(Browser)` | `CaptchaChrome(uc.Chrome)`        | ditto, tunnelled through tor.                                                         |

Note that these are not the real class relations: the code makes extensive use
of mixins.

Which to use?  The `Manual`- classes were made first, because I couldn't get
plugin installation working with `undetected_chromedriver`.  We since use a
*horrible* hack to make it work (monkeypatching the code which launches chrome)
and setting `shell=True`.  Without doing this I was unable to get `tor` working.
I would love to know why this is necessary.

Note that all these classes behave exactly the same way from your point of view,
except that as you go down the list they need fewer arguments.  If you use a
`Manual`- class you will be prompted to click 'install' the first time chrome
runs.  This is an internal prompt and there is no way to click it with
chromedriver.  After that the *same* profile dir will be reused to keep the
browser on hand, which reduces one source of entropy.  Manually removing the dir
will cause reinstallation.

## Testing

It is highly advisable to run the tests before trying to develop on top of these
classes, as they depend upon being able to run binaries like `tor`.

```bash
python -m pytest tests/
```

If you only want to run automated tests (i.e. not requiring manual input):

```bash
python -m pytest tests/ -m "not manual"
```

Note that these tests will only work if the fixtures in `tests/conftest.py` can
find your binaries.  Either modify the fixtures or move your binaries to the
right places for them to work.
