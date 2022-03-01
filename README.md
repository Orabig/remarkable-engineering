reMarkable Engineering Templates
================================

![Imperial grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Imperial-thumb.png)
![Metric 5mm grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Metric_5mm-thumb.png)
![Metric 2mm grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Engineering_Metric_2mm-thumb.png)
![Logarithmic grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Log-thumb.png)
![Semilogarithmic grid, portrait](https://static.aperiodic.net/remarkable-engineering/P_Semiog-thumb.png)
![Imperial grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Engineering_Imperial-thumb.png)
![Metric 5mm grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Engineering_Metric_5mm-thumb.png)
![Metric 2mm grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Engineering_Metric_2mm-thumb.png)
![Logarithmic grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Log-thumb.png)
![Semilogarithmic grid, landscape](https://static.aperiodic.net/remarkable-engineering/LS_Semiog-thumb.png)

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
that are one centimeter apart on the reMarkable may look different when
exported from the device or reMarkable cloud.  Experimentation (with
software version 2.6) indicates that the PDF export option should match
the size pretty closely.  The PNG export will match the size for any
program that understands the PNG's embedded DPI.  The SVG export will not
match the dimensions of the tablet's image.


Installation
------------

Go to the project's [releases][] page and use the "Template Images" link
on the most recent release to download a zip file containing all of the
template files.  Extract the zip file's contents.  Note that there is an
SVG file and a PNG file for each template; you need to send *both* of them
to the reMarkable for each template you want to use!

  [releases]: https://gitlab.com/asciiphil/remarkable-engineering/-/releases

It's probably easiest to use the [reMarkable Connection Utility][RCU] or
[Remarkable Assistant][RMA] to add the templates to your tablet.

  [RMA]: https://github.com/richeymichael/remarkable-assistant
  [RCU]: http://www.davisr.me/projects/rcu/

If you want to do it more manually, use an SCP client to copy the files to
`/usr/share/remarkable/templates/` on the reMarkable, then add entries for
them to `/usr/share/remarkable/templates/templates.json`.

If you have [templatectl][] installed, you can use one or more of the
following commands:

  [templatectl]: https://github.com/PeterGrace/templatectl

    templatectl add --name 'Engineering Grid 1/8" P' --filename 'P_Engineering_Imperial' --category Grids --icon_code e99e
    templatectl add --name 'Engineering Grid 1/8" LS' --filename 'LS_Engineering_Imperial' --category Grids --icon_code e9fa --landscape
    templatectl add --name 'Engineering Grid Log-Log P' --filename 'P_Log --category Grids --icon_code e99e
    templatectl add --name 'Engineering Grid Log-Log LS' --filename 'LS_Log --category Grids --icon_code e9fa
    templatectl add --name 'Engineering Grid Semilog P' --filename 'P_Semilog --category Grids --icon_code e99e
    templatectl add --name 'Engineering Grid Semilog LS' --filename 'LS_Semilog --category Grids --icon_code e9fa
    templatectl add --name 'Engineering Grid 2mm P' --filename 'P_Engineering_Metric_2mm' --category Grids --icon_code e99e
    templatectl add --name 'Engineering Grid 2mm LS' --filename 'LS_Engineering_Metric_2mm' --category Grids --icon_code e9fa --landscape
    templatectl add --name 'Engineering Grid 5mm P' --filename 'P_Engineering_Metric_5mm' --category Grids --icon_code e99e
    templatectl add --name 'Engineering Grid 5mm LS' --filename 'LS_Engineering_Metric_5mm' --category Grids --icon_code e9fa --landscape

Otherwise, you'll have to edit
`/usr/share/remarkable/templates/templates.json` by hand and add the
following JSON text.  (Add the text between one `},` line and the
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
        "name": "Engineering Grid, Log-Log",
        "filename": "P_Log",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, Log-Log",
        "filename": "LS_Log",
        "iconCode": "\ue9fa",
        "landscape": true,
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, Semilog",
        "filename": "P_Semilog",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, Semilog",
        "filename": "LS_Semilog",
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
        "name": "Engineering Grid, 5mm",
        "filename": "LS_Engineering_Metric_5mm",
        "iconCode": "\ue9fa",
        "landscape": true,
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, 2mm",
        "filename": "P_Engineering_Metric_2mm",
        "iconCode": "\ue99e",
        "categories": [
            "Grids"
        ]
    },
    {
        "name": "Engineering Grid, 2mm",
        "filename": "LS_Engineering_Metric_2mm",
        "iconCode": "\ue9fa",
        "landscape": true,
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
