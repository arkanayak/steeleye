import json
import csv
import boto3
import urllib3
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from datetime import datetime

http = urllib3.PoolManager()


def download_xml():
    """ Downloads the xml file from the given link and returns first download URL """

    url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2020-01-08T00:00:00Z+TO+2020-01-08T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"
    resp = http.request('GET', url)
    with open('/tmp/feed.xml', 'wb') as f:
        f.write(resp.data)

    xmlfile = '/tmp/feed.xml'
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    download_link = ""
    found = False
    for item in root.findall('./result/doc'):

        for child in item:
            if 'http' in str(child.text):
                download_link = str(child.text)
            if str(child.text) == 'DLTINS':
                found = True
                break
        if found:
            break

    return download_link


def extract_zip(url):
    """ Extract the zip downloaded via first download URL"""
    r = http.request('GET', url)
    zip_file_path = "/tmp/{}".format(url.split('/')[-1])
    open(zip_file_path, 'wb').write(r.data)
    with ZipFile(zip_file_path, 'r') as zip:
        zip.printdir()
        print('Extracting all the files now...')
        zip.extractall('/tmp')
        print('Done!')


def create_csv_upload_s3():
    """ Creates the CSV with headers and uploads it to s3 bucket 'arkas3b' """

    now = datetime.now()
    current_time = now.strftime("%m_%d_%Y_%H_%M_%S")

    csv_file_name = "/tmp/{}.csv".format(str(current_time))

    rows = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp",
            "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy", "Issr"]
    f = open(csv_file_name, 'w+')

    with f:
        fnames = rows
        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writeheader()

    s3 = boto3.resource('s3')
    s3.Object('arkas3b', csv_file_name.split('/')[-1]).upload_file(Filename=csv_file_name)


def convert_xml_to_dict():
    """ This function converts the xml to dict for writing to csv.
    P.S. -  Was not able to come up with a solution for this """
    pass


def lambda_handler(event, context):
    download_link = download_xml()

    extract_zip(download_link)

    convert_xml_to_dict()

    create_csv_upload_s3()

    return {
        'statusCode': 200,
        'body': json.dumps('Process Completed')
    }
