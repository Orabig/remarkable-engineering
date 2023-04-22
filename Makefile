TEMPLATE_BASES = \
	LS_Engineering_Imperial P_Engineering_Imperial \
	LS_Engineering_Metric_2mm P_Engineering_Metric_2mm \
	LS_Engineering_Metric_5mm P_Engineering_Metric_5mm \
	P_Engineering_Log LS_Engineering_Log \
	P_Engineering_Durationlog LS_Engineering_Durationlog \
	P_Engineering_Semilog LS_Engineering_Semilog

TEMPLATE_SOURCES = $(addprefix src/,$(TEMPLATE_BASES))
TEMPLATE_PATHS = $(addprefix output/,$(TEMPLATE_BASES))
TEMPLATE_SVGS = $(TEMPLATE_PATHS:=.svg)
TEMPLATE_PNGS = $(TEMPLATE_PATHS:=.png)
TEMPLATE_THUMBS = $(addprefix thumbs/,$(TEMPLATE_BASES:=-thumb.png))

PROGRAM_FILES = draw-template.py parameters.py draw.py

GIT_VERSION := "$(shell git describe --abbrev=4 --dirty --always --tags)"

PNG_EXPORT = inkscape --export-type=png --export-area-page --export-width=1404 --export-height=1872 --export-dpi=227

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

# Inkscape will generate RGBA PNGs.  By default, optipng will reduce those
# to paletted 8-bit PNGs.  But the reMarkable can't handle paletted PNGs,
# so we have to use `-nc` to prevent color map alterations.
#
# TODO: See if reMarkable likes greyscale, non-transparent PNGs.  Might
# have to use Imagemagick to convert; doesn't look like Inkscape will
# output anything but RGBA PNGs.
output/%.png: output/%.svg
	$(PNG_EXPORT) --export-filename="$@" $<
	optipng -nc $@

output/%.svg: src/%.toml src/remarkable.toml src/lines.toml $(PROGRAM_FILES)
	mkdir -p output
	./draw-template.py -o $@ src/remarkable.toml src/lines.toml $<
