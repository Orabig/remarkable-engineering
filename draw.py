#!/usr/bin/env python3

import math

import numpy as np
import svgwrite

def draw_svg(filename, parameters):
    if parameters.landscapep:
        size = (parameters.template_height_in * svgwrite.inch,
                parameters.template_width_in * svgwrite.inch)
        viewBox = '0 0 {} {}'.format(
            parameters.template_height_px,
            parameters.template_width_px)
    else:
        size = (parameters.template_width_in * svgwrite.inch,
                parameters.template_height_in * svgwrite.inch)
        viewBox='0 0 {} {}'.format(
            parameters.template_width_px,
            parameters.template_height_px)
    drawing = svgwrite.Drawing(filename,
                               profile='tiny',
                               size=size,
                               viewBox=viewBox)

    main_group = drawing.g()
    if parameters.landscapep:
        main_group.translate(tx=0, ty=parameters.template_width_px)
        main_group.rotate(-90)
    drawing.add(main_group)
    
    draw_background(drawing, main_group, parameters)
    draw_header(drawing, main_group, parameters)
    draw_grid(drawing, main_group, parameters)
    draw_footer(drawing, main_group, parameters)
    
    drawing.save()

def px_align(coordinate, line_thickness):
    """Returns a value as close to the given coordinate as possible that
    centers a line of the given thickness on the pixel grid.
    """
    is_even = math.floor(line_thickness) % 2 == 0
    if is_even:
        return round(coordinate)
    else:
        return round(coordinate + 0.5) - 0.5
    
def draw_background(drawing, main_group, parameters):
    main_group.add(
        drawing.rect(insert=(0, 0),
                     size=(parameters.template_width_px,
                           parameters.template_height_px),
                     fill=parameters.bg_color))

def draw_header(drawing, main_group, parameters):
    header_group = drawing.g(fill='none',
                             stroke=parameters.line_color,
                             stroke_width=parameters.header_outline)

    header_top = px_align(parameters.header_y, parameters.header_outline)
    header_bottom = px_align(parameters.header_y + parameters.header_height, parameters.header_outline)
    header_height = header_bottom - header_top
    title_left = px_align(parameters.header_title_x, parameters.header_outline)
    title_right = px_align(parameters.header_title_x + parameters.header_title_width, parameters.header_outline)
    title_width = title_right - title_left
    date_left = px_align(parameters.header_date_x, parameters.header_outline)
    date_right = px_align(parameters.header_date_x + parameters.header_date_width, parameters.header_outline)
    date_width = date_right - date_left
    
    main_group.add(header_group)
    header_group.add(
        drawing.rect(
            insert=(title_left, header_top),
            size=(title_width, header_height)))
    header_group.add(
        drawing.rect(
            insert=(date_left, header_top),
            size=(date_width, header_height)))
    
def draw_grid(drawing, main_group, parameters):
    grid_group = drawing.g(stroke=parameters.line_color)
    main_group.add(grid_group)

    grid_left = px_align(parameters.grid_x, parameters.grid_outline)
    grid_right = px_align(parameters.grid_x + parameters.grid_width, parameters.grid_outline)
    grid_top = px_align(parameters.grid_y, parameters.grid_outline)
    grid_bottom = px_align(parameters.grid_y + parameters.grid_height, parameters.grid_outline)
    
    grid_group.add(
        drawing.rect(
            fill='none',
            insert=(grid_left, grid_top),
            size=(grid_right - grid_left, grid_bottom - grid_top),
            stroke_width=parameters.grid_outline))
    major_group = drawing.g(stroke_width=parameters.grid_major_thickness)
    minor_group = drawing.g(stroke_width=parameters.grid_minor_thickness)
    grid_group.add(major_group)
    grid_group.add(minor_group)

    draw_horizontal_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters)
    draw_vertical_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters)

# Merge identical minor scales into a major one
def merge_scales(majors, minors):
    return list(map(lambda major: list(map(lambda minor: major + minor, minors)), majors))

