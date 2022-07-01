# exiforder
Tool to tweak exif files for sorting by filename in google photos

Usage:
```
  exiforder.py DSC_*.jpg
```

The JPEG exif field for the time a photo was taken only has seconds granularity.
If you take multiple photos in a burst, they might all end up with the same
time taken, with the subsecond detail in some other exif field.
Google Photos doesn't look in this other field, so it ends up often misordering
photos from a burst.

I wish Google Photos could sort photos by filename, but this is the best I've
come up with: adjust the thing it *can* sort by so that it's the same as the
filename order. Run this script on your JPEGs before uploading to Google Photos,
and they might end up ordered as if by filename.

I've only ever tested this with jpegs that came out of lightroom, and which
were shot with my D500. If this script works for you too, great. Chances are
it won't though, but maybe you can make it work?

Wesley Darlington <wesley.darlington@gmail.com>, June 2022.
