from optparse import OptionParser

usage = "Usage: %prog [discover | test] url [OPTIONS]"
parser = OptionParser(usage=usage)

# custom auth option
parser.add_option("--custom-auth", dest="app_to_auth",
                  help="Signal that the fuzzer should use hard-coded authentication for a"
                       "specific application (e.g. dvwa). Optional.", metavar="STRING")

# common words option
parser.add_option("--common-words", dest="common_words",
                  help="Newline-delimited file of common words to be used in page guessing."
                       "Required.", metavar="FILE")

# extensions option
parser.add_option("--extensions", dest="extensions",
                  help="Newline-delimited file of path extensions, e.g. '.php'. Optional. "
                       "Defaults to '.php' and the empty string if not specified", metavar="FILE")

# vectors option
parser.add_option("--vectors", dest="vectors",
                  help="Newline-delimited file of common exploits to vulnerabilities. Required.",
                  metavar="FILE")

# random option
parser.add_option("--sanitized-chars", dest="sanitization",
                  help="Newline-delimited file of characters that should be sanitized from inputs. Defaults to just < "
                       "and >",
                  metavar="FILE")

# slow option
parser.add_option("--slow", dest="slow_ms", default=500,
                  help="Number of milliseconds considered when a response is considered 'slow' \
	                    Default is 500 milliseconds",
                  metavar="NUMBER")

# sensitive data option
parser.add_option("--sensitive", dest="sensitive",
                  help="Newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response. Required.",
                  metavar="FILE")
