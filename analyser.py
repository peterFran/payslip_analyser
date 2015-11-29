#!/usr/bin/env python3
import asyncio
import os
import re
import subprocess
from optparse import OptionParser


def run_analyser(options,args):
    if len(args) == 1:
        if not os.path.isabs(args[0]):
            print("Must use absolute paths")
        else:
            contents = get_payslips(args[0], 'pdf')
            print(contents)
            asynchronously_convert_pdfs(contents, './images')

    else:
        print(parser.print_help())


#######
def get_payslips(directory, suffix, keep_dir=False):
    """

    :rtype: List[str]
    """
    print("Directory to be scanned is: {}".format(directory))

    if keep_dir:
        contents = ["{}/{}".format(directory, x) for x in os.listdir(directory) if
                    re.search(suffix, x) and not re.search("P60", x)]
    else:
        contents = [x for x in os.listdir(directory) if re.search(suffix, x) and not re.search("P60", x)]
    return contents


#######

####### Process PDFS
async def process_pdfs(pdf_list, destination_directory: str):
    res, _ = await asyncio.wait([process_pdf(pdf, destination_directory) for pdf in pdf_list])
    sorted_result = sorted(task.result() for task in res)
    while len(sorted_result) != len(get_payslips(destination_directory, 'jpg')):
        await asyncio.sleep(1)
    return sorted_result


#######

####### Process PDF
async def process_pdf(pdf: str, destination_directory: str):
    # Converting first page into JPG
    jpg = destination_directory + "/" + pdf.split('/')[-1][:-3] + 'jpg'
    await asyncio.create_subprocess_shell("convert -quality 100% {} {}".format(pdf + "[0]", jpg))
    # print("Converted", "{0} converted".format(pdf))
    return jpg


######

###### Convert PDFs

def asynchronously_convert_pdfs(pdf_list, destination_directory):
    loop = asyncio.get_event_loop()
    return_val = loop.run_until_complete(process_pdfs(pdf_list, destination_directory))
    return return_val


######

####### Process PDFS
async def tesseract_images(image_list):
    res, _ = await asyncio.wait([tesseract_image(image) for image in image_list])
    dict_result = {task.result() for task in res}
    print(dict_result)
    return dict_result


#######

####### Process PDF
async def tesseract_image(image: str):
    # Converting first page into JPG
    text = await asyncio.create_subprocess_shell("tesseract {} stdout".format(image), stdout=subprocess.PIPE)
    print(text)
    return {image: text}


######

###### Get strings from images
def asynchronously_tesseract_images(image_list):
    loop = asyncio.get_event_loop()
    return_val = loop.run_until_complete(tesseract_images(image_list))
    loop.close()
    return return_val


######






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