# Fills 'width' pixels with a major/minor scale.
# Returns an array of x/y coordinates arrays, each starting with a major point.
# [ [ major_0(==0), minor_0_0, minor_0_1, ...], [major_1, minor_1_0, ...], ... ]
def compute_scale(width, grid_scale, major_spacing, minor_spacing):
    major_count = 1 + round(width / major_spacing)
    real_spacing = width / major_count
    major_lines = np.linspace(0, width, major_count, endpoint=False)
    if grid_scale == 'log':
        minor_lines = real_spacing - (np.log(np.linspace(1, 10, 1 + round(real_spacing / minor_spacing), endpoint=False)) / np.log(10) * real_spacing)
    else:
        minor_lines = np.linspace(0, real_spacing, 1 + round(real_spacing / minor_spacing), endpoint=False)
    return merge_scales(major_lines, minor_lines)

def draw_horizontal_line(drawing, group, grid_left, grid_right, y, thickness):
        y_centered = px_align(y, thickness)
        new_line = drawing.line(
            start=(grid_left, y_centered),
            end=(grid_right, y_centered))
        group.add(new_line)

def draw_vertical_line(drawing, group, grid_top, grid_bottom, x, thickness):
        x_centered = px_align(x, thickness)
        new_line = drawing.line(
            start=(x_centered, grid_top),
            end=(x_centered, grid_bottom))
        group.add(new_line)

def draw_horizontal_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters):
    grid_scale = parameters.grid_scale_y
    if grid_scale == 'timelog':
        draw_horizontal_timelog_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters)
        return
    horizontals = compute_scale(parameters.grid_height, grid_scale, parameters.grid_major_spacing, parameters.grid_minor_spacing)
    for dy_major in horizontals:
        draw_horizontal_line(drawing, major_group, grid_left, grid_right, grid_top + dy_major[0], parameters.grid_major_thickness)
        for dy_minor in dy_major[1:]:
            draw_horizontal_line(drawing, minor_group, grid_left, grid_right, grid_top + dy_minor, parameters.grid_minor_thickness)

def draw_vertical_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters):
    grid_scale = parameters.grid_scale_x
    if grid_scale == 'timelog':
        draw_vertical_timelog_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters)
        return
    verticals = compute_scale(parameters.grid_width, grid_scale, parameters.grid_major_spacing, parameters.grid_minor_spacing)
    for dx_major in verticals:
        draw_vertical_line(drawing, major_group, grid_top, grid_bottom, grid_left + dx_major[0], parameters.grid_major_thickness)
        for dx_minor in dx_major[1:]:
            draw_vertical_line(drawing, minor_group, grid_top, grid_bottom, grid_left + dx_minor, parameters.grid_minor_thickness)


# Fills 'width' pixels with a major/minor scale with 'timelog' axe.
# Returns an array of x/y coordinates arrays, each starting with a major point.
# [ { "unit", "s", "lines": [ major_0(==0), minor_0_0, minor_0_1, ...], "legends":[1,2,3...] } ... ]
def compute_timelog_scale(width, from_seconds, to_seconds):
    timelog_scales = [
        {
            "unit": "second",
            "value": 1,
            "range": 60,
            "minors": [2, 3, 4, 5, 10, 20, 30, 40, 50]
        }, {
            "unit": "minute",
            "value": 60,
            "range": 60,
            "minors": [2, 3, 4, 5, 10, 15, 20, 30, 45]
        }, {
            "unit": "hour",
            "value": 60 * 60,
            "range": 24,
            "minors": [2, 3, 4, 5, 6, 9, 12, 16, 20]
        }, {
            "unit": "day",
            "value": 60 * 60 * 24,
            "range": 7,
            "minors": [2, 3, 4, 5, 6]
        }, {
            "unit": "week",
            "value": 60 * 60 * 24 * 7,
            "range": 4,
            "minors": [2, 3]
        } ]

    full_width_ratio_log = np.log( to_seconds / from_seconds )
    sub_scales = []
    for ref_scale in timelog_scales:
        scale_part = {}
        scale_part["unit"] = ref_scale["unit"]
        base_value = ref_scale["value"]
        major_line = width * np.log( base_value / from_seconds ) / full_width_ratio_log
        minor_lines = list(map(lambda minor: width * np.log( base_value * minor / from_seconds ) / full_width_ratio_log, ref_scale["minors"]))
        tiny_lines = list(map(lambda minor: width * np.log( base_value * minor / from_seconds ) / full_width_ratio_log, range(ref_scale["range"])[1:]))
        scale_part["legends"] = [ 1 ] + ref_scale["minors"]
        scale_part["lines"] = [ major_line ] + minor_lines
        scale_part["tiny_lines"] = tiny_lines
        sub_scales.append( scale_part )
    return sub_scales

