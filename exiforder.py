#!/usr/bin/env python3
#
# Tweak JPEG exif data so that files sort by time taken the same as by filename.
#
# Usage:
#   exiforder.py DSC_*.jpg
#
# The JPEG exif field for "time taken" only has seconds granularity. If you
# take multiple photos in a burst, they might all end up with the same time
# taken, with the subsecond detail off in some other exif field. Google photos
# doesn't look in this other field, so it ends up often misordering photos
# in a burst. If you run this script on your JPGs before putting them in a
# Google Photos album, they'll probably stay in the correct order.
#
# I've only ever tested this with jpegs that came out of lightroom, and which
# were shot with my D500. If this script works for you too, great. LMK.
#
# Wesley Darlington <wesley.darlington@gmail.com>, June 2022.


import datetime
import exif
import glob
import os
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: exiftime pattern ...')
filenames = []
for pattern in sys.argv[1:]:
    filenames.extend(sorted(glob.glob(pattern)))
print("Found %d files" % len(filenames))

images = {}
new_datetime_originals = {}
largest_delta = datetime.timedelta()
prev_datetime_original = None
for filename in filenames:
    with open(filename, 'rb') as f:
        images[filename] = exif.Image(f)
    datetime_original = datetime.datetime.strptime(images[filename].datetime_original, exif.DATETIME_STR_FORMAT)
    if not prev_datetime_original or datetime_original > prev_datetime_original:
        prev_datetime_original = datetime_original
        continue
    ex_datetime_original = datetime_original
    datetime_original = prev_datetime_original + datetime.timedelta(seconds=1)
    delta = datetime_original - ex_datetime_original
    new_datetime_originals[filename] = datetime_original
    print("%s: %s -> %s (%s)" % (filename, ex_datetime_original, datetime_original, delta))
    if delta > largest_delta:
        largest_delta = delta
    prev_datetime_original = datetime_original
print("Largest delta is %s" % largest_delta)

if len(new_datetime_originals) == 0:
    sys.exit("Nothing to do. Exiting.")

if input("Make these %d changes? (y/n) " % len(new_datetime_originals)) != "y":
    sys.exit("Exiting.")

for filename, new_datetime_original in new_datetime_originals.items():
    print("Adjusting %s" % filename, end=" ... ")
    images[filename].datetime_original = new_datetime_original.strftime(exif.DATETIME_STR_FORMAT)
    renamed = filename+".prev"
    print("renamed original to %s" % renamed, end=" ... ")
    os.rename(filename, renamed)
    with open(filename, 'wb') as f:
        f.write(images[filename].get_file())
    print("done")
