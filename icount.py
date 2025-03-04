'''
Query data from /proc/interrupts.

This module provides a function, snapshot(), that returns a table of the current
values in /proc/interrupts.  The table is a list of dictionaries, one for each
row in /proc/interrupts.  The keys in the dictionary are the column headers from
/proc/interrupts, and the values are the corresponding values from the row.
'''

# Copyright 2025 The Board of Trustees of the University of Illinois
# Portions of the code were inspired by or adapted from AI output,
# specifically Github Copilot.


from pprint import pprint
import re
from typing import Dict, Generator

def snapshot(filter: str = '.'):
    '''
    Return a table of the current values in /proc/interrupts.

    Parameters
    ----------
    filter : str, optional
        If provided, only return rows where the 'Device' column matches this
        regular expression.

    A typical first few lines of /proc/interrupts looks like this:
            CPU0       CPU1       CPU2       CPU3       CPU4       CPU5       CPU6       CPU7       
   1:     126723          0          0          0          0          0          0      10932  IR-IO-APIC    1-edge      i8042
   8:          0          0          0          0          0          0          0          0  IR-IO-APIC    8-edge      rtc0

    '''
    with open('/proc/interrupts') as f:
        lines = f.readlines()

    # Parse the header line to determine the number of CPUs.
    headers = lines[0].split()
    n_cpu = len(headers)

    # Update headers to include the unnamed columns
    headers = ['IRQ', 'PerCPU', 'Total', 'Type', 'Edge', 'Device']
    cpus_slice = slice(1, n_cpu + 1)

    # Parse the remaining lines
    for line in lines[1:]:
            if re.search(filter, line):
                fields = line.split()
                cpus = [int(x) for x in fields[cpus_slice]]
                total = sum(cpus)
                if re.match(r'[0-9]', fields[0]):
                    type_ = fields[n_cpu+1]
                    edge = fields[n_cpu+2]
                    device = ' '.join(fields[n_cpu+3:])
                else:
                    type_ = ''
                    edge = ''
                    device = ' '.join(fields[n_cpu+1:])
                yield dict(zip(headers, [fields[0], cpus, total, type_, edge, device]))
                
if __name__ == '__main__':
    # For example, to print the current interrupt count for my wifi card
    # Substitute your own network driver name here
    wifi_list = list(snapshot("iwlwifi"))
    wifi = wifi_list[0]
    wifi_total = wifi['Total']
    print(f"Total interrupts for iwlwifi: {wifi_total}")

    # Or, to print out a few devices
    # pprint(list(snapshot("iwlwifi|rtc0|NMI")))

    # Or, to print out the entire table
    # pprint(list(snapshot()))
