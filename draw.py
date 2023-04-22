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
def compute_scale(width, type, major_spacing, minor_spacing):
    major_count = 1 + round(width / major_spacing)
    real_spacing = width / major_count
    major_lines = np.linspace(0, width, major_count, endpoint=False)
    if type == 'log':
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
    horizontals = compute_scale(parameters.grid_height, parameters.grid_scale_y, parameters.grid_major_spacing, parameters.grid_minor_spacing)
    for dy_major in horizontals:
        draw_horizontal_line(drawing, major_group, grid_left, grid_right, grid_top + dy_major[0], parameters.grid_major_thickness)
        for dy_minor in dy_major[1:]:
            draw_horizontal_line(drawing, minor_group, grid_left, grid_right, grid_top + dy_minor, parameters.grid_minor_thickness)

def draw_vertical_grid(drawing, grid_group, major_group, minor_group, grid_left, grid_right, grid_top, grid_bottom, parameters):
    verticals = compute_scale(parameters.grid_width, parameters.grid_scale_x, parameters.grid_major_spacing, parameters.grid_minor_spacing)
    for dx_major in verticals:
        draw_vertical_line(drawing, major_group, grid_top, grid_bottom, grid_left + dx_major[0], parameters.grid_major_thickness)
        for dx_minor in dx_major[1:]:
            draw_vertical_line(drawing, minor_group, grid_top, grid_bottom, grid_left + dx_minor, parameters.grid_minor_thickness)

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
