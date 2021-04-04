#!/usr/bin/env python3

class MeasurementMismatch(Exception):
    pass

def get_inches(params, key):
    measurement_dict = params[key]
    if 'in' in measurement_dict:
        return measurement_dict['in']
    if 'mm' in measurement_dict:
        return measurement_dict['mm'] / 25.4
    if 'cm' in measurement_dict:
        return measurement_dict['cm'] / 2.54
    raise MeasurementMismatch('No measurements for key "{}"'.format(key))
            

class Parameters:
    """Holds all of the parameters for a single template."""

    def __init__(self, definitions):
        self.definitions = definitions
        if self.landscapep:
            self.template_width_in = get_inches(definitions['screen'], 'height')
            self.template_height_in = get_inches(definitions['screen'], 'width')
            self.template_width_px = definitions['screen']['height']['px']
            self.template_height_px = definitions['screen']['width']['px']
        else:
            self.template_width_in = get_inches(definitions['screen'], 'width')
            self.template_height_in = get_inches(definitions['screen'], 'height')
            self.template_width_px = definitions['screen']['width']['px']
            self.template_height_px = definitions['screen']['height']['px']
        width_dpi = self.template_width_px / self.template_width_in
        height_dpi = self.template_height_px / self.template_height_in
        self.dpi = max(width_dpi, height_dpi)

    def px(self, section, field):
        return get_inches(self.definitions[section], field) * self.dpi

    @property
    def landscapep(self):
        return self.definitions['layout']['orientation'] == 'landscape'
    
    @property
    def bg_color(self):
        return self.definitions['lines']['bg_color']

    @property
    def line_color(self):
        return self.definitions['lines']['line_color']
        
    @property
    def header_outline(self):
        return self.px('lines', 'header_outline')

    @property
    def grid_outline(self):
        return self.px('lines', 'grid_outline')

    @property
    def grid_major_thickness(self):
        return self.px('lines', 'grid_major')

    @property
    def grid_minor_thickness(self):
        return self.px('lines', 'grid_minor')

    @property
    def footer_line(self):
        return self.px('lines', 'footer_line')

    @property
    def header_y(self):
        return self.px('layout', 'header_margin')
    
    @property
    def header_height(self):
        return self.px('layout', 'header_height')
    
    @property
    def header_title_x(self):
        return self.grid_x

    @property
    def header_title_width(self):
        return self.grid_width - self.header_date_width - self.px('layout', 'header_margin')
    
    @property
    def header_date_x(self):
        return self.grid_x + self.grid_width - self.header_date_width

    @property
    def header_date_width(self):
        return self.px('layout', 'header_date_width')

    @property
    def grid_x(self):
        return self.template_width_px / 2 - self.grid_width / 2

    @property
    def grid_y(self):
        return self.header_y + self.header_height + self.px('layout', 'header_margin')

    @property
    def grid_width(self):
        return self.px('layout', 'grid_width')

    @property
    def grid_height(self):
        return self.px('layout', 'grid_height')
    
    @property
    def grid_major_spacing(self):
        return self.px('layout', 'grid_major')

    @property
    def grid_minor_spacing(self):
        return self.px('layout', 'grid_minor')

    @property
    def footer_spacing(self):
        return self.px('layout', 'footer_spacing')

