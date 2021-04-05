#!/usr/bin/env python3

import math

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

    next_major = parameters.grid_major_spacing
    dy = parameters.grid_minor_spacing
    while dy < parameters.grid_height:
        is_major = abs(next_major - dy) < parameters.grid_minor_spacing / 2
        y = px_align(grid_top + dy, parameters.grid_major_thickness if is_major else parameters.grid_minor_thickness)
        new_line = drawing.line(
            start=(grid_left, y),
            end=(grid_right, y))
        if is_major:
            major_group.add(new_line)
            next_major += parameters.grid_major_spacing
        else:
            minor_group.add(new_line)
        dy += parameters.grid_minor_spacing

    next_major = parameters.grid_major_spacing
    dx = parameters.grid_minor_spacing
    while dx < parameters.grid_width:
        is_major = abs(next_major - dx) < parameters.grid_minor_spacing / 2
        x = px_align(grid_left + dx, parameters.grid_major_thickness if is_major else parameters.grid_minor_thickness)
        new_line = drawing.line(
            start=(x, grid_top),
            end=(x, grid_bottom))
        if is_major:
            major_group.add(new_line)
            next_major += parameters.grid_major_spacing
        else:
            minor_group.add(new_line)
        dx += parameters.grid_minor_spacing
        
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
