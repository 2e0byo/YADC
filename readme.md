# YADC: Yet Another (DVSA) cancellations Checker

YADC is yet another checker for driving cancellations in the UK.

-   **why another?:** Because all the code I found on github doesn't work with the
    latest anti-bot protections on dvsa.  Besides, it was all rather
    spaghettified.  YADC is, I hope a little cleaner and more modular.  It should
    be easier to modify down the line.
-   **why a bot?:** Because I can't get a driving test.  Note that I *do not think*
    this solution is remotely ideal.  See the appeal below.
-   **will you maintain this?:** Not if I get a test and pass.  But hopefully it
    should be a better framework for the next generation to come along and do the
    same.



# Features

YADC is:

-   cleanly written and object-oriented
-   neat.  We use a context manager to handle the browser; I'm pretty proud of
    that.
-   easy to extend
-   easy (hopefully) to get around the next rubbish DVSA put up
-   pretty immune to blocking (thanks to TOR)
-   pretty colourful, too. We have coloured logs (thanks to `coloredlogs`),
    spinners (thanks to `Halo`) and well-formatted output. When things go wrong,
    we save a traceback, a screenshot, and the html the browser was seeing.

YADC is not:

-   my idea.  I started with [this repo](https://github.com/tp223/Driving-Test-Cancellations) and extensively rewrote the logic from
    the ground up.  I got the idea of the poisson sleep from [this repo](https://github.com/birdcolour/dvsa-practicals), although
    I didn't take any code directly from anything.
-   infallible
-   capable of booking tests for you (thanks to @chrishat34 it will reserve them, though).
-   always going to work
-   properly supported



# Installation

## With pip

`YADC` is now deployed on PyPi, so you can just

```bash
python3 -m pip install YADC
```

However, since every individual setup is going to vary somewhat, `YADC` *is only
a library*.  You still have to decide how to use it.  A starting point is
provided in the `main.py` of this repository: save it somewhere, edit it, and
off you go.  A dummy CLI is provided which will merely direct you to do this ;)

If anyone wishes to write a proper CLI I will happily merge it.

Note that if you want captcha defeating you need to download [buster](https://github.com/dessant/buster/releases) and unzip it
somewhere you can get at from your `main.py`.  Likewise if you want `tor`, it
needs to be installed and executable as the user running your \`main.py\`.


## From git (for development).

-   clone the repo
-   run `poetry install`
-   run `poetry shell`
-   (optional) to download [buster](https://github.com/dessant/buster/releases) and unzip it.
-   (optional) install `tor` and ensure it can be run as a user.
-   edit `main.py` with your setup.
-   run `python -m yadc.main`

# FAQ

- **Chrome/Chromedriver/Tor doesn't start!** You need to provide either the
  *complete* path to the executable (that's something like
  `"/usr/bin/chromedriver"` or `r"C:\Program Files\Chrome\chrome.exe ""`)
  *including any suffix it might have*; or you need to make sure that the
  executables are in your `$PATH` / `%PATH%`.  Have a look in `main.py` to see
  where they should go. Windows users: I'm very sorry your operating system
  makes this so difficult, it wasn't me who decided to put a *space* in the path
  to further confuse things.
  
- **Tor doesn't connect to the internet.**  This is *probably* a bug in your
  environment *if* you have correctly passed the tor executable.  If you
  haven't, do so.  Verify that one and only one tor process is running (for some
  reason multiple tor processes will fail on Windows at least), using Task
  Manager (Micro$oft Windoze) or `pkill` (*nix) to stop any which are left over
  by mistake.  If you can't get it working, try manually: start tor with
  `/path/to/tor --SocksPort 48059` and then start chrome with `/path/to/chrome
  --proxy-server="socks4://localhost:48059"`.  If this fails the problem is in
  your installation: if it succeeds and you can't get it running, open an issue
  and I'll have a look at it.  Note that this code has been confirmed working on
  both Windows and Linux in the past, but it is not in active development, and
  it's possible things have broken since.
  
- **I don't know where to start!** If you can't make sense of the instructions
  in this readme, open an issue and explain what's confusing.  That way I can
  improve the readme :D

- **I got this error when it was running!**  Note that errors when running are
  perfectly normal.  YADC gets detected eventually; sooner or later it will
  probably stop working entirely.  See my appeal to the DVSA below.  If you want
  to open an issue with the error, make sure you include the error dump from the
  errors dir (the `.txt`, the `.html`, and the `.png`).  You are strongly
  advised to sanitise the files *first* in case they contain personal data.

# Usage

Currently you have to be at the computer to do anything.  You will see the
browser moving, which should help.  If you want to interact with it manually,
hit `Ctrl-z` in the terminal to stop execution of the script, and the browser
is yours (note that manual interaction increases the chance of being detected
by some anti-bot measures).  If the script finds a test it will notify you
with the notify function you set (the default is just \`print\`, so do set
something more appropriate!  A nice service is \`pushover\`, though it does have
a once-off payment).  If the script does find a test it will block


# Roadmap / Good first PRs

-   [ ] Work in `undetected_browser.py` would make it possible to use
        `undetected_chromedriver`.  A PR implementing this would be welcome.
-   [ ] We have no cli.  That's probably not an issue, but it would be trivial
    to add one, e.g. with click.
    
# Use in other projects

YADC has been written to be reusable.  See [docs/reusing](docs/reusing.md) for
pointers.


# Appeal to DVSA

The current situation is a mess.  Because of the pandemic, there are no tests
for months; that is not your fault.  So we are all forced either to wait for
months, or to book a last-minute cancellation. But we can't do that, because
all the companies using bots to find tests snatch them up.  So we all use
those companies; and then DVSA's website becomes even more useless.  There
are two **easy** solutions you could adopt:

-   Add an auto-booking with queue feature to the website.  Once a test is
    booked you get to specify criteria for a better test, and enter in a queue.
    When you rise to the top of that queue, you get whatever matches reserved
    for you.  In other words, implement the third-party solution yourself.  I
    would gladly pay a reasonable sum for it.  And the third-party firms will
    go out of business and stop spamming your website.

-   Add an API, and charge for access.  That way the third parties will use the
    API.  You can release tests to the API after x minutes to give humans a
    chance as well.  You can go after anyone who tries to use a bot to get
    round the limit, and providing your API is reasonable, nobody will mind.

Instead of these, you make the already useless website even harder to use.
Bot protection is an uphill battle.  So is bot developing.  The only people
who profit from this are companies like google (via chrome/chromium).

