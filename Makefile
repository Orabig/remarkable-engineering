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

output/%.png: %.svg
	$(PNG_EXPORT) --export-png="$@" $<

output/%.svg: %.svg
	$(SVG_EXPORT) --export-plain-svg="$@" $<
