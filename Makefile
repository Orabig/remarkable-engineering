TEMPLATE_BASES = LS_Engineering_Imperial P_Engineering_Imperial P_Engineering_Metric_2mm P_Engineering_Metric_5mm

TEMPLATE_PATHS = $(addprefix output/,$(TEMPLATE_BASES))
TEMPLATE_SVGS = $(TEMPLATE_PATHS:=.svg)
TEMPLATE_PNGS = $(TEMPLATE_PATHS:=.png)

PNG_EXPORT = inkscape --export-area-page --export-width=1404 --export-height=1872
SVG_EXPORT = inkscape

.PHONY: all clean

all: $(TEMPLATE_SVGS) $(TEMPLATE_PNGS)

clean:
	rm -rf output

output/P_Engineering_Imperial.png: imperial-portrait.svg
	$(PNG_EXPORT) --export-png="$@" $<

output/P_Engineering_Imperial.svg: imperial-portrait.svg
	$(SVG_EXPORT) --export-plain-svg="$@" $<

output/LS_Engineering_Imperial.png: imperial-landscape.svg
	$(PNG_EXPORT) --export-png="$@" $<

output/LS_Engineering_Imperial.svg: imperial-landscape.svg
	$(SVG_EXPORT) --export-plain-svg="$@" $<

output/P_Engineering_Metric_2mm.png: metric-2mm-portrait.svg
	$(PNG_EXPORT) --export-png="$@" $<

output/P_Engineering_Metric_2mm.svg: metric-2mm-portrait.svg
	$(SVG_EXPORT) --export-plain-svg="$@" $<

output/P_Engineering_Metric_5mm.png: metric-5mm-portrait.svg
	$(PNG_EXPORT) --export-png="$@" $<

output/P_Engineering_Metric_5mm.svg: metric-5mm-portrait.svg
	$(SVG_EXPORT) --export-plain-svg="$@" $<

