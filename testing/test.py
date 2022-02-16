"""
file: test.py
description: Contains functions for performing testing/fuzzing of a web page
"""

from testing.exploit_strategy import *  # the exploit strategy
from testing.sanitization_exploit import *  # the concrete sanitization exploit
from testing.delayed_response_exploit import *  # the concrete delayed response exploit
from testing.http_response_exploit import *  # the concrete http response code exploit
from testing.sensitive_data_exploit import *  # the concrete sensitive data exploit


def test_pages(pages, session, options):
    """
    test/fuzzes all given pages.
    """

    # set up all exploit strategies
    sanitization = ExploitStrategy(pages, session, SanitizationExploit(), options)
    delayed_response = ExploitStrategy(pages, session, DelayedResponseExploit(), options)
    http_response = ExploitStrategy(pages, session, HttpResponseExploit(), options)
    sensitive_data = ExploitStrategy(pages, session, SensitiveDataExploit(), options)

    # execute all exploit strategies
    sanitization.execute()
    delayed_response.execute()
    http_response.execute()
    sensitive_data.execute()
