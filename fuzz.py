"""
file: fuzz.py
writer : Daniel Cho
"""

# Import the library
import sys
from options import *
from discover import *  # page containing discovery functions
import mechanicalsoup
from testing.test import *  # Module containing page test functions

(options, args) = parser.parse_args()

if len(sys.argv) < 4:

    parser.error("incorrect number of arguments")

else:

    action = sys.argv[1]
    url = sys.argv[2]

    if action == "discover" or action == "test":
        browser = mechanicalsoup.StatefulBrowser()
        session = browser

        # “Click” on the Create/Reset Database (i.e. submit the form)
        browser.open(url + "setup.php")
        browser.select_form('form[action="#"]')
        browser["create_db"] = "Create / Reset Database"
        browser.submit_selected()

        # Ensure that required common-file option is set
        if options.common_words is None:
            parser.error("Newline-delimited file of common words to be used in page guessing. Required.")

        elif options.vectors is None and action == "test":
            parser.error("Newline-delimited file of common exploits to vulnerabilities. Required.")

        elif options.sensitive is None and action == "test":
            parser.error("Newline-delimited file data that should never be leaked. It's assumed that"
                         " this data is in the application's database (e.g. test data), but is not"
                         " reported in any response. Required.")

        else:
            # authentic if applicable to site
            if options.app_to_auth is not None:
                if options.app_to_auth.lower() == "dvwa":
                    # Log in by entering in “admin” and “password”
                    browser.open(url)
                    browser.select_form('form[action="login.php"]')
                    browser["username"] = "admin"
                    browser["password"] = "password"
                    response = browser.submit_selected()

                    # set the security cookie to low!
                    response = browser.open(url + "security.php")
                    browser.select_form()
                    browser["security"] = "low"
                    browser.submit_selected()

            # time to discover
            if options.extensions is None:
                discovered_urls, session = page_discovery_no_extension_file(url, session, options.common_words)
                discovered_pages = list()
            else:
                discovered_urls, session = page_discovery(url, session, options.extensions, options.common_words)
                discovered_pages = list()

            for url in discovered_urls:
                inputs, session = input_discovery(url, session)
                discovered_page = {'url': url, 'inputs': inputs}
                discovered_pages.append(discovered_page)

            if action == "test":
                test_pages(discovered_pages, session, options)

    else:
        parser.error("invalid action")
