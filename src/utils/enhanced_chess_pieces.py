"""
Enhanced Chess Pieces Module
Contains functions for creating beautiful 3D-style chess pieces
"""
import pygame
import math

def create_enhanced_piece_images(square_size=80):
    """Create beautiful 3D-looking chess piece images with enhanced visual effects"""
    images = {}

    # Define piece types and colors
    piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']

    for color in colors:
        for piece_type in piece_types:
            # Create a surface with alpha channel
            surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)

            # Center coordinates
            cx, cy = square_size // 2, square_size // 2

            # Define colors based on piece color
            if color == 'white':
                # White pieces with luxury marble-like finish
                main_color = (245, 245, 245)  # Base white
                highlight_color = (255, 255, 255)  # Pure white for highlights
                shadow_color = (200, 200, 200)  # Light gray for shadows
                outline_color = (100, 100, 100)  # Softer outline
                detail_color = (50, 50, 50)  # Dark details

                # Gradient colors for 3D effect
                grad1 = (255, 255, 255)  # Brightest
                grad2 = (245, 245, 245)  # Medium
                grad3 = (220, 220, 220)  # Darker

                # Gold accents for white pieces
                accent_color = (255, 215, 0)  # Gold
                accent_shadow = (200, 170, 0)  # Darker gold
            else:
                # Black pieces with polished ebony-like finish
                main_color = (30, 30, 30)  # Base black
                highlight_color = (80, 80, 80)  # Dark gray for highlights
                shadow_color = (10, 10, 10)  # Very dark gray for shadows
                outline_color = (120, 120, 120)  # Lighter outline
                detail_color = (200, 200, 200)  # Light details

                # Gradient colors for 3D effect
                grad1 = (70, 70, 70)  # Lightest
                grad2 = (40, 40, 40)  # Medium
                grad3 = (20, 20, 20)  # Darkest

                # Silver accents for black pieces
                accent_color = (200, 200, 220)  # Silver
                accent_shadow = (150, 150, 170)  # Darker silver

            # Draw different pieces with enhanced 3D effects
            if piece_type == 'pawn':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Stem with more elegant shape
                stem_height = 22
                stem_width = 12
                stem_top_width = 8

                # Draw stem as a trapezoid with gradient
                stem_points = [
                    (cx-stem_width//2, cy+2),       # Bottom left
                    (cx+stem_width//2, cy+2),       # Bottom right
                    (cx+stem_top_width//2, cy-18),  # Top right
                    (cx-stem_top_width//2, cy-18)   # Top left
                ]
                draw_gradient_polygon(surface, stem_points, grad1, grad2, grad3)

                # Head with more elegant shape
                head_radius = 14
                draw_gradient_circle(surface, cx, cy-22, head_radius, grad1, grad2, grad3)

                # Add decorative collar where stem meets head
                collar_height = 4
                collar_width = 14
                collar_rect = (cx-collar_width//2, cy-20, collar_width, collar_height)
                pygame.draw.rect(surface, accent_color, collar_rect, border_radius=2)
                pygame.draw.rect(surface, accent_shadow, (cx-collar_width//2, cy-20+collar_height//2, collar_width, collar_height//2), border_radius=2)

                # Add decorative detail to head
                detail_radius = 6
                if color == 'white':
                    # Gold circle on white pawn
                    pygame.draw.circle(surface, accent_color, (cx, cy-22), detail_radius)
                    pygame.draw.circle(surface, accent_shadow, (cx, cy-22), detail_radius, 1)
                else:
                    # Silver circle on black pawn
                    pygame.draw.circle(surface, accent_color, (cx, cy-22), detail_radius)
                    pygame.draw.circle(surface, accent_shadow, (cx, cy-22), detail_radius, 1)

                # Outlines
                pygame.draw.polygon(surface, outline_color, stem_points, 1)
                pygame.draw.circle(surface, outline_color, (cx, cy-22), head_radius, 1)
                pygame.draw.rect(surface, outline_color, collar_rect, 1, border_radius=2)

            elif piece_type == 'rook':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Body with more elegant shape
                body_width_bottom = 24
                body_width_top = 20
                body_height = 30

                # Draw body as a trapezoid with gradient
                body_points = [
                    (cx-body_width_bottom//2, cy+2),       # Bottom left
                    (cx+body_width_bottom//2, cy+2),       # Bottom right
                    (cx+body_width_top//2, cy-28),         # Top right
                    (cx-body_width_top//2, cy-28)          # Top left
                ]
                draw_gradient_polygon(surface, body_points, grad1, grad2, grad3)

                # Add decorative band in the middle
                band_height = 5
                band_y = cy - 12
                band_width = body_width_bottom - 4
                pygame.draw.rect(surface, accent_color, (cx-band_width//2, band_y, band_width, band_height), border_radius=1)
                pygame.draw.rect(surface, accent_shadow, (cx-band_width//2, band_y+band_height//2, band_width, band_height//2), border_radius=1)
                pygame.draw.rect(surface, outline_color, (cx-band_width//2, band_y, band_width, band_height), 1, border_radius=1)

                # Top with crenellations
                top_width = 30
                top_height = 8
                top_y = cy - 28

                # Draw top with gradient
                top_rect = (cx-top_width//2, top_y, top_width, top_height)
                draw_gradient_rect(surface, cx-top_width//2, top_y, top_width, top_height, grad1, grad2, grad3, vertical=True)
                pygame.draw.rect(surface, outline_color, top_rect, 1)

                # Crenellations with more detail
                cren_width = 6
                cren_height = 8
                cren_spacing = 8

                for i in range(4):
                    cren_x = cx - top_width//2 + i*cren_spacing + 3
                    cren_y = top_y - cren_height

                    # Draw crenellation with gradient
                    draw_gradient_rect(surface, cren_x, cren_y, cren_width, cren_height, grad1, grad2, grad3, vertical=True)

                    # Add accent to top of crenellation
                    pygame.draw.rect(surface, accent_color, (cren_x, cren_y, cren_width, 2))

                    # Outline
                    pygame.draw.rect(surface, outline_color, (cren_x, cren_y, cren_width, cren_height), 1)

                # Outlines for main body
                pygame.draw.polygon(surface, outline_color, body_points, 1)

            elif piece_type == 'knight':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Body and head with more elegant horse shape
                knight_points = [
                    (cx-12, cy+2),     # Bottom left
                    (cx-8, cy-8),      # Middle left
                    (cx-6, cy-15),     # Neck left
                    (cx-8, cy-25),     # Head back
                    (cx-2, cy-30),     # Head top
                    (cx+6, cy-28),     # Head front
                    (cx+10, cy-22),    # Nose
                    (cx+8, cy-15),     # Mouth
                    (cx+12, cy-8),     # Chest
                    (cx+8, cy+2)       # Bottom right
                ]

                # Draw the knight shape with gradient
                draw_gradient_polygon(surface, knight_points, grad1, grad2, grad3)

                # Add mane with accent color
                mane_points = [
                    (cx-6, cy-15),     # Neck left
                    (cx-8, cy-25),     # Head back
                    (cx-2, cy-30),     # Head top
                    (cx-4, cy-20),     # Middle of mane
                    (cx-2, cy-15)      # Bottom of mane
                ]
                pygame.draw.polygon(surface, accent_color, mane_points)
                pygame.draw.polygon(surface, accent_shadow, mane_points, 1)

                # Add decorative bridle
                bridle_points = [
                    (cx+6, cy-28),     # Head top front
                    (cx+10, cy-22),    # Nose
                    (cx+8, cy-15),     # Mouth
                    (cx+4, cy-18)      # Middle of face
                ]
                pygame.draw.lines(surface, accent_color, False, bridle_points, 2)

                # Eye
                eye_x, eye_y = cx+5, cy-24
                pygame.draw.circle(surface, detail_color, (eye_x, eye_y), 2)

                # Nostril
                nostril_x, nostril_y = cx+8, cy-20
                pygame.draw.ellipse(surface, detail_color, (nostril_x-1, nostril_y-2, 2, 3))

                # Outline
                pygame.draw.polygon(surface, outline_color, knight_points, 1)

            elif piece_type == 'bishop':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Body with more elegant shape
                body_width_bottom = 22
                body_width_top = 12

                # Draw body as a trapezoid with gradient
                body_points = [
                    (cx-body_width_bottom//2, cy+2),  # Bottom left
                    (cx+body_width_bottom//2, cy+2),  # Bottom right
                    (cx+body_width_top//2, cy-20),    # Top right
                    (cx-body_width_top//2, cy-20)     # Top left
                ]
                draw_gradient_polygon(surface, body_points, grad1, grad2, grad3)

                # Add decorative collar
                collar_height = 4
                collar_y = cy - 10
                collar_width = body_width_bottom - 6
                pygame.draw.rect(surface, accent_color, (cx-collar_width//2, collar_y, collar_width, collar_height), border_radius=2)
                pygame.draw.rect(surface, accent_shadow, (cx-collar_width//2, collar_y+collar_height//2, collar_width, collar_height//2), border_radius=2)
                pygame.draw.rect(surface, outline_color, (cx-collar_width//2, collar_y, collar_width, collar_height), 1, border_radius=2)

                # Head/mitre with more elegant shape
                mitre_width_bottom = 16
                mitre_width_top = 8
                mitre_height = 20

                # Draw mitre as a trapezoid with gradient
                mitre_points = [
                    (cx-mitre_width_bottom//2, cy-20),  # Bottom left
                    (cx+mitre_width_bottom//2, cy-20),  # Bottom right
                    (cx+mitre_width_top//2, cy-40),     # Top right
                    (cx-mitre_width_top//2, cy-40)      # Top left
                ]
                draw_gradient_polygon(surface, mitre_points, grad1, grad2, grad3)

                # Add decorative band to mitre
                band_height = 3
                band_y = cy - 25
                band_width = mitre_width_bottom - 4
                pygame.draw.rect(surface, accent_color, (cx-band_width//2, band_y, band_width, band_height), border_radius=1)
                pygame.draw.rect(surface, outline_color, (cx-band_width//2, band_y, band_width, band_height), 1, border_radius=1)

                # Cross on top with accent color
                cross_width = 4
                cross_height = 10
                cross_y = cy - 50

                # Vertical part of cross
                pygame.draw.rect(surface, accent_color, (cx-cross_width//2, cross_y, cross_width, cross_height))
                pygame.draw.rect(surface, outline_color, (cx-cross_width//2, cross_y, cross_width, cross_height), 1)

                # Horizontal part of cross
                pygame.draw.rect(surface, accent_color, (cx-6, cross_y+3, 12, cross_width))
                pygame.draw.rect(surface, outline_color, (cx-6, cross_y+3, 12, cross_width), 1)

                # Outlines
                pygame.draw.polygon(surface, outline_color, body_points, 1)
                pygame.draw.polygon(surface, outline_color, mitre_points, 1)

            elif piece_type == 'queen':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Body with more elegant shape
                body_width_bottom = 24
                body_width_top = 16

                # Draw body as a trapezoid with gradient
                body_points = [
                    (cx-body_width_bottom//2, cy+2),  # Bottom left
                    (cx+body_width_bottom//2, cy+2),  # Bottom right
                    (cx+body_width_top//2, cy-25),    # Top right
                    (cx-body_width_top//2, cy-25)     # Top left
                ]
                draw_gradient_polygon(surface, body_points, grad1, grad2, grad3)

                # Add decorative bands
                # Lower band
                lower_band_height = 4
                lower_band_y = cy - 8
                lower_band_width = body_width_bottom - 6
                pygame.draw.rect(surface, accent_color, (cx-lower_band_width//2, lower_band_y, lower_band_width, lower_band_height), border_radius=2)
                pygame.draw.rect(surface, accent_shadow, (cx-lower_band_width//2, lower_band_y+lower_band_height//2, lower_band_width, lower_band_height//2), border_radius=2)
                pygame.draw.rect(surface, outline_color, (cx-lower_band_width//2, lower_band_y, lower_band_width, lower_band_height), 1, border_radius=2)

                # Upper band
                upper_band_height = 3
                upper_band_y = cy - 18
                upper_band_width = body_width_top + 2
                pygame.draw.rect(surface, accent_color, (cx-upper_band_width//2, upper_band_y, upper_band_width, upper_band_height), border_radius=1)
                pygame.draw.rect(surface, accent_shadow, (cx-upper_band_width//2, upper_band_y+upper_band_height//2, upper_band_width, upper_band_height//2), border_radius=1)
                pygame.draw.rect(surface, outline_color, (cx-upper_band_width//2, upper_band_y, upper_band_width, upper_band_height), 1, border_radius=1)

                # Crown base
                crown_radius = 12
                crown_y = cy - 30
                draw_gradient_circle(surface, cx, crown_y, crown_radius, grad1, grad2, grad3)
                pygame.draw.circle(surface, outline_color, (cx, crown_y), crown_radius, 1)

                # Crown points/spikes with jewels
                num_points = 5
                for i in range(num_points):
                    angle = math.pi/2 + i * 2*math.pi/num_points
                    spike_length = 14
                    spike_width = 3

                    # Calculate spike points
                    px = cx + spike_length * math.cos(angle)
                    py = crown_y + spike_length * math.sin(angle)

                    # Draw spike with gradient
                    spike_points = [
                        (cx + (crown_radius-1) * math.cos(angle-0.1), crown_y + (crown_radius-1) * math.sin(angle-0.1)),
                        (cx + (crown_radius-1) * math.cos(angle+0.1), crown_y + (crown_radius-1) * math.sin(angle+0.1)),
                        (px, py)
                    ]
                    draw_gradient_polygon(surface, spike_points, grad1, grad2, grad3)
                    pygame.draw.polygon(surface, outline_color, spike_points, 1)

                    # Draw jewel at tip with accent color and glow
                    jewel_radius = 4

                    # Draw glow around jewel
                    for r in range(3):
                        glow_radius = jewel_radius + 2 - r
                        glow_alpha = 100 - r * 30
                        glow_color = (accent_color[0], accent_color[1], accent_color[2], glow_alpha)
                        glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
                        surface.blit(glow_surface, (int(px)-glow_radius, int(py)-glow_radius))

                    # Draw main jewel
                    pygame.draw.circle(surface, accent_color, (int(px), int(py)), jewel_radius)
                    pygame.draw.circle(surface, accent_shadow, (int(px), int(py)), jewel_radius, 1)

                # Outlines for main body
                pygame.draw.polygon(surface, outline_color, body_points, 1)

            elif piece_type == 'king':
                # Base
                draw_elliptical_base(surface, cx, cy, color, accent_color)

                # Body with more elegant shape
                body_width_bottom = 24
                body_width_top = 16

                # Draw body as a trapezoid with gradient
                body_points = [
                    (cx-body_width_bottom//2, cy+2),  # Bottom left
                    (cx+body_width_bottom//2, cy+2),  # Bottom right
                    (cx+body_width_top//2, cy-25),    # Top right
                    (cx-body_width_top//2, cy-25)     # Top left
                ]
                draw_gradient_polygon(surface, body_points, grad1, grad2, grad3)

                # Add decorative bands
                # Lower band
                lower_band_height = 4
                lower_band_y = cy - 8
                lower_band_width = body_width_bottom - 6
                pygame.draw.rect(surface, accent_color, (cx-lower_band_width//2, lower_band_y, lower_band_width, lower_band_height), border_radius=2)
                pygame.draw.rect(surface, accent_shadow, (cx-lower_band_width//2, lower_band_y+lower_band_height//2, lower_band_width, lower_band_height//2), border_radius=2)
                pygame.draw.rect(surface, outline_color, (cx-lower_band_width//2, lower_band_y, lower_band_width, lower_band_height), 1, border_radius=2)

                # Upper band
                upper_band_height = 3
                upper_band_y = cy - 18
                upper_band_width = body_width_top + 2
                pygame.draw.rect(surface, accent_color, (cx-upper_band_width//2, upper_band_y, upper_band_width, upper_band_height), border_radius=1)
                pygame.draw.rect(surface, accent_shadow, (cx-upper_band_width//2, upper_band_y+upper_band_height//2, upper_band_width, upper_band_height//2), border_radius=1)
                pygame.draw.rect(surface, outline_color, (cx-upper_band_width//2, upper_band_y, upper_band_width, upper_band_height), 1, border_radius=1)

                # Crown base
                crown_radius = 12
                crown_y = cy - 30
                draw_gradient_circle(surface, cx, crown_y, crown_radius, grad1, grad2, grad3)
                pygame.draw.circle(surface, outline_color, (cx, crown_y), crown_radius, 1)

                # Cross on top with accent color
                cross_width = 5
                cross_height = 18
                cross_y = cy - 42

                # Vertical part of cross
                # Draw with accent color
                pygame.draw.rect(surface, accent_color, (cx-cross_width//2, cross_y, cross_width, cross_height), border_radius=1)
                # Add shadow effect
                pygame.draw.rect(surface, accent_shadow, (cx-cross_width//2+1, cross_y, cross_width//2, cross_height), border_radius=1)
                # Outline
                pygame.draw.rect(surface, outline_color, (cx-cross_width//2, cross_y, cross_width, cross_height), 1, border_radius=1)

                # Horizontal part of cross
                h_cross_width = 14
                h_cross_height = cross_width
                h_cross_y = cross_y + 4

                # Draw with accent color
                pygame.draw.rect(surface, accent_color, (cx-h_cross_width//2, h_cross_y, h_cross_width, h_cross_height), border_radius=1)
                # Add shadow effect
                pygame.draw.rect(surface, accent_shadow, (cx-h_cross_width//2, h_cross_y+h_cross_height//2, h_cross_width, h_cross_height//2), border_radius=1)
                # Outline
                pygame.draw.rect(surface, outline_color, (cx-h_cross_width//2, h_cross_y, h_cross_width, h_cross_height), 1, border_radius=1)

                # Add small decorative jewel at cross intersection
                jewel_radius = 3
                pygame.draw.circle(surface, accent_color, (cx, h_cross_y + h_cross_height//2), jewel_radius)
                pygame.draw.circle(surface, outline_color, (cx, h_cross_y + h_cross_height//2), jewel_radius, 1)

                # Outlines for main body
                pygame.draw.polygon(surface, outline_color, body_points, 1)

            # Add shadow beneath piece for 3D effect
            shadow_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            shadow_radius = 15
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 40), (cx-shadow_radius, cy+15, shadow_radius*2, 8))
            surface.blit(shadow_surface, (0, 0))

            # Add glossy highlight effect
            add_glossy_highlight(surface, cx, cy, square_size, color)

            # Store the image
            images[(piece_type, color)] = surface

    return images

def draw_elliptical_base(surface, cx, cy, color, accent_color=None):
    """Draw an elliptical base for the chess piece with optional accent"""
    if color == 'white':
        base_colors = [(245, 245, 245), (230, 230, 230), (210, 210, 210)]
    else:
        base_colors = [(50, 50, 50), (30, 30, 30), (10, 10, 10)]

    # Base width and height
    base_width = 36
    base_height = 12

    # Draw multiple ellipses for 3D effect
    pygame.draw.ellipse(surface, base_colors[2], (cx-base_width//2, cy+10, base_width, base_height))
    pygame.draw.ellipse(surface, base_colors[1], (cx-base_width//2, cy+8, base_width, base_height))
    pygame.draw.ellipse(surface, base_colors[0], (cx-base_width//2, cy+6, base_width, base_height))

    # Add accent ring if accent_color is provided
    if accent_color:
        accent_width = 30
        accent_height = 6
        pygame.draw.ellipse(surface, accent_color, (cx-accent_width//2, cy+8, accent_width, accent_height))

    # Outline
    pygame.draw.ellipse(surface, (100, 100, 100) if color == 'white' else (150, 150, 150),
                       (cx-base_width//2, cy+6, base_width, base_height), 1)

def draw_gradient_rect(surface, x, y, width, height, color1, color2, color3, vertical=True, border_radius=0):
    """Draw a rectangle with a gradient effect"""
    # Ensure width and height are integers
    width = int(width)
    height = int(height)

    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    if vertical:
        # Vertical gradient
        for i in range(height):
            # Determine position in gradient (0 to 1)
            pos = i / height

            # Calculate color based on position
            if pos < 0.5:
                # Blend from color1 to color2
                blend_pos = pos * 2  # Scale to 0-1 range
                r = int(color1[0] * (1 - blend_pos) + color2[0] * blend_pos)
                g = int(color1[1] * (1 - blend_pos) + color2[1] * blend_pos)
                b = int(color1[2] * (1 - blend_pos) + color2[2] * blend_pos)
            else:
                # Blend from color2 to color3
                blend_pos = (pos - 0.5) * 2  # Scale to 0-1 range
                r = int(color2[0] * (1 - blend_pos) + color3[0] * blend_pos)
                g = int(color2[1] * (1 - blend_pos) + color3[1] * blend_pos)
                b = int(color2[2] * (1 - blend_pos) + color3[2] * blend_pos)

            pygame.draw.line(temp_surface, (r, g, b), (0, i), (width, i))
    else:
        # Horizontal gradient
        for i in range(width):
            # Determine position in gradient (0 to 1)
            pos = i / width

            # Calculate color based on position
            if pos < 0.5:
                # Blend from color1 to color2
                blend_pos = pos * 2  # Scale to 0-1 range
                r = int(color1[0] * (1 - blend_pos) + color2[0] * blend_pos)
                g = int(color1[1] * (1 - blend_pos) + color2[1] * blend_pos)
                b = int(color1[2] * (1 - blend_pos) + color2[2] * blend_pos)
            else:
                # Blend from color2 to color3
                blend_pos = (pos - 0.5) * 2  # Scale to 0-1 range
                r = int(color2[0] * (1 - blend_pos) + color3[0] * blend_pos)
                g = int(color2[1] * (1 - blend_pos) + color3[1] * blend_pos)
                b = int(color2[2] * (1 - blend_pos) + color3[2] * blend_pos)

            pygame.draw.line(temp_surface, (r, g, b), (i, 0), (i, height))

    # Apply border radius if needed
    if border_radius > 0:
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=border_radius)
        temp_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Blit to main surface
    surface.blit(temp_surface, (x, y))

def draw_gradient_circle(surface, x, y, radius, color1, color2, color3):
    """Draw a circle with a gradient effect"""
    # Ensure radius is an integer
    radius = int(radius)

    temp_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    # Draw from outside in with different colors
    pygame.draw.circle(temp_surface, color3, (radius, radius), radius)
    pygame.draw.circle(temp_surface, color2, (radius, radius), int(radius * 0.7))
    pygame.draw.circle(temp_surface, color1, (radius, radius), int(radius * 0.4))

    # Blit to main surface
    surface.blit(temp_surface, (x-radius, y-radius))

def draw_gradient_polygon(surface, points, color1, color2, color3):
    """Draw a polygon with a gradient effect"""
    # Find bounding box of polygon
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    width = int(max_x - min_x + 1)
    height = int(max_y - min_y + 1)

    # Create temporary surface for gradient
    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Draw gradient on temp surface
    for y in range(height):
        # Determine position in gradient (0 to 1)
        pos = y / height

        # Calculate color based on position
        if pos < 0.3:
            # Blend from color1 to color2
            blend_pos = pos / 0.3  # Scale to 0-1 range
            r = int(color1[0] * (1 - blend_pos) + color2[0] * blend_pos)
            g = int(color1[1] * (1 - blend_pos) + color2[1] * blend_pos)
            b = int(color1[2] * (1 - blend_pos) + color2[2] * blend_pos)
        else:
            # Blend from color2 to color3
            blend_pos = (pos - 0.3) / 0.7  # Scale to 0-1 range
            r = int(color2[0] * (1 - blend_pos) + color3[0] * blend_pos)
            g = int(color2[1] * (1 - blend_pos) + color3[1] * blend_pos)
            b = int(color2[2] * (1 - blend_pos) + color3[2] * blend_pos)

        pygame.draw.line(temp_surface, (r, g, b), (0, y), (width, y))

    # Create mask from polygon
    mask = pygame.Surface((width, height), pygame.SRCALPHA)

    # Adjust points to be relative to temp surface
    adjusted_points = [(int(p[0] - min_x), int(p[1] - min_y)) for p in points]

    # Draw polygon on mask
    pygame.draw.polygon(mask, (255, 255, 255), adjusted_points)

    # Apply mask to gradient
    temp_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Blit to main surface
    surface.blit(temp_surface, (min_x, min_y))

def draw_gradient_triangle(surface, x, y, width, height, color1, color2, color3):
    """Draw a triangle with a gradient effect"""
    # Ensure width and height are integers
    width = int(width)
    height = int(height)

    points = [
        (x, y),                  # Top
        (x - width//2, y + height),  # Bottom left
        (x + width//2, y + height)   # Bottom right
    ]
    draw_gradient_polygon(surface, points, color1, color2, color3)

def add_glossy_highlight(surface, cx, cy, size, color):
    """Add an enhanced glossy highlight effect to the piece"""
    # Create a highlight surface
    highlight = pygame.Surface((size, size), pygame.SRCALPHA)

    # Determine highlight parameters based on piece color
    if color == 'white':
        primary_highlight = (255, 255, 255, 120)  # Semi-transparent white
        secondary_highlight = (255, 255, 220, 80)  # Warm glow
        spot_highlight = (255, 255, 255, 180)      # Bright spot
    else:
        primary_highlight = (255, 255, 255, 60)    # More transparent white for black pieces
        secondary_highlight = (180, 180, 255, 40)  # Cool blue glow
        spot_highlight = (255, 255, 255, 100)      # Bright spot

    # Draw main oval highlight (top-left to bottom-right)
    highlight_width = int(size // 2)
    highlight_height = int(size // 2)
    highlight_offset_x = int(-size // 8)
    highlight_offset_y = int(-size // 6)

    highlight_rect = (
        cx + highlight_offset_x - highlight_width // 2,
        cy + highlight_offset_y - highlight_height // 2,
        highlight_width,
        highlight_height
    )
    pygame.draw.ellipse(highlight, primary_highlight, highlight_rect)

    # Draw secondary highlight (bottom-right)
    secondary_width = int(size // 3)
    secondary_height = int(size // 4)
    secondary_offset_x = int(size // 6)
    secondary_offset_y = int(size // 5)

    secondary_rect = (
        cx + secondary_offset_x - secondary_width // 2,
        cy + secondary_offset_y - secondary_height // 2,
        secondary_width,
        secondary_height
    )
    pygame.draw.ellipse(highlight, secondary_highlight, secondary_rect)

    # Add a small bright spot at the top-left
    spot_radius = int(size // 15)
    spot_offset_x = int(-size // 6)
    spot_offset_y = int(-size // 6)

    pygame.draw.circle(highlight, spot_highlight,
                      (cx + spot_offset_x, cy + spot_offset_y), spot_radius)

    # Add a subtle overall shine
    for i in range(3):
        shine_radius = int(size // 2 - i * (size // 10))
        shine_alpha = 10 - i * 3
        if shine_alpha > 0:
            shine_color = (255, 255, 255, shine_alpha)
            pygame.draw.circle(highlight, shine_color, (cx, cy), shine_radius)

    # Blit the highlight to the main surface
    surface.blit(highlight, (0, 0))