def textwidth(text, fontsize=14):
    return len(text) * fontsize * 0.6 # This is an empirical value

def draw_vertical_timelog_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters):
    width = grid_right - grid_left
    legend_group = drawing.g()
    legend_group.translate(grid_left, grid_bottom)
    grid_group.add(legend_group)
    verticals = compute_timelog_scale(parameters.grid_width, parameters.grid_time_x_start, parameters.grid_time_x_end)
    for scale_parts in verticals:
        lines = scale_parts["lines"]
        tiny_lines = scale_parts["tiny_lines"]
        dx_major = lines[0]
        if dx_major > width:
            return
        if dx_major >= 0:
            draw_vertical_line(drawing, major_group, grid_top, grid_bottom, grid_left + dx_major, parameters.grid_major_thickness)
        for dx_minor in tiny_lines[1:]:
            if dx_minor < 0:
                continue
            if dx_minor > width:
                break
            draw_vertical_line(drawing, minor_group, grid_top, grid_bottom, grid_left + dx_minor, parameters.grid_minor_thickness)
        # Display textual indicators too
        legends = scale_parts["legends"]
        unit = scale_parts["unit"]
        for legend in zip(legends, lines):
            dx = legend[1]
            if dx < 0:
                continue
            if dx > width:
                return
            legend_group.add( text_legend( drawing, legend, unit, parameters.scale_font_size) )

def draw_horizontal_timelog_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters):
    height = grid_bottom - grid_top
    legend_group = drawing.g()
    legend_group.translate(grid_left, grid_top)
    legend_group.rotate(90)
    grid_group.add(legend_group)
    horizontals = compute_timelog_scale(parameters.grid_height, parameters.grid_time_y_start, parameters.grid_time_y_end)
    for scale_parts in horizontals:
        lines = scale_parts["lines"]
        tiny_lines = scale_parts["tiny_lines"]
        dy_major = lines[0]
        if dy_major > height:
            return
        if dy_major >= 0:
            draw_horizontal_line(drawing, major_group, grid_left, grid_right, grid_top + dy_major, parameters.grid_major_thickness)
        for dy_minor in tiny_lines[1:]:
            if dy_minor < 0:
                continue
            if dy_minor > height:
                break
            draw_horizontal_line(drawing, minor_group, grid_left, grid_right, grid_top + dy_minor, parameters.grid_minor_thickness)
        # Display textual indicators too
        legends = scale_parts["legends"]
        unit = scale_parts["unit"]
        for legend in zip(legends, lines):
            dy = legend[1]
            if dy < 0:
                continue
            if dy > height:
                return
            legend_group.add( text_legend( drawing, legend, unit, parameters.scale_font_size) )

def text_legend(drawing, legend, unit, font_size=10):
            unit_value = legend[0] == 1
            text_legend = (str(legend[0]) + " " + unit) if unit_value else str(legend[0])
            text_size = font_size * ( 1.25 if unit_value else 1 )
            text_width = textwidth("1", text_size) if unit_value else textwidth(text_legend, text_size)
            dx_legend = legend[1]
            return drawing.text(text_legend, insert=(dx_legend - text_width/2, text_size + font_size / 2), font_size=font_size)

def draw_footer(drawing, main_group, parameters):
    footer_group = drawing.g(
        stroke=parameters.line_color,
        stroke_width=parameters.footer_line)
    main_group.add(footer_group)
    
    line_left = px_align(parameters.grid_x, parameters.grid_outline)
    line_right = px_align(parameters.grid_x + parameters.grid_width, parameters.grid_outline)
    
    line_y = parameters.grid_y + parameters.grid_height + parameters.footer_spacing
    while line_y < parameters.template_height_px:
        y = px_align(line_y, parameters.footer_line)
        footer_group.add(
            drawing.line(
                start=(line_left, y),
                end=(line_right, y)))
        line_y += parameters.footer_spacing
