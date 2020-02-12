#!/usr/bin/env python3
"""Test reading data files."""

# pylint:disable=import-error
# imported modules exist

import pymysql

# import constants as CN

from read_load_xml import XmlLoadFile
from read_data_files import ReadDataFiles
from write_stat_sql import WriteStatSql

# Read in the XML load file
XML_FILE = '/Users/venita.hagerty/metviewer/testloadv10fewp3.xml'

XML_LOADFILE = XmlLoadFile(XML_FILE)
XML_LOADFILE.read_xml()

# Read all of the data from the data files into a dataframe
FILE_DATA = ReadDataFiles()

# read in the data files, with options specified by XML flags
FILE_DATA.read_data(XML_LOADFILE.flags,
                    XML_LOADFILE.load_files,
                    XML_LOADFILE.line_types)

# Connect to the database
CONN = pymysql.connect(host=XML_LOADFILE.connection['db_host'],
                       port=XML_LOADFILE.connection['db_port'],
                       user=XML_LOADFILE.connection['db_user'],
                       passwd=XML_LOADFILE.connection['db_password'],
                       db=XML_LOADFILE.connection['db_name'],
                       local_infile=True)

cur = CONN.cursor()

# clear the data if it exists
cur.execute("delete from data_file;")
cur.execute("delete from line_data_cnt;")
cur.execute("delete from line_data_ctc;")
cur.execute("delete from line_data_cts;")
cur.execute("delete from line_data_cts;")
cur.execute("delete from line_data_eclv;")
cur.execute("delete from line_data_eclv_pnt;")
cur.execute("delete from line_data_ecnt;")
cur.execute("delete from line_data_enscnt;")
cur.execute("delete from line_data_fho;")
cur.execute("delete from line_data_grad;")
cur.execute("delete from line_data_isc;")
cur.execute("delete from line_data_mctc;")
cur.execute("delete from line_data_mctc_cnt;")
cur.execute("delete from line_data_mcts;")
cur.execute("delete from line_data_mpr;")
cur.execute("delete from line_data_nbrcnt;")
cur.execute("delete from line_data_nbrctc;")
cur.execute("delete from line_data_nbrcts;")
cur.execute("delete from line_data_orank;")
cur.execute("delete from line_data_orank_ens;")
cur.execute("delete from line_data_pct;")
cur.execute("delete from line_data_pct_thresh;")
cur.execute("delete from line_data_perc;")
cur.execute("delete from line_data_phist;")
cur.execute("delete from line_data_phist_bin;")
cur.execute("delete from line_data_pjc;")
cur.execute("delete from line_data_pjc_thresh;")
cur.execute("delete from line_data_prc;")
cur.execute("delete from line_data_prc_thresh;")
cur.execute("delete from line_data_pstd;")
cur.execute("delete from line_data_pstd_thresh;")
cur.execute("delete from line_data_relp;")
cur.execute("delete from line_data_relp_ens;")
cur.execute("delete from line_data_rhist;")
cur.execute("delete from line_data_rhist_rank;")
cur.execute("delete from line_data_sl1l2;")
cur.execute("delete from line_data_sal1l2;")
cur.execute("delete from line_data_ssvar;")
cur.execute("delete from line_data_vl1l2;")
cur.execute("delete from line_data_val1l2;")
cur.execute("delete from line_data_vcnt;")
cur.execute("delete from stat_header;")
cur.execute("delete from instance_info;")
cur.execute("delete from metadata;")

STAT_LINES = WriteStatSql(XML_LOADFILE.connection)

STAT_LINES.write_sql_data(XML_LOADFILE.flags,
                          FILE_DATA.data_files,
                          FILE_DATA.stat_data,
                          XML_LOADFILE.group,
                          XML_LOADFILE.description,
                          XML_LOADFILE.load_note,
                          XML_LOADFILE.xml_str)

def test_counts():
    """Count lines in database tables."""

    # Count the number of instance_info records created
    cur.execute("SELECT COUNT(*) from instance_info;")
    result = cur.fetchone()
    assert result[0] == 1

    # Count the number of metadata records created
    cur.execute("SELECT COUNT(*) from metadata;")
    result = cur.fetchone()
    assert result[0] == 1

    # Count the number of data_file records created
    cur.execute("SELECT COUNT(*) from data_file;")
    result = cur.fetchone()
    assert result[0] == 7

    # Count the number of stat_header records created
    cur.execute("SELECT COUNT(*) from stat_header;")
    result = cur.fetchone()
    assert result[0] == 368

    # Count the number of line_data_fho records created
    cur.execute("SELECT COUNT(*) from line_data_fho;")
    result = cur.fetchone()
    assert result[0] == 163

    # Count the number of line_data_ctc records created
    cur.execute("SELECT COUNT(*) from line_data_ctc;")
    result = cur.fetchone()
    assert result[0] == 163

    # Count the number of line_data_cnt records created
    cur.execute("SELECT COUNT(*) from line_data_cnt;")
    result = cur.fetchone()
    assert result[0] == 162

    # Count the number of line_data_sl1l2 records created
    cur.execute("SELECT COUNT(*) from line_data_sl1l2;")
    result = cur.fetchone()
    assert result[0] == 10945

    # Count the number of line_data_cts records created
    cur.execute("SELECT COUNT(*) from line_data_cts;")
    result = cur.fetchone()
    assert result[0] == 326

    # Count the number of line_data_ecnt records created
    cur.execute("SELECT COUNT(*) from line_data_ecnt;")
    result = cur.fetchone()
    assert result[0] == 27

    # Count the number of line_data_grad records created
    cur.execute("SELECT COUNT(*) from line_data_grad;")
    result = cur.fetchone()
    assert result[0] == 3

    cur.close()
    CONN.close()