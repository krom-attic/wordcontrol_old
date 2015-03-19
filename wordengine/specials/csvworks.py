import codecs
import csv


def get_csv(csvfile):
    """
    It's probably impossible to detect (sniff) dialect and encoding correctly, because MS Excel prepares CSV files
    incorrectly. May be some parsing setting should be introduced.
    """
    return csv.reader(codecs.iterdecode(csvfile, 'utf-8'), dialect=csv.excel_tab, delimiter='\t')
