"""
Override the hook from pyinstaller-hooks-contrib.
This prevents g2p_en from collecting files that you do not use.
Please collect the NLTK data manually.
"""

excludedimports = ["tkinter"]
