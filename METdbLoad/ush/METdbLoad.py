#!/usr/bin/env python3

"""
Program Name: METdbLoad.py
Contact(s): Venita Hagerty
Abstract:
History Log:  Initial version
Usage: Load files into METdb
Parameters: -index
Input Files: load_spec XML file
Output Files: N/A
Copyright 2019 UCAR/NCAR/RAL, CSU/CIRES, Regents of the University of Colorado, NOAA/OAR/ESRL/GSD
"""

# pylint:disable=import-error
# imported modules exist

import argparse
import sys

from read_load_xml import XmlLoadFile
from read_data_files import ReadDataFiles


def main():
    """! Class to read in load_spec xml file
        Returns:
           N/A
    """

    print("--- Start METdbLoad ---")

    parser = argparse.ArgumentParser()
    parser.add_argument("xmlfile", help="please provide required xml load_spec filename")
    parser.add_argument("-index", action="store_true", help="only process index, do not load data")

    # get the command line arguments
    args = parser.parse_args()

    print(sys.path)

    # if -index is used, only process the index
    if args.index:
        print("index is true - only process index")

    try:
        print("XML filename is ", args.xmlfile)

        # instantiate a load_spec XML file
        xml_loadfile = XmlLoadFile(args.xmlfile)

        # read in the XML file and get the information out of its tags
        xml_loadfile.read_xml()

    except (RuntimeError, TypeError, NameError, KeyError):
        print("***", sys.exc_info()[0], "occurred in Main ***")

    try:
        file_data = ReadDataFiles()

        file_data.read_data(xml_loadfile.load_files,
                            xml_loadfile.flags,
                            xml_loadfile.line_types)

    except (RuntimeError, TypeError, NameError, KeyError):
        print("***", sys.exc_info()[0], "occurred in Main ***")

    print("--- End METdbLoad ---")


if __name__ == '__main__':
    main()
