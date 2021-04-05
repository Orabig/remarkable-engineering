TEMPLATE_BASES = LS_Engineering_Imperial P_Engineering_Imperial P_Engineering_Metric_2mm P_Engineering_Metric_5mm

TEMPLATE_PATHS = $(addprefix output/,$(TEMPLATE_BASES))
TEMPLATE_SVGS = $(TEMPLATE_PATHS:=.svg)
TEMPLATE_PNGS = $(TEMPLATE_PATHS:=.png)
TEMPLATE_THUMBS = $(addprefix thumbs/,$(TEMPLATE_BASES:=-thumb.png))

PROGRAM_FILES = draw-template.py parameters.py draw.py

GIT_VERSION := "$(shell git describe --abbrev=4 --dirty --always --tags)"

PNG_EXPORT = inkscape --export-area-page --export-width=1404 --export-height=1872

.PHONY: all build dist clean distclean thumbs

all: build

build: $(TEMPLATE_SVGS) $(TEMPLATE_PNGS)

clean:
	rm -rf output thumbs

distclean: clean
	rm -f remarkable-engineering-*.zip

thumbs: $(TEMPLATE_THUMBS)

thumbs/P_%-thumb.png: output/P_%.png
	mkdir -p thumbs
	convert $< -colorspace Gray -gamma 0.4 -resize 320x320 $@
	optipng $@

thumbs/LS_%-thumb.png: output/LS_%.png
	mkdir -p thumbs
	convert $< -colorspace Gray -gamma 0.4 -rotate 90 -resize 320x320 $@
	optipng $@

RELEASE = remarkable-engineering-$(GIT_VERSION)
dist: build
	mkdir -p $(RELEASE)
	ln output/* $(RELEASE)
	zip -r $(RELEASE).zip $(RELEASE)
	rm -rf $(RELEASE)

output/%.png: output/%.svg
	$(PNG_EXPORT) --export-png="$@" $<
	optipng $@

output/%.svg: %.toml remarkable.toml lines.toml $(PROGRAM_FILES)
	mkdir -p output
	./draw-template.py -o $@ remarkable.toml lines.toml $<
