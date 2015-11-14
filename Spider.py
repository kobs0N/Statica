# Issues - Many #

# Save Extension to Files
# Many URL Errors
# Performance Issues
# True Negative domain gather
# Threading ?


# Imports
import urllib2
import os
import time
import httplib

pages_list = []
domain = ""
counter = 0


def pages_scan(url):
    global domain, counter
    domain = get_domain_name(url)
    print "Domain: ", domain

    folder = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(folder):
        os.makedirs(domain)

    print folder + "\\" + domain
    page_downloader(url, folder + "\\" + domain + "\\")
    print "Found" ,counter


def page_downloader(url, location):
    global domain, counter
    print "Working now on ", url
    counter += 1
    pages_list.append(url)

    response = ""
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print "Http Error"
        return

    try:
        html = response.read()
    except httplib.IncompleteRead:
        # We got blocked
        print "Error on ", url
        return

    tmp_url = remove_chars(url[url.index("://") + 3:])
    fo = open(location + tmp_url, "w")
    fo.write(html)
    fo.close()
    places = find_all(html.lower(), "http")

    for place in places:
        new_tested_url = html[place:place+70]

        if domain == get_domain_name(new_tested_url):
            # Also fix this
            new_tested_url = secured_index(new_tested_url, " ")
            new_tested_url = secured_index(new_tested_url, "\"")
            new_tested_url = secured_index(new_tested_url, "\'")

            if does_exists(new_tested_url) is True:
                continue
            else:
                pages_list.append(new_tested_url)
                page_downloader(new_tested_url, location)


def does_exists(new_url):
    try:
        index = pages_list.index(new_url)
        return True
    except ValueError:
        return False


def find_all(text, sub):
    result = []
    index = 0
    while index < len(text):
        index = text.find(sub, index)
        if index == -1:
            return result
        else:
            result.append(index)
            index += 1
    return result


def remove_chars(url):
    length = len(url)
    print length
    index = 0
    while index < length - 1:
        if url[index] is '/' or url[index] is '? ' or url[index] is '@':
            # Need to do some benchmarking
            url = url[:index - 1] + "." + url[index + 1:]
        index += 1
    return url

# Need to make this function better, many true - negative
def get_domain_name(url):
    url = url[url.index(".") + 1:]
    return secured_index(url, "/")


def secured_index(url, index):
    try:
        return url[:url.index(index)]
    except ValueError:
        return url
