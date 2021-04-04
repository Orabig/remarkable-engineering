#!/usr/bin/env python3

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
    main_group.add(header_group)
    header_group.add(
        drawing.rect(
            insert=(parameters.header_title_x, parameters.header_y),
            size=(parameters.header_title_width, parameters.header_height)))
    header_group.add(
        drawing.rect(
            insert=(parameters.header_date_x, parameters.header_y),
            size=(parameters.header_date_width, parameters.header_height)))
    
def draw_grid(drawing, main_group, parameters):
    grid_group = drawing.g(stroke=parameters.line_color)
    main_group.add(grid_group)

    grid_group.add(
        drawing.rect(
            fill='none',
            insert=(parameters.grid_x, parameters.grid_y),
            size=(parameters.grid_width, parameters.grid_height),
            stroke_width=parameters.grid_outline))

    major_group = drawing.g(stroke_width=parameters.grid_major_thickness)
    minor_group = drawing.g(stroke_width=parameters.grid_minor_thickness)
    grid_group.add(major_group)
    grid_group.add(minor_group)

    grid_left = parameters.grid_x
    grid_right = parameters.grid_x + parameters.grid_width
    grid_top = parameters.grid_y
    grid_bottom = parameters.grid_y + parameters.grid_height
    
    next_major = parameters.grid_major_spacing
    dy = parameters.grid_minor_spacing
    while dy < parameters.grid_height:
        new_line = drawing.line(
            start=(grid_left, grid_top + dy),
            end=(grid_right, grid_top + dy))
        if abs(next_major - dy) < parameters.grid_minor_spacing / 2:
            major_group.add(new_line)
            next_major += parameters.grid_major_spacing
        else:
            minor_group.add(new_line)
        dy += parameters.grid_minor_spacing

    next_major = parameters.grid_major_spacing
    dx = parameters.grid_minor_spacing
    while dx < parameters.grid_width:
        new_line = drawing.line(
            start=(grid_left + dx, grid_top),
            end=(grid_left + dx, grid_bottom))
        if abs(next_major - dx) < parameters.grid_minor_spacing / 2:
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
    
    line_left = parameters.grid_x
    line_right = parameters.grid_x + parameters.grid_width
    
    line_y = parameters.grid_y + parameters.grid_height + parameters.footer_spacing
    while line_y < parameters.template_height_px:
        footer_group.add(
            drawing.line(
                start=(line_left, line_y),
                end=(line_right, line_y)))
        line_y += parameters.footer_spacing
