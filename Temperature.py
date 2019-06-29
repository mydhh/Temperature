#!/usr/bin/env python

# DESCRIPTION
# Software to parse temperature datasets from KNMI and plot charts using
# the Matplotlib library

# DATASETS
# https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_270_tg.txt
# https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_290_tg.txt
# https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/maandgegevens/mndgeg_370_tg.txt

from datetime import datetime

import os
import sys
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def readfile(fn, x, y, STN):

    Exists = os.path.isfile(fn)

    if Exists:
        logging.info("Reading file " + fn)

        with open(fn) as f:
            content = f.readlines()

        for input in content:
            if input.startswith( STN ):                             # Skip the header and look at lines starting with Station Number (STN)
                input_date = input[4:8]                             # Get the year (YYYY)
                dt = datetime.strptime(input_date, '%Y')            # Parse string into datetime

                input_temp = input[94:]                             # Get the temperature
                cleanedline = input_temp.strip()                    # Strip leading and trailing whitespaces
                if (cleanedline != ""):
                    temp = float(cleanedline)                       # Parse string into float
                    temp = temp / 10				                # Calculate yearly average
                    logging.debug(str(dt.year) + " " + str(temp))   # Print data points to cross-reference with online file
                    x.append(dt)                                    # Append year to x
                    y.append(temp)					                # Append temperature to y
                else:
                    logging.warning("Ignoring empty line for year " + str(dt.year))
    else:
        logging.error("File " + fn + " not found")

def main():

    Debug = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            print("Setting loglevel to debug")
            Debug = True

    if (Debug):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("Start")

    # Arrays to store measurements
    x1 = []; x2 = []; x3 = [];
    y1 = []; y2 = []; y3 = [];

    infile = "data/mndgeg_270_tg.txt"
    readfile(infile, x1, y1, "270")

    infile = "data/mndgeg_290_tg.txt"
    readfile(infile, x2, y2, "290")

    infile = "data/mndgeg_370_tg.txt"
    readfile(infile, x3, y3, "370")

    # Create a graph
    fig, ax = plt.subplots()
    ax.plot(x1, y1)
    ax.plot(x2, y2)
    ax.plot(x3, y3)

    # Format the ticks
    years = mdates.YearLocator(5)
    yearsFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)

    # Format the labels
    plt.xlabel('Tijd')
    plt.ylabel('Temperatuur')
    plt.title('Gemiddelde jaartemperatuur in Nederland (Bron: KNMI)')

    # Make y-axis start at 0
    plt.ylim(bottom=0)
    ax.grid(True)

    # Rotates and aligns the x labels
    fig.autofmt_xdate()

    # Add the legend
    plt.legend(['Leeuwarden', 'Twente', 'Eindhoven'], loc='lower right')

    plt.show()

    print("Done")

##############################################################################

if __name__ == "__main__":
    main()
