# Changelog

<!--next-version-placeholder-->

## v0.16.0 (2022-02-17)
### Feature
* **browser:** Even more explicit logging. ([`98cde22`](https://github.com/2e0byo/YADC/commit/98cde22e04de8e829359f9cd7c994e89b4f71385))

### Fix
* **browser:** Only log when we actually wait. ([`48894fb`](https://github.com/2e0byo/YADC/commit/48894fb576e5d0e75bea3107ed5ad2d60ccdd161))

## v0.15.0 (2022-02-02)
### Feature
* **browser:** Enable taking control of browser (terminally). ([`064e2dd`](https://github.com/2e0byo/YADC/commit/064e2dd53a1c4d6ef3d0beeb6227e7fdf82efd71))

### Fix
* **browser:** Handle windoze... ([`9646633`](https://github.com/2e0byo/YADC/commit/96466335f0550cf53f0c43998d963683cc5c09d3))

## v0.14.1 (2022-02-01)
### Fix
* **browser:** We hadn't imported sleep! ([`eb39d43`](https://github.com/2e0byo/YADC/commit/eb39d4301932ce3831d043b7ac1621b152b0e26a))

## v0.14.0 (2022-02-01)
### Feature
* **scraper:** Factor out loop sleep. ([`bd6da75`](https://github.com/2e0byo/YADC/commit/bd6da756e384b05ae43e4514fe1a4943401a954b))

## v0.13.1 (2022-01-31)
### Fix
* **browser:** Typo if -> while ([`ba9938a`](https://github.com/2e0byo/YADC/commit/ba9938a166821cdda5fee97fce7d86efaa36c30e))

## v0.13.0 (2022-01-31)
### Feature
* **scraper:** Add error_callback. ([`670f623`](https://github.com/2e0byo/YADC/commit/670f62316d7ed99f18fd12c91d2706614d74b1a0))

## v0.12.0 (2022-01-31)
### Feature
* **scraper:** Add count log. ([`63c3637`](https://github.com/2e0byo/YADC/commit/63c36375bb54f0ee6211abf13fb2af96fa7bf33e))

## v0.11.0 (2022-01-29)
### Feature
* **browser:** Handle killing for dozy operating systems. ([`cc60e88`](https://github.com/2e0byo/YADC/commit/cc60e88f0226c93526ab2c7f5b3acea2c2b564fb))

### Fix
* **undetected_browser:** Make windoze path handling universal. ([`528e23d`](https://github.com/2e0byo/YADC/commit/528e23dfebfcdc6d05f08a2437072415c9badfdd))

## v0.10.0 (2022-01-29)
### Feature
* **scraper:** Distribute sleeps properly. ([`7402f4f`](https://github.com/2e0byo/YADC/commit/7402f4fafc96459c6a9948f316cfee49abbd5503))
* **browser:** Handle the 'please wait' page which sometimes occurs. ([`9ed5618`](https://github.com/2e0byo/YADC/commit/9ed561826dcc3bdd7fd00662c20e832bb7ea6807))
* **browser:** Improve captcha handling. ([`b0a170e`](https://github.com/2e0byo/YADC/commit/b0a170ec640986a1e09136e77d8f7c64dfbd7e3c))

### Fix
* **scraper:** Actually sleep ([`2835717`](https://github.com/2e0byo/YADC/commit/28357172e52503d9812e8de317af092958858681))
* **browser:** Revert part of incapsula handling. ([`e7eb12b`](https://github.com/2e0byo/YADC/commit/e7eb12b92df847133c66a1fd5290c5fa7e4f71b4))
* **browser:** Wait. ([`6873228`](https://github.com/2e0byo/YADC/commit/6873228c6a7a9605b480198209f89b6c03afe3c4))

## v0.9.0 (2022-01-29)
### Feature
* **scraper:** Take time of current run into account in period. ([`8323a12`](https://github.com/2e0byo/YADC/commit/8323a1222b19f15176169bfce4cd6a618a0a4df7))

## v0.8.1 (2022-01-29)
### Fix
* **browser:** Catch when the captcha has gone. ([`9ef3ab7`](https://github.com/2e0byo/YADC/commit/9ef3ab71bd144fb37850d51a1c140d075803d44b))

### Documentation
* **scraper:** Add docs for scraper. ([`1834ffc`](https://github.com/2e0byo/YADC/commit/1834ffc99ec9b88182ed26292895aecddf334c5d))

## v0.8.0 (2022-01-29)
### Feature
* **browser:** Customisable error period. ([`dbb111d`](https://github.com/2e0byo/YADC/commit/dbb111d0434ba7793c0e9df7729e96dcb8368ab5))

## v0.7.1 (2022-01-28)
### Fix
* **undetected_browser:** Actually use kwargs. ([`da28b8d`](https://github.com/2e0byo/YADC/commit/da28b8d6e9f046fa3ef1e076d87a5251116d2749))

## v0.7.0 (2022-01-28)
### Feature
* **undetected_browser:** Print cmdline for debugging. ([`084bffe`](https://github.com/2e0byo/YADC/commit/084bffebbb196b3d9fbc2715b09a8d3ac8bb19b3))

## v0.6.0 (2022-01-27)
### Feature
* **browser:** Allow passing chrome path for windoze. ([`f67725f`](https://github.com/2e0byo/YADC/commit/f67725f8be6e0ba1acf719e972b4272f5f04903d))

## v0.5.0 (2022-01-27)
### Feature
* **scraper:** Sleep for more predictable time and be verbose. ([`dbe4efb`](https://github.com/2e0byo/YADC/commit/dbe4efbe4022e2a11f22e13123d4be0c009cfbc4))

## v0.4.0 (2022-01-27)
### Feature
* **browser:** Try to kill driver if possible. ([`10648f8`](https://github.com/2e0byo/YADC/commit/10648f8e94b54510930f2f77f23aa9bca99cdbec))
* Undetected_browser classes. ([`81ce832`](https://github.com/2e0byo/YADC/commit/81ce832ada0cbd8feb2a4ddcceaabbe98299be16))

### Fix
* **undetected_browser:** Now works with tor and buster. ([`6d06525`](https://github.com/2e0byo/YADC/commit/6d06525b1c2da09b9e4e727b0fa4b8edbd16a987))
* **undetected tor browser:** Include tor mixin! ([`60e2495`](https://github.com/2e0byo/YADC/commit/60e24957e90a11cdc0c375f9427b8fabae06141d))
* **undetected_browser:** Manual mixin and test. ([`86ff1a7`](https://github.com/2e0byo/YADC/commit/86ff1a717b170b1e6138349d59a7a300917140c3))

### Documentation
* Browsers. ([`d9ce7d3`](https://github.com/2e0byo/YADC/commit/d9ce7d3c07974ce7c69313b781d9de0067d1907b))

## v0.3.2 (2022-01-26)
### Fix
* Leftover uc breaking typehint. ([`b519f8d`](https://github.com/2e0byo/YADC/commit/b519f8d39a1492416689574a102358b7be312a6c))
* Drop undetected_chromedriver and fix return. ([`7d900a7`](https://github.com/2e0byo/YADC/commit/7d900a7dc393453d53fde5478588bba515beefae))

## v0.3.1 (2022-01-26)
### Fix
* No longer static method. ([`4da97c7`](https://github.com/2e0byo/YADC/commit/4da97c79968e31a16bc502baa6cadfc97af81611))
* Datetime.combine. ([`2a4707b`](https://github.com/2e0byo/YADC/commit/2a4707b2e5de41c331af31b88edc2ea843676ed6))

## v0.3.0 (2022-01-26)
### Feature
* **scraper:** Click on entry if desired. ([`e45dddb`](https://github.com/2e0byo/YADC/commit/e45dddb88900e4858e0f18b5de2321e7aab6853b))

### Documentation
* Update readme. ([`4d9e441`](https://github.com/2e0byo/YADC/commit/4d9e441375ca58420fc42c4bba66ab85dd04d821))

## v0.2.1 (2022-01-26)
### Fix
* Correct log setting code. ([`415d923`](https://github.com/2e0byo/YADC/commit/415d92302ecc68d3d8ded387039feb6a59e498f5))

### Documentation
* Add readme. ([`8a9b8cf`](https://github.com/2e0byo/YADC/commit/8a9b8cf2f1ac8950dd5ec43b4c0fdc5991366896))

## v0.2.0 (2022-01-26)
### Feature
* **scraper:** (unused) running property to permit pausing later. ([`af0ff83`](https://github.com/2e0byo/YADC/commit/af0ff83d63b05035b12dd167b9b4169a2803a1a4))

### Fix
* **scraper:** Correct closing/opening logic. ([`1ef5f53`](https://github.com/2e0byo/YADC/commit/1ef5f5395982d12e5c931311ec5278bf3ac65dd8))
* Typo. ([`b940ccc`](https://github.com/2e0byo/YADC/commit/b940ccc98c37389f3beac5b70ac09694554d6f4b))
* Actually call self._errorfn(). ([`a8a9b5b`](https://github.com/2e0byo/YADC/commit/a8a9b5bc192ce47c8aa275edda42bf1e38ee5f88))
* **browser:** Slugify wasn't enough, use strftime. ([`ebe1357`](https://github.com/2e0byo/YADC/commit/ebe1357ecfd98bfca4c90385512fc76bffbc99a1))
* **browser:** Use slugified timestamp coz windows is rubbish :p ([`f9714ec`](https://github.com/2e0byo/YADC/commit/f9714ecdc681f02831398b5671391439be2ab705))
* **browser:** Make error dumping function a bit more robust. ([`6917e02`](https://github.com/2e0byo/YADC/commit/6917e02365e813a79766a589abb242800c354826))

### Documentation
* Update. ([`7e3ff3a`](https://github.com/2e0byo/YADC/commit/7e3ff3a6791519c7679bf9dd55cf19d8123ce9c4))
