#!/bin/bash/python

"""
Get PVC collection location from INEC
"""

import requests

url = "http://pvc.inecnigeria.org/index.php/pu/ajaxsearchpu"


def spliter(text, delimiter):
    return text.split(delimiter)


def hasDelimiter(text, delimiter):
    return text.find(delimiter) >= 0


def formatPvcNumber(pvc_number):
    pvc_len = len(pvc_number)

    if pvc_len < 9: return False
    if pvc_len == 9: return pvc_number
    if pvc_len > 9:
        dash = '-'
        slash = '/'
        pipe = '|'

        hasDash = hasDelimiter(pvc_number, dash)
        hasSlash = hasDelimiter(pvc_number, slash)
        hasPipe = hasDelimiter(pvc_number,  pipe)

        split = ""

        if hasDash: split = spliter(pvc_number, dash)
        elif hasSlash: split = spliter(pvc_number, slash)
        elif hasPipe: split = spliter(pvc_number, pipe)

        split_len = len(split)
       
        if split_len != 4: return False

        return ''.join(split)


def requestPayload(pvc_number):
    state_id = pvc_number[:2]
    lga_id = pvc_number[2:4]
    ra_id = pvc_number[4:6]
    pu_id = pvc_number[6:]

    return {
            "state_id": state_id,
            "lga_id": lga_id,
            "ra_id": ra_id,
            "pu_id": pu_id
            }


def getPvcLocation(data):
    return requests.post(url, data=data).text


def formatPvcResponse(response):
    split = response.split('>')
    locIndex = 3
    return split[locIndex].split('</div')[0]


def pvc_main(testData):
    pvc_number = formatPvcNumber(testData)

    if not pvc_number: return "Invalid PVC number"

    data = requestPayload(pvc_number)
    pvc_location = getPvcLocation(data)

    return formatPvcResponse(pvc_location)


if __name__ == "__main__":
    pvc_number = ""
    #pvc_main(pvc_number)
