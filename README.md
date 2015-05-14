xcode-tool
=========================================

This project has 2 components:

1. `genstrings.py` - Replace Apple's closed sourced genstrings with a Python replacement. origin from project [samwize/localized](https://github.com/samwize/localized)

2. `zhs2t.py` - Auto genrate zh-Hant.lproj/Localizable.strings basing zh-Hans.lproj/Localizable.strings using opencc for translate. opencc can be installed by brew. opencc-python must use https://github.com/lepture/opencc-python. pip version is too old. 


Python genstrings
-----------------

Note: The python script `genstrings.py` is heavily copied from: https://github.com/dunkelstern/Cocoa-Localisation-Helper

Place the script `genstrings.py` in your Xcode project folder.

Run the script

	python genstrings.py

Or if you want to write to the `Localizable.strings` file,

	python genstrings.py > Localizable.strings


The script will read all `.m` `.mm` `.h` files (including subdirectories), and scan for all `NSLocalizedString` and `I(@"localstring")` codes.

The strings will be grouped by their filename (instead of alphabetically in Apple's genstrings tool), which makes much more sense!

It also scan for `I(@"localstring")` code, which is a Macro for NSLocalizedString with recursive replacement. 

`#define I(str) NSLocalizedString(str, @"")`
