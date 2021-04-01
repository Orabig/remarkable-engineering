reMarkable Engineering Templates
================================

![Imperial grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Imperial-thumb.png)
![Metric 5mm grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Metric_5mm-thumb.png)
![Metric 2mm grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Metric_2mm-thumb.png)
![Imperial grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Engineering_Imperial-thumb.png)

These are a set of templates for the [reMarkable][] E Ink tablets.  They
provide a more structured base than any of the stock grid templates.  In
particular, these have:

  [reMarkable]: https://remarkable.com

 * A header line with a large and small information box.  The author uses
   them for page titles and dates, respectively.
   
 * A grid with major and minor grid lines.  The imperial templates have
   major lines every inch and minor lines every eighth of an inch.  The
   metric templates have major lines every centimeter and minor lines
   every five millimeters or every two millimeters, depending on the
   template.
   
 * A couple of lines at the bottom for more free-form notes.
 
The spacing is calibrated to the size of the reMarkable's screen.  Marks
that are one centimeter apart on the reMarkable may have look different
when exported from the device or reMarkable cloud.


Installation
------------

Go to the project's [releases][] page and use the "Template Images" link
on the most recent release to download a zip file containing all of the
template files.  Extract the zip file's contents.  Note that there is an
SVG file and a PNG file for each template; you need to send *both* of them
to the reMarkable for each template you want to use!

  [releases]: https://gitlab.com/asciiphil/remarkable-engineering/-/releases

It's probably easiest to use the [Remarkable Assistant][RMA] or
[reMarkable Connection Utility][RCU] to add the templates to your tablet.

  [RMA]: https://github.com/richeymichael/remarkable-assistant
  [RCU]: http://www.davisr.me/projects/rcu/

If you want to do it by hand, use an SCP client to copy the files to
`/usr/share/remarkable/templates/` on the reMarkable, then edit
`/usr/share/remarkable/templates/templates.json` and add the following
JSON text to the file.  (Add the text between one `},` line and the
following `{` line.)

```json
    {
        "name": "Engineering Grid, ⅛″",
        "filename": "P_Engineering_Imperial",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, ⅛″",
        "filename": "LS_Engineering_Imperial",
        "iconCode": "\ue9fa",
        "landscape": true,
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, 5mm",
        "filename": "P_Engineering_Metric_5mm",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, 2mm",
        "filename": "LS_Engineering_Metric_2mm",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
```


License
-------

To the extent possible under law, the author(s) have dedicated all
copyright and related and neighboring rights to this software to the
public domain worldwide. This software is distributed without any
warranty.

You should have received a copy of the CC0 Public Domain Dedication along
with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
