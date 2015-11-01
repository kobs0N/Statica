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
    print counter


def page_downloader(url, location):
    global domain, counter
    print "Working now on ", url
    counter = counter + 1
    pages_list.append(url)

    response = ""
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return

    try:
        html = response.read()
    except httplib.IncompleteRead:
        # We got blocked
        print "Error on ", url
        return

    # Not Efficient Line
    tmp_url = url[url.index("://") + 3:].replace("/", ".").replace("@", ".").replace("?", ".")
    fo = open(location + tmp_url, "w")
    fo.write(html)
    fo.close()

    places = find_all(html.lower(), "http")

    for place in places:
        new_tested_url = html[place:place+70]

        if domain == get_domain_name(new_tested_url):
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
    k = 0
    while k < len(text):
        k = text.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result


# Need to make this function better, many true - negative
def get_domain_name(url):
    try:
        url = url[url.index(".") + 1:]
        last = url.index("/")
    except ValueError:
        return url
    return url[:last]


def secured_index(url, index):
    try:
        return url[:url.index(index)]
    except ValueError:
        return url
