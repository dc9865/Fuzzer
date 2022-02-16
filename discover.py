"""
file: discover.py
writer : Daniel Cho
"""
from bs4 import BeautifulSoup # for parsing web pages
from urllib.parse import *  # for parsing the domain of a url


def page_discovery_no_extension_file(url, session, common_words_file):
    """
	Crawls and guesses pages, including link discovery and page
	guessing (without the extension list).
	"""

    print("Crawling for pages")
    discovered_urls = link_discovery(url, session)
    page_guessing_no_extension_file(url, session, discovered_urls, common_words_file)

    return discovered_urls, session

def page_discovery(url, session, extensions_file, common_words_file):
    """
	Crawls and guesses pages, including link discovery and page
	guessing (with the extension list).
	"""

    print("Crawling for pages")
    discovered_urls = link_discovery(url, session)
    page_guessing(url, session, discovered_urls, extensions_file, common_words_file)

    return discovered_urls, session



def link_discovery(url, session):
    """
	Discovers all accessible links in the same domain
	given a page. Returns a list of urls found.
	"""
    max_depth = 100  # huge sites -> horrific performance w/ recursion
    parsed_url = urlparse(url)
    domain = '{url.scheme}://{url.netloc}'.format(url=parsed_url)
    print("Links Discovered:")
    print("**************************************")

    urls = recursive_link_search(url, domain, [], session, max_depth, 0)

    return urls


def recursive_link_search(url, domain, urls, session, max_depth, depth):
    """
    Helper function for link_discovery.
    """
    if depth == max_depth:
        return

    # Add page if never seen before
    print(url)
    if url not in urls:
        urls.append(url)

    page = session.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    for link in soup.find_all('a'):
        href_absolute = urljoin(url, link.get('href'))
        # Only include links in our domain and not seen before
        if href_absolute.startswith(domain) and href_absolute not in urls:
            recursive_link_search(href_absolute, domain, urls, session, max_depth, depth + 1)

    return urls

def page_guessing_no_extension_file(url, session, discovered_urls, common_words_file):
    """
    Use the common word list without the extension list to discover potentially unlinked pages.
    """

    try:
        common_pgs = open(common_words_file, "r").read().splitlines()
    except:
        print("list of common words file not found: " + common_words_file)
        return

    print("Pages Successfully Guessed:")
    print("*************************************")
    for pg in common_pgs:
            possible_pg = session.get(url + "/" + pg + ".php")

            # is this possible page not been seen before?
            if possible_pg.status_code < 300 and possible_pg.url not in discovered_urls:
                print(possible_pg.url)
                discovered_urls.append(possible_pg.url)

def page_guessing(url, session, discovered_urls, extensions_file, common_words_file):
    """
    Use the common word list with the extension list to discover potentially unlinked pages.
    """
    common_ext = open(extensions_file, "r").read().splitlines()

    try:
        common_pgs = open(common_words_file, "r").read().splitlines()
    except:
        print("list of common words file not found: " + common_words_file)
        return

    print("Pages Successfully Guessed:")
    print("*************************************")
    for pg in common_pgs:
        for ext in common_ext:
            possible_pg = session.get(url + "/" + pg + "." + ext)

            # is this possible page not been seen before?
            if possible_pg.status_code < 300 and possible_pg.url not in discovered_urls:
                print(possible_pg.url)
                discovered_urls.append(possible_pg.url)


def form_discovery(url, session):
    page = session.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    forms = list()

    for form_element in soup.findAll('form'):

        form = {'action': '', 'name': '', 'method': '', 'inputs': list()}

        if form_element.has_key('name'):
            form['name'] = form_element['name']

        if form_element.has_key('action') and form_element.has_key('method'):
            form['action'] = form_element['action']
            form['method'] = form_element['method']

            forms.append(form)

            print("--form '%s' found" % (form_element['action']))

            for input_field in form_element.findAll('input'):
                if input_field.has_key('name'):
                    form['inputs'].append(input_field['name'])
                    print("--input field '%s' found" % (input_field['name']))

    return forms, session


def cookie_discovery(session):

    page_cookies = session.get_cookiejar()

    print("Discovering cookies:")
    cookies = list()

    for cookie_found in page_cookies:
        cookie = {"name": cookie_found.name, "value": cookie_found.value}
        cookies.append(cookie)
        print("--cookie found: %(name)s=%(value)s" % cookie)

    return cookies, session


def input_discovery(url, session):
    """
    Crawls a page to discover all possible ways to input data into the system.
    """

    print("Discovering inputs for %s : " % url)
    forms, session = form_discovery(url, session)
    cookies, session = cookie_discovery(session)

    return {'cookies': cookies, 'forms': forms}, session
