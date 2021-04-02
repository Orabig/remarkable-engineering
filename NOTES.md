Screen Size
-----------

There are no official specs on the dimensions of the screen, but there are
inferences we can make.

### Official Spec Derivations

The screen is, officially a 1404×1872 pixel display with a 10.3″ diagonal
and 226 DPI.  If we assume that there's some rounding involved, we can
conclude that the diagonal must be between 10.25″ and 10.35″, while the
DPI must be between 225.5 and 226.5.  As the following table shows, that
gives us a width between 6.199″ and 6.210″ and a height between 8.265″ and
8.280″.

|                  | Width (in) | Height (in) |
|------------------|------------|-------------|
| min diag (10.25) |     6.1500 |      8.2000 |
| max DPI (226.5)  |     6.1987 |      8.2649 |
| max diag (10.35) |     6.2100 |      8.2800 |
| min DPI (225.5)  |     6.2262 |      8.3016 |

### Exported Files

Furthermore, when you export images from your reMarkable, they come out as
follows:

#### SVG Export

The exported SVGs do not specify a unit for their dimensions, which mean
they use the SVG default of 1 == 1px == 1/96th of 1in.  This gives some
rather nonsensical size results.

| Measurement             | Value  |
|-------------------------|--------|
| DPI                     |     96 |
| Width (px)              |   1404 |
| Height (px)             |   1872 |
| Width (in, calculated)  | 14.625 |
| Height (in, calculated) | 19.500 |

#### PNG Export

The exported PNGs are 1404×1872, naturally, with a DPI of 227.99.

| Measurement             | Value  |
|-------------------------|--------|
| DPI                     | 227.99 |
| Width (px)              |   1404 |
| Height (px)             |   1872 |
| Width (in, calculated)  | 6.1582 |
| Height (in, calculated) | 8.2109 |

#### PDF Export

The exported PDFs have a media box of 445×594 points, which gives:

| Measurement             | Value  |
|-------------------------|--------|
| PPI                     |     72 |
| Width (pt)              |    445 |
| Height (pt)             |    594 |
| Width (in, calculated)  | 6.1806 |
| Height (in, calculated) | 8.2500 |

### Other Sources of Information

[One reMarkable review][pjm-review] says the screen is 15.6×21
centimeters, which translates into 6.142×8.268 inches and 228.6×226.4 DPI.
That seems pretty far outside the other measurements.

  [pjm-review]: https://pauljmiller.wordpress.com/2017/11/23/a-review-of-the-remarkable-tablet/

### Compiled Results

This gives us:

| Measurement Source     | DPI    | Width (in) | Height (in) |
|------------------------|--------|------------|-------------|
| PNG Export             | 227.99 |     6.1582 |      8.2109 |
| Exactly 10.3″ diagonal | 227.18 |     6.1800 |      8.2400 |
| PDF Export             | †      |     6.1806 |      8.2500 |
| Min for official specs | 226.50 |     6.1987 |      8.2649 |
| Max for official specs | 226.09 |     6.2100 |      8.2800 |

† The PDF export gives 227.16 DPI horizontally and 226.91 DPI vertically

The width and height resulting from the assumtion that the 10.3″ diagonal
is exact are themselves exact.  That seems a nice place to default to, so
that's what these templates use.
