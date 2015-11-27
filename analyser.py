#!/usr/bin/env python3
from optparse import OptionParser
import asyncio
import os
import re
import pypipdfocr


def run_analyser(options,args):
    if len(args) == 1:
        if not os.path.isabs(args[0]):
            print("Must use absolute paths")
        else:
            contents = get_payslips(args[0])
            print(contents)
            asynchronously_get_deets(contents)

    else:
        print(parser.print_help())



def get_payslips(directory):
    print("Directory to be scanned is: {}".format(directory))
    contents = [x for x in os.listdir(directory) if not re.search("P60", x)]
    return contents

async def process_pdfs(pdf_list):
    await asyncio.wait([process_pdf(index,pdf)for index, pdf in enumerate(pdf_list)])

async def process_pdf(index, pdf):
    await asyncio.sleep(index % 5)
    print(index)
    return pdf

def asynchronously_get_deets(pdf_list):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_pdfs(pdf_list))

def synchronously_get_deets(pdf_list):
    pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--student", action="store_true", dest="student",
                      help="Give Student Loan Summary", default=True)
    parser.add_option("-n", "--ni",
                      action="store_false", dest="ni", default=True,
                      help="Give National Insurance Summary")
    parser.add_option("-p", "--paye",
                      action="store_false", dest="paye", default=True,
                      help="Give PAYE summary")

    (options, args) = parser.parse_args()
    run_analyser(options,args)


#
#
# loop.close()

# async def process_pdfs(pdf_list):
#
#     async def process_pdf(pdf):
#         await return pdf