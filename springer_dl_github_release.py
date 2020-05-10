#!/usr/bin/python3

# Author: Aleksander Vainer, April 2020

# This short python script downloads the free content from the Springer website.
# It is based on the following observation:
# the (example) url of the download page is
# https://link.springer.com/book/10.1007/978-981-13-8759-3
# it leads to download button with the following path
# https://link.springer.com/content/pdf/10.1007/978-981-13-8759-3.pdf
# and
# https://link.springer.com/download/epub/10.1007/978-981-13-8759-3.epub
# (epub does not exist for every book)

# To use this script put it and the csv-file with book_list_csv_filename in any folder and run it.

import csv
import os
import wget


book_list_csv_filename = 'SearchResults_Springer.csv'
report_filename = 'report.csv'

dir_name = os.path.dirname(__file__)
download_dir = os.path.join(dir_name, 'downloads')
if not os.path.exists(download_dir):
    os.mkdir(download_dir)


def page_url_to_pdf_url(input_url):
    output_url = input_url.replace('book', 'content/pdf') + '.pdf'
    return output_url


def page_url_to_epub_url(input_url):
    output_url = input_url.replace('book', 'download/epub') + '.epub'
    return output_url


def bool_to_word(bool_value):
    return 'SUCCESS' if bool_value else 'FAILURE'


with open(book_list_csv_filename, 'r') as file_handler:
    reader = csv.DictReader(file_handler)
    page_urls = []
    filenames = []
    for row in reader:
        page_urls.append(row['URL'])
        filename = row['Item Title'] + ' DOI' + row['Item DOI']
        filename = filename.replace('/', '--')
        filename = filename.replace(',', '')
        filenames.append(filename)
    pdf_urls = [page_url_to_pdf_url(path) for path in page_urls]
    epub_urls = [page_url_to_epub_url(path) for path in page_urls]

report_list_of_dicts = []

for page_url, pdf_url, epub_url, filename in zip(page_urls, pdf_urls, epub_urls, filenames):
    try:
        print(os.path.join(download_dir, filename + '.pdf'))
        wget.download(pdf_url, os.path.join(download_dir, filename + '.pdf'))
        dead_pdf_link_found = False
    except:
        dead_pdf_link_found = True
    try:
        wget.download(epub_url, os.path.join(download_dir, filename + '.epub'))
        dead_epub_link_found = False
    except:
        dead_epub_link_found = True
    report_list_of_dicts.append({'page_url': page_url, 'pdf_url': pdf_url, 'epub_url': epub_url,
                                 'pdf_exists': bool_to_word((not dead_pdf_link_found)),
                                 'epub_exists': bool_to_word((not dead_epub_link_found))})

keys = report_list_of_dicts[0].keys()
with open(report_filename, 'w') as file_handler:
    writer = csv.DictWriter(file_handler, keys)
    writer.writeheader()
    writer.writerows(report_list_of_dicts)
