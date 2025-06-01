"""
Chess Assets Module
Contains helper functions for drawing chess-themed UI elements
"""
import pygame
import math
import random

# Chess piece icons (enhanced 3D-style)
def draw_chess_icon(surface, piece_type, color, pos, size=40):
    """Draw a beautiful 3D-style chess piece icon"""
    x, y = pos

    # Ensure size is an integer to avoid TypeError
    size = int(size)

    # Define colors based on piece color - classic black-and-white
    if color == "white":
        # White pieces with classic finish
        main_color = (255, 255, 255)  # Pure white
        highlight_color = (255, 255, 255)  # Pure white for highlights
        shadow_color = (200, 200, 200)  # Light gray for shadows
        outline_color = (100, 100, 100)  # Gray outline
        detail_color = (50, 50, 50)  # Dark details
    else:
        # Black pieces with classic finish
        main_color = (0, 0, 0)  # Pure black
        highlight_color = (50, 50, 50)  # Dark gray for highlights
        shadow_color = (0, 0, 0)  # Black for shadows
        outline_color = (100, 100, 100)  # Gray outline
        detail_color = (200, 200, 200)  # Light details

    if piece_type == "pawn":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Stem
        pygame.draw.rect(surface, main_color, (x-size//8, y-size//6, size//4, size//2), border_radius=size//20)
        # Highlight on stem
        pygame.draw.rect(surface, highlight_color, (x-size//8, y-size//6, size//8, size//2), border_radius=size//20)

        # Head
        pygame.draw.circle(surface, main_color, (x, y-size//3), size//4)
        # Highlight on head
        pygame.draw.circle(surface, highlight_color, (x-size//12, y-size//3-size//12), size//6)

        # Outline
        pygame.draw.ellipse(surface, outline_color, (x-size//3, y+size//4, size//1.5, size//8), 1)
        pygame.draw.rect(surface, outline_color, (x-size//8, y-size//6, size//4, size//2), 1, border_radius=size//20)
        pygame.draw.circle(surface, outline_color, (x, y-size//3), size//4, 1)

    elif piece_type == "knight":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Body and head combined with smooth curves
        points = [
            (x-size//3, y+size//4),    # Bottom left
            (x-size//6, y-size//4),    # Middle left
            (x-size//8, y-size//2.5),  # Top left
            (x+size//8, y-size//2),    # Top middle
            (x+size//3, y-size//6),    # Top right
            (x+size//4, y+size//4)     # Bottom right
        ]

        # Draw main body
        pygame.draw.polygon(surface, main_color, points)

        # Highlight side
        highlight_points = [
            (x-size//3, y+size//4),    # Bottom left
            (x-size//6, y-size//4),    # Middle left
            (x-size//8, y-size//2.5),  # Top left
            (x+size//8, y-size//2),    # Top middle
            (x, y-size//6),            # Middle
            (x-size//8, y+size//4)     # Bottom middle
        ]
        pygame.draw.polygon(surface, highlight_color, highlight_points)

        # Mane details
        for i in range(3):
            y_offset = -size//6 + i*size//12
            pygame.draw.ellipse(surface, shadow_color, (x, y+y_offset, size//4, size//12))

        # Eye
        eye_x, eye_y = x+size//8, y-size//4
        pygame.draw.circle(surface, detail_color, (eye_x, eye_y), size//15)

        # Outline
        pygame.draw.polygon(surface, outline_color, points, 1)

    elif piece_type == "king":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Body
        pygame.draw.rect(surface, main_color, (x-size//6, y-size//4, size//3, size//2), border_radius=size//20)
        # Highlight on body
        pygame.draw.rect(surface, highlight_color, (x-size//6, y-size//4, size//6, size//2), border_radius=size//20)

        # Crown
        crown_radius = size//5
        pygame.draw.circle(surface, main_color, (x, y-size//3), crown_radius)
        # Highlight on crown
        pygame.draw.circle(surface, highlight_color, (x-size//12, y-size//3-size//12), crown_radius//2)

        # Cross on top
        cross_width = size//15
        cross_height = size//3

        # Vertical part of cross
        pygame.draw.rect(surface, detail_color, (x-cross_width//2, y-size//2, cross_width, cross_height))

        # Horizontal part of cross
        pygame.draw.rect(surface, detail_color, (x-size//6, y-size//2.5, size//3, cross_width))

        # Outlines
        pygame.draw.ellipse(surface, outline_color, (x-size//3, y+size//4, size//1.5, size//8), 1)
        pygame.draw.rect(surface, outline_color, (x-size//6, y-size//4, size//3, size//2), 1, border_radius=size//20)
        pygame.draw.circle(surface, outline_color, (x, y-size//3), crown_radius, 1)

    elif piece_type == "queen":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Body
        body_width = size//3
        body_height = size//2

        # Draw body as a trapezoid
        points = [
            (x-body_width//2, y+size//4),  # Bottom left
            (x+body_width//2, y+size//4),  # Bottom right
            (x+body_width//3, y-size//4),  # Top right
            (x-body_width//3, y-size//4)   # Top left
        ]
        pygame.draw.polygon(surface, main_color, points)

        # Highlight on body
        highlight_points = [
            (x-body_width//2, y+size//4),  # Bottom left
            (x, y+size//4),                # Bottom middle
            (x-body_width//6, y-size//4),  # Top middle
            (x-body_width//3, y-size//4)   # Top left
        ]
        pygame.draw.polygon(surface, highlight_color, highlight_points)

        # Crown
        crown_radius = size//5
        pygame.draw.circle(surface, main_color, (x, y-size//3), crown_radius)

        # Highlight on crown
        pygame.draw.circle(surface, highlight_color, (x-size//12, y-size//3-size//12), crown_radius//2)

        # Crown points/spikes
        num_points = 5
        for i in range(num_points):
            angle = math.pi/2 + i * 2*math.pi/num_points
            spike_length = size//6
            px = x + spike_length * math.cos(angle)
            py = y - size//3 + spike_length * math.sin(angle)

            # Draw spike
            pygame.draw.line(surface, main_color, (x, y-size//3), (px, py), 2)

            # Draw jewel at tip
            jewel_color = (220, 50, 50) if i % 2 == 0 else (50, 50, 220)  # Alternate red and blue
            if color == "black":
                # Darken jewels for black pieces
                jewel_color = (jewel_color[0]//2, jewel_color[1]//2, jewel_color[2]//2)

            pygame.draw.circle(surface, jewel_color, (int(px), int(py)), size//20)

        # Outlines
        pygame.draw.ellipse(surface, outline_color, (x-size//3, y+size//4, size//1.5, size//8), 1)
        pygame.draw.polygon(surface, outline_color, points, 1)
        pygame.draw.circle(surface, outline_color, (x, y-size//3), crown_radius, 1)

    elif piece_type == "rook":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Body
        body_width = size//3
        body_height = size//2
        pygame.draw.rect(surface, main_color, (x-body_width//2, y-size//4, body_width, body_height), border_radius=size//40)

        # Highlight on body
        pygame.draw.rect(surface, highlight_color, (x-body_width//2, y-size//4, body_width//2, body_height), border_radius=size//40)

        # Top battlements
        battlement_width = size//2.5
        battlement_height = size//8
        pygame.draw.rect(surface, main_color, (x-battlement_width//2, y-size//3, battlement_width, battlement_height))

        # Highlight on battlements
        pygame.draw.rect(surface, highlight_color, (x-battlement_width//2, y-size//3, battlement_width//2, battlement_height))

        # Crenellations (castle top)
        for i in range(3):
            x_offset = -size//6 + i*size//6
            cren_width = size//10
            cren_height = size//8
            pygame.draw.rect(surface, main_color, (x+x_offset-cren_width//2, y-size//2.5, cren_width, cren_height))

            # Highlight on crenellations
            if i == 0:  # Only highlight the leftmost crenellation
                pygame.draw.rect(surface, highlight_color, (x+x_offset-cren_width//2, y-size//2.5, cren_width//2, cren_height))

        # Outlines
        pygame.draw.ellipse(surface, outline_color, (x-size//3, y+size//4, size//1.5, size//8), 1)
        pygame.draw.rect(surface, outline_color, (x-body_width//2, y-size//4, body_width, body_height), 1, border_radius=size//40)
        pygame.draw.rect(surface, outline_color, (x-battlement_width//2, y-size//3, battlement_width, battlement_height), 1)

        for i in range(3):
            x_offset = -size//6 + i*size//6
            cren_width = size//10
            cren_height = size//8
            pygame.draw.rect(surface, outline_color, (x+x_offset-cren_width//2, y-size//2.5, cren_width, cren_height), 1)

    elif piece_type == "bishop":
        # Base
        pygame.draw.ellipse(surface, shadow_color, (x-size//3, y+size//4, size//1.5, size//8))

        # Body
        body_width_bottom = size//2.5
        body_width_top = size//4
        body_height = size//2

        # Draw body as a trapezoid
        points = [
            (x-body_width_bottom//2, y+size//4),  # Bottom left
            (x+body_width_bottom//2, y+size//4),  # Bottom right
            (x+body_width_top//2, y-size//4),     # Top right
            (x-body_width_top//2, y-size//4)      # Top left
        ]
        pygame.draw.polygon(surface, main_color, points)

        # Highlight on body
        highlight_points = [
            (x-body_width_bottom//2, y+size//4),  # Bottom left
            (x, y+size//4),                       # Bottom middle
            (x-body_width_top//4, y-size//4),     # Top middle
            (x-body_width_top//2, y-size//4)      # Top left
        ]
        pygame.draw.polygon(surface, highlight_color, highlight_points)

        # Head/mitre
        head_width = size//3
        head_height = size//4

        # Draw head as a triangle
        head_points = [
            (x, y-size//2.5),                    # Top
            (x-head_width//2, y-size//4),        # Bottom left
            (x+head_width//2, y-size//4)         # Bottom right
        ]
        pygame.draw.polygon(surface, main_color, head_points)

        # Highlight on head
        head_highlight_points = [
            (x, y-size//2.5),                    # Top
            (x-head_width//2, y-size//4),        # Bottom left
            (x-head_width//4, y-size//4)         # Bottom middle
        ]
        pygame.draw.polygon(surface, highlight_color, head_highlight_points)

        # Cross on top
        cross_color = detail_color
        pygame.draw.line(surface, cross_color, (x, y-size//2.5), (x, y-size//3), 2)
        pygame.draw.line(surface, cross_color, (x-size//12, y-size//2.8), (x+size//12, y-size//2.8), 2)

        # Outlines
        pygame.draw.ellipse(surface, outline_color, (x-size//3, y+size//4, size//1.5, size//8), 1)
        pygame.draw.polygon(surface, outline_color, points, 1)
        pygame.draw.polygon(surface, outline_color, head_points, 1)

# Chess board pattern
def draw_chess_board_pattern(surface, rect, light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=40):
    """Draw a chess board pattern in the given rectangle"""
    x, y, width, height = rect
    rows = height // square_size
    cols = width // square_size

    for row in range(rows):
        for col in range(cols):
            square_rect = (x + col * square_size, y + row * square_size, square_size, square_size)
            color = light_color if (row + col) % 2 == 0 else dark_color
            pygame.draw.rect(surface, color, square_rect)

# Decorative chess pieces for background
class DecorativePiece:
    def __init__(self, piece_type, color, x, y, size, speed, rotation_speed=None):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.rotation = random.randint(0, 360)
        self.rotation_speed = rotation_speed if rotation_speed is not None else random.uniform(-0.5, 0.5)
        self.alpha = random.randint(30, 80)
        self.pulse_speed = random.uniform(0.01, 0.05)
        self.pulse_amount = random.uniform(0.05, 0.15)
        self.pulse_offset = random.uniform(0, 6.28)  # Random phase offset (0 to 2π)

    def update(self, width, height):
        self.y += self.speed
        self.rotation += self.rotation_speed

        # Reset if off screen
        if self.y > height + self.size:
            self.y = -self.size
            self.x = random.randint(0, width)

    def draw(self, surface):
        # Calculate pulsing size effect
        time_factor = pygame.time.get_ticks() * self.pulse_speed / 1000
        pulse = 1 + self.pulse_amount * math.sin(time_factor + self.pulse_offset)
        current_size = self.size * pulse

        # Create a temporary surface for the piece with alpha
        temp_surface = pygame.Surface((current_size*2.5, current_size*2.5), pygame.SRCALPHA)
        draw_chess_icon(temp_surface, self.piece_type, self.color, (current_size, current_size), current_size)

        # Add glossy highlight effect
        self._add_glossy_highlight(temp_surface)

        # Add subtle glow effect
        glow_surface = pygame.Surface((current_size*3, current_size*3), pygame.SRCALPHA)
        glow_color = (255, 255, 255, 10) if self.color == "white" else (100, 100, 255, 10)
        pygame.draw.circle(glow_surface, glow_color, (current_size*1.5, current_size*1.5), current_size*1.2)
        temp_surface.blit(glow_surface, (current_size*0.25, current_size*0.25))

        # Apply rotation
        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation)

        # Apply alpha with slight pulsing
        alpha_pulse = self.alpha + int(10 * math.sin(time_factor * 1.5))
        alpha_pulse = max(20, min(alpha_pulse, 100))  # Keep alpha between 20 and 100
        rotated_surface.set_alpha(alpha_pulse)

        # Blit to main surface
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surface, rect)

    def _add_glossy_highlight(self, surface):
        """Add an enhanced glossy highlight effect to the piece"""
        # Get current size from the surface
        surf_width, surf_height = surface.get_size()
        center_x, center_y = surf_width // 2, surf_height // 2

        # Create a highlight surface
        highlight = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)

        # Determine highlight parameters based on piece color - classic black-and-white
        if self.color == "white":
            primary_highlight = (255, 255, 255, 70)  # Semi-transparent white
            secondary_highlight = (255, 255, 255, 40)  # White glow
        else:
            primary_highlight = (100, 100, 100, 40)  # Gray highlight for black pieces
            secondary_highlight = (50, 50, 50, 30)  # Dark gray glow

        # Calculate time-based animation for moving highlight
        time_factor = pygame.time.get_ticks() / 2000
        offset_x = math.sin(time_factor) * (self.size / 8)
        offset_y = math.cos(time_factor * 0.7) * (self.size / 10)

        # Draw main oval highlight
        highlight_width = self.size // 3
        highlight_height = self.size // 1.5
        highlight_rect = (
            center_x - highlight_width // 2 + offset_x,
            center_y - highlight_height // 2 + offset_y,
            highlight_width,
            highlight_height
        )
        pygame.draw.ellipse(highlight, primary_highlight, highlight_rect)

        # Add a small bright spot that moves slightly
        spot_x = center_x - self.size // 4 + offset_x * 1.5
        spot_y = center_y - self.size // 8 + offset_y * 1.5
        pygame.draw.circle(highlight, (255, 255, 255, 120), (spot_x, spot_y), self.size // 10)

        # Add a secondary highlight for depth
        secondary_rect = (
            center_x - highlight_width // 1.5,
            center_y - highlight_height // 3,
            highlight_width // 1.5,
            highlight_height // 2
        )
        pygame.draw.ellipse(highlight, secondary_highlight, secondary_rect)

        # Blit the highlight to the main surface
        surface.blit(highlight, (0, 0))

# Animated background with falling chess pieces and particle effects
class AnimatedChessBackground:
    def __init__(self, width, height, num_pieces=20):
        self.width = width
        self.height = height
        self.pieces = []
        self.particles = []
        self.stars = []
        self.time = 0

        # Create a subtle gradient effect
        self.gradient_offset = 0
        self.gradient_speed = 0.2

        # Create nebula-like clouds
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': random.randint(200, 400),
                'color': (
                    random.randint(40, 70),  # R
                    random.randint(40, 70),  # G
                    random.randint(80, 120), # B
                    random.randint(5, 15)    # Alpha
                ),
                'speed': random.uniform(0.05, 0.2),
                'direction': random.uniform(0, 2 * math.pi)
            })

        # Create stars (small bright points)
        for _ in range(150):
            size = random.uniform(0.5, 2)
            brightness = random.randint(150, 255)
            twinkle_speed = random.uniform(1, 3)
            self.stars.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': size,
                'color': (brightness, brightness, brightness, random.randint(100, 200)),
                'twinkle_speed': twinkle_speed,
                'twinkle_offset': random.uniform(0, 6.28)  # Random phase offset
            })

        piece_types = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        colors = ["white", "black"]

        # Create chess pieces with more elegant movement
        for _ in range(num_pieces):
            piece_type = random.choice(piece_types)
            color = random.choice(colors)
            x = random.randint(0, width)
            y = random.randint(-height, height)
            size = random.randint(30, 60)  # More consistent size range

            # Slower, more elegant movement
            speed = random.uniform(0.1, 0.5)
            rotation_speed = random.uniform(-0.3, 0.3)  # Gentler rotation

            self.pieces.append(DecorativePiece(piece_type, color, x, y, size, speed, rotation_speed))

        # Create particles for a more dynamic background (gold dust effect)
        for _ in range(80):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.uniform(0.8, 2)
            speed = random.uniform(0.05, 0.2)

            # Gold/amber particles
            r = random.randint(200, 255)
            g = random.randint(170, 220)
            b = random.randint(50, 100)
            a = random.randint(20, 60)

            self.particles.append({
                'x': x, 'y': y, 'size': size, 'speed': speed,
                'color': (r, g, b, a),
                'direction': random.uniform(0, 2 * math.pi)
            })

    def update(self):
        self.time += 0.01
        self.gradient_offset += self.gradient_speed
        if self.gradient_offset > 360:
            self.gradient_offset = 0

        # Update nebula clouds
        for cloud in self.clouds:
            cloud['x'] += math.cos(cloud['direction']) * cloud['speed']
            cloud['y'] += math.sin(cloud['direction']) * cloud['speed']

            # Wrap clouds around screen with padding
            padding = cloud['size']
            if cloud['x'] < -padding:
                cloud['x'] = self.width + padding
            elif cloud['x'] > self.width + padding:
                cloud['x'] = -padding
            if cloud['y'] < -padding:
                cloud['y'] = self.height + padding
            elif cloud['y'] > self.height + padding:
                cloud['y'] = -padding

            # Occasionally change direction slightly
            if random.random() < 0.005:
                cloud['direction'] += random.uniform(-0.1, 0.1)

        # Update chess pieces
        for piece in self.pieces:
            piece.update(self.width, self.height)

        # Update particles (gold dust)
        for particle in self.particles:
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']

            # Wrap particles around screen
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0

            # Occasionally change direction slightly for more natural movement
            if random.random() < 0.02:
                particle['direction'] += random.uniform(-0.3, 0.3)

    def draw(self, surface):
        # Draw cosmic gradient background
        gradient_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Create a subtle shifting gradient
        for y in range(0, self.height, 2):  # Step by 2 for performance
            # Calculate gradient color with subtle animation
            progress = y / self.height
            phase = (progress * 6.28 + self.time * 0.2) % 6.28

            # Deep blue to purple gradient
            r = int(45 + 10 * math.sin(phase))
            g = int(45 + 5 * math.sin(phase * 0.7))
            b = int(65 + 15 * math.sin(phase * 0.5))

            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (self.width, y))

        surface.blit(gradient_surface, (0, 0))

        # Draw nebula-like clouds
        for cloud in self.clouds:
            cloud_surface = pygame.Surface((cloud['size'] * 2, cloud['size'] * 2), pygame.SRCALPHA)

            # Create a soft, glowing cloud
            for radius in range(int(cloud['size']), 0, -10):
                # Vary alpha based on radius
                alpha_factor = radius / cloud['size']
                color = (
                    cloud['color'][0],
                    cloud['color'][1],
                    cloud['color'][2],
                    int(cloud['color'][3] * alpha_factor)
                )

                # Add some variation to the position for less perfect circles
                offset_x = random.uniform(-5, 5) if radius < cloud['size'] * 0.8 else 0
                offset_y = random.uniform(-5, 5) if radius < cloud['size'] * 0.8 else 0

                pygame.draw.circle(
                    cloud_surface,
                    color,
                    (int(cloud['size'] + offset_x), int(cloud['size'] + offset_y)),
                    radius
                )

            # Apply a subtle time-based distortion
            distortion = math.sin(self.time * 0.5) * 5
            cloud_rect = cloud_surface.get_rect(center=(cloud['x'] + distortion, cloud['y']))
            surface.blit(cloud_surface, cloud_rect)

        # Draw stars with twinkling effect
        for star in self.stars:
            # Calculate twinkling effect
            twinkle = math.sin(self.time * star['twinkle_speed'] + star['twinkle_offset'])
            size_mod = 1 + 0.3 * twinkle
            alpha_mod = 1 + 0.5 * twinkle

            # Apply modifications
            size = star['size'] * size_mod
            alpha = min(255, int(star['color'][3] * alpha_mod))
            color = (star['color'][0], star['color'][1], star['color'][2], alpha)

            # Draw the star
            pygame.draw.circle(
                surface,
                color,
                (int(star['x']), int(star['y'])),
                size
            )

            # Add a subtle glow to brighter stars
            if star['size'] > 1.5:
                glow_size = size * 2
                glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
                glow_color = (star['color'][0], star['color'][1], star['color'][2], 30)
                pygame.draw.circle(glow_surface, glow_color, (int(glow_size), int(glow_size)), int(glow_size))
                surface.blit(glow_surface, (int(star['x'] - glow_size), int(star['y'] - glow_size)))

        # Draw gold dust particles
        for particle in self.particles:
            # Pulse size and alpha slightly based on time
            pulse = math.sin(self.time * 2 + particle['x'] * 0.01)
            size_mod = 1 + 0.2 * pulse
            alpha_mod = 1 + 0.3 * pulse

            size = particle['size'] * size_mod
            alpha = min(255, int(particle['color'][3] * alpha_mod))
            color = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)

            pygame.draw.circle(
                surface,
                color,
                (int(particle['x']), int(particle['y'])),
                size
            )

        # Draw chess pieces
        for piece in self.pieces:
            piece.draw(surface)

# Fancy button with chess theme
def draw_chess_button(surface, rect, text, font, is_hovered=False, custom_color=None):
    """Draw an enhanced chess-themed button with modern visual effects"""
    x, y, width, height = rect

    # Get current time for animations
    current_time = pygame.time.get_ticks() / 1000

    # Base colors with classic black-and-white theme
    if custom_color:
        bg_color = custom_color  # Use custom color if provided
    else:
        bg_color = (30, 30, 30)  # Dark gray base color

    # Dynamic border color that subtly shifts over time when not hovered
    if not is_hovered:
        # Shift between shades of gray
        t = (math.sin(current_time * 0.7) + 1) / 2  # Value between 0 and 1
        r = g = b = int(150 + 20 * t)  # Gray base
        border_color = (r, g, b)
    else:
        # Brighter white pulsing when hovered
        t = (math.sin(current_time * 4) + 1) / 2  # Faster pulsing
        r = g = b = int(200 + 55 * t)
        border_color = (r, g, b)

    text_color = (240, 240, 240)  # White text

    # Create a surface for the button with a subtle glow
    glow_radius = 10
    button_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)

    # Draw white glow effect when hovered - classic black-and-white theme
    if is_hovered:
        for i in range(glow_radius, 0, -2):
            alpha = 5 - int(i * 5 / glow_radius)
            glow_color = (255, 255, 255, alpha)  # Pure white glow
            pygame.draw.rect(button_surface, glow_color,
                            (glow_radius - i, glow_radius - i,
                             width + i*2, height + i*2),
                            border_radius=10)

    # Draw button background with rounded corners and 3D effect - classic black-and-white
    pygame.draw.rect(button_surface, (20, 20, 20), (glow_radius, glow_radius + 2, width, height), border_radius=8)  # Shadow
    pygame.draw.rect(button_surface, bg_color, (glow_radius, glow_radius, width, height), border_radius=8)  # Main button

    # Draw inner gradient for 3D effect
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        # Top half gets lighter, bottom half gets darker
        if i < height / 2:
            alpha = 30 - int(i * 60 / height)
            color = (255, 255, 255, alpha)  # White gradient at top
        else:
            alpha = int((i - height/2) * 40 / (height/2))
            color = (0, 0, 0, alpha)  # Black gradient at bottom
        pygame.draw.line(gradient_surface, color, (0, i), (width, i))

    # Apply the gradient
    button_surface.blit(gradient_surface, (glow_radius, glow_radius))

    # Draw border with animated thickness when hovered
    border_width = 2
    if is_hovered:
        # Animate border thickness
        border_width = 2 + int(math.sin(current_time * 8) + 1)

    pygame.draw.rect(button_surface, border_color,
                    (glow_radius, glow_radius, width, height),
                    border_width, border_radius=8)

    # Draw text with shadow and glow effect
    text_size = 1.05 if is_hovered else 1.0

    # Shadow text - classic black-and-white
    shadow_surf = font.render(text, True, (20, 20, 20))
    shadow_rect = shadow_surf.get_rect(center=(width//2 + glow_radius + 2, height//2 + glow_radius + 2))
    button_surface.blit(shadow_surf, shadow_rect)

    # Main text
    text_surf = font.render(text, True, text_color)
    if is_hovered:
        # Scale text slightly larger when hovered
        original_size = text_surf.get_size()
        new_size = (int(original_size[0] * text_size), int(original_size[1] * text_size))
        text_surf = pygame.transform.scale(text_surf, new_size)

    # Add subtle white glow to text when hovered - classic black-and-white
    if is_hovered:
        glow_text = font.render(text, True, (255, 255, 255))
        glow_text.set_alpha(100)
        glow_rect = glow_text.get_rect(center=(width//2 + glow_radius, height//2 + glow_radius))
        button_surface.blit(glow_text, glow_rect.move(-1, -1))

    text_rect = text_surf.get_rect(center=(width//2 + glow_radius, height//2 + glow_radius))
    button_surface.blit(text_surf, text_rect)

    # Add animated chess icons based on button text
    icon_size = 20
    icon_x = 30
    icon_y = height // 2 + glow_radius

    # Determine which icon to use
    if "online quick match" in text.lower() or "quick" in text.lower():
        piece_type = "king"
        piece_color = "white"
    elif "create" in text.lower():
        piece_type = "king"
        piece_color = "white"
    elif "join" in text.lower():
        piece_type = "queen"
        piece_color = "black"
    elif "spectate" in text.lower():
        piece_type = "bishop"
        piece_color = "white"
    elif "back" in text.lower() or "exit" in text.lower():
        piece_type = "rook"
        piece_color = "black"
    else:
        piece_type = "pawn"
        piece_color = "white"

    # Create a temporary surface for the icon with rotation
    if is_hovered:
        # Animate icon when hovered
        rotation = current_time * 60 % 360
        icon_bounce = math.sin(current_time * 5) * 3
        icon_y += icon_bounce
    else:
        rotation = 0

    icon_surface = pygame.Surface((icon_size*3, icon_size*3), pygame.SRCALPHA)
    draw_chess_icon(icon_surface, piece_type, piece_color, (icon_size*1.5, icon_size*1.5), icon_size)

    if is_hovered:
        # Add glow to icon when hovered
        for i in range(3):
            glow_size = icon_size + i*2
            glow_alpha = 30 - i*10
            glow_surf = pygame.Surface((glow_size*3, glow_size*3), pygame.SRCALPHA)
            if piece_color == "white":
                glow_color = (255, 255, 200, glow_alpha)
            else:
                glow_color = (100, 150, 255, glow_alpha)
            pygame.draw.circle(glow_surf, glow_color, (glow_size*1.5, glow_size*1.5), glow_size)
            icon_surface.blit(glow_surf, ((icon_size*3 - glow_size*3)//2, (icon_size*3 - glow_size*3)//2))

    # Rotate icon if hovered
    if is_hovered:
        icon_surface = pygame.transform.rotate(icon_surface, rotation)

    # Blit icon to button
    icon_rect = icon_surface.get_rect(center=(icon_x, icon_y))
    button_surface.blit(icon_surface, icon_rect)

    # Blit the final button to the main surface
    surface.blit(button_surface, (x - glow_radius, y - glow_radius))

# Fancy panel with chess theme
def draw_chess_panel(surface, rect, border_color=(200, 200, 200), bg_color=(40, 40, 40), pattern=True):
    """Draw an enhanced chess-themed panel with modern visual effects"""
    x, y, width, height = rect

    # Get current time for animations
    current_time = pygame.time.get_ticks() / 1000

    # Create a surface for the panel with a subtle glow
    panel_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
    glow_radius = 10

    # Draw subtle outer glow
    for i in range(glow_radius, 0, -2):
        alpha = 3 - int(i * 3 / glow_radius)
        glow_color = (border_color[0], border_color[1], border_color[2], alpha)
        pygame.draw.rect(panel_surface, glow_color,
                        (glow_radius - i, glow_radius - i,
                         width + i*2, height + i*2),
                        border_radius=12)

    # Draw panel background with rounded corners and subtle 3D effect
    shadow_offset = 3
    pygame.draw.rect(panel_surface, (20, 20, 50),
                    (glow_radius, glow_radius + shadow_offset, width, height),
                    border_radius=10)  # Shadow
    pygame.draw.rect(panel_surface, bg_color,
                    (glow_radius, glow_radius, width, height),
                    border_radius=10)  # Main panel

    # Draw inner gradient for depth
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        # Top gets lighter, bottom gets slightly darker
        if i < height / 4:
            alpha = 15 - int(i * 60 / height)
            color = (255, 255, 255, alpha)  # White gradient at top
        elif i > height * 3/4:
            alpha = int((i - height*3/4) * 20 / (height/4))
            color = (0, 0, 0, alpha)  # Black gradient at bottom
        else:
            color = (0, 0, 0, 0)  # Transparent in middle
        pygame.draw.line(gradient_surface, color, (0, i), (width, i))

    # Apply the gradient
    panel_surface.blit(gradient_surface, (glow_radius, glow_radius))

    # Draw animated border
    # Make border color slightly pulse
    t = (math.sin(current_time * 0.8) + 1) / 2  # Value between 0 and 1
    r = int(border_color[0] * (0.9 + 0.1 * t))
    g = int(border_color[1] * (0.9 + 0.1 * t))
    b = int(border_color[2] * (0.9 + 0.1 * t))
    animated_border_color = (r, g, b)

    pygame.draw.rect(panel_surface, animated_border_color,
                    (glow_radius, glow_radius, width, height),
                    2, border_radius=10)

    # Draw chess pattern on the top and bottom if requested
    if pattern:
        # Create pattern with enhanced visual style
        pattern_height = 12
        pattern_rect_top = (glow_radius + 15, glow_radius + 5, width - 30, pattern_height)
        pattern_rect_bottom = (glow_radius + 15, glow_radius + height - pattern_height - 5, width - 30, pattern_height)

        # Draw patterns with slight glow
        pattern_surface_top = pygame.Surface((width - 30, pattern_height), pygame.SRCALPHA)
        pattern_surface_bottom = pygame.Surface((width - 30, pattern_height), pygame.SRCALPHA)

        # Draw chess patterns with classic black-and-white color scheme
        draw_chess_board_pattern(pattern_surface_top, (0, 0, width - 30, pattern_height), light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=6)
        draw_chess_board_pattern(pattern_surface_bottom, (0, 0, width - 30, pattern_height), light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=6)

        # Add subtle glow to patterns
        glow_surface = pygame.Surface((width - 30, pattern_height), pygame.SRCALPHA)
        for i in range(pattern_height):
            alpha = 20 - abs(i - pattern_height/2) * 40 / pattern_height
            pygame.draw.line(glow_surface, (255, 255, 255, int(alpha)), (0, i), (width - 30, i))

        pattern_surface_top.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        pattern_surface_bottom.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        # Apply patterns to panel
        panel_surface.blit(pattern_surface_top, pattern_rect_top[:2])
        panel_surface.blit(pattern_surface_bottom, pattern_rect_bottom[:2])

        # Add decorative borders around patterns
        pygame.draw.rect(panel_surface, animated_border_color,
                        (pattern_rect_top[0] - 2, pattern_rect_top[1] - 2,
                         pattern_rect_top[2] + 4, pattern_rect_top[3] + 4),
                        1, border_radius=3)
        pygame.draw.rect(panel_surface, animated_border_color,
                        (pattern_rect_bottom[0] - 2, pattern_rect_bottom[1] - 2,
                         pattern_rect_bottom[2] + 4, pattern_rect_bottom[3] + 4),
                        1, border_radius=3)

    # Blit the final panel to the main surface
    surface.blit(panel_surface, (x - glow_radius, y - glow_radius))

# Fancy input box with chess theme
def draw_chess_input(surface, rect, text, placeholder, font, small_font, is_active=False):
    """Draw an enhanced chess-themed input box with modern visual effects"""
    x, y, width, height = rect

    # Get current time for animations
    current_time = pygame.time.get_ticks() / 1000

    # Create a surface for the input box with a subtle glow
    input_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
    glow_radius = 10

    # Base colors with enhanced aesthetics
    bg_color = (240, 240, 240)  # Light background for input

    # Animated border color - classic black-and-white
    if is_active:
        # Pulsing white when active
        t = (math.sin(current_time * 2) + 1) / 2  # Value between 0 and 1
        r = g = b = int(200 + 55 * t)
        border_color = (r, g, b)
    else:
        # Subtle gray when inactive
        border_color = (150, 150, 150)

    text_color = (40, 40, 40)  # Dark text
    placeholder_color = (120, 120, 120)  # Gray placeholder

    # Draw subtle glow effect when active
    if is_active:
        for i in range(glow_radius, 0, -2):
            alpha = 5 - int(i * 5 / glow_radius)
            glow_color = (border_color[0], border_color[1], border_color[2], alpha)
            pygame.draw.rect(input_surface, glow_color,
                            (glow_radius - i, glow_radius - i,
                             width + i*2, height + i*2),
                            border_radius=10)

    # Draw input background with rounded corners and subtle 3D effect
    shadow_offset = 2
    pygame.draw.rect(input_surface, (180, 180, 180),
                    (glow_radius, glow_radius + shadow_offset, width, height),
                    border_radius=8)  # Shadow
    pygame.draw.rect(input_surface, bg_color,
                    (glow_radius, glow_radius, width, height),
                    border_radius=8)  # Main input

    # Draw inner gradient for 3D effect
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        if i < height / 2:
            alpha = 10 - int(i * 20 / height)
            color = (255, 255, 255, alpha)  # White gradient at top
        else:
            alpha = int((i - height/2) * 10 / (height/2))
            color = (0, 0, 0, alpha)  # Black gradient at bottom
        pygame.draw.line(gradient_surface, color, (0, i), (width, i))

    # Apply the gradient
    input_surface.blit(gradient_surface, (glow_radius, glow_radius))

    # Draw border with animated thickness when active
    border_width = 2
    if is_active:
        # Animate border thickness
        border_width = 2 + int(math.sin(current_time * 4) + 1)

    pygame.draw.rect(input_surface, border_color,
                    (glow_radius, glow_radius, width, height),
                    border_width, border_radius=8)

    # Draw decorative chess pattern on the left side with classic black-and-white color scheme
    pattern_width = 20
    pattern_rect = (glow_radius + 5, glow_radius + 5, pattern_width, height - 10)
    pattern_surface = pygame.Surface((pattern_width, height - 10), pygame.SRCALPHA)
    draw_chess_board_pattern(pattern_surface, (0, 0, pattern_width, height - 10), light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=5)

    # Add subtle glow to pattern
    pattern_glow = pygame.Surface((pattern_width, height - 10), pygame.SRCALPHA)
    for i in range(height - 10):
        alpha = 30 - abs(i - (height - 10)/2) * 60 / (height - 10)
        pygame.draw.line(pattern_glow, (255, 255, 255, int(alpha)), (0, i), (pattern_width, i))

    # Apply glow to pattern and add to input
    if is_active:
        pattern_surface.blit(pattern_glow, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    input_surface.blit(pattern_surface, pattern_rect[:2])

    # Draw text or placeholder with shadow
    padding = pattern_width + 15
    if text:
        # Draw text shadow
        shadow_surf = font.render(text, True, (100, 100, 100))
        shadow_rect = shadow_surf.get_rect(x=glow_radius + padding + 1, centery=glow_radius + height // 2 + 1)
        input_surface.blit(shadow_surf, shadow_rect)

        # Draw main text
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(x=glow_radius + padding, centery=glow_radius + height // 2)
        input_surface.blit(text_surf, text_rect)
    else:
        # Draw placeholder with subtle animation
        alpha = int(180 + 30 * math.sin(current_time * 2))
        placeholder_surf = small_font.render(placeholder, True, placeholder_color)
        placeholder_surf.set_alpha(alpha)
        placeholder_rect = placeholder_surf.get_rect(x=glow_radius + padding, centery=glow_radius + height // 2)
        input_surface.blit(placeholder_surf, placeholder_rect)

    # Draw animated cursor if active
    if is_active:
        cursor_x = glow_radius + padding + (font.size(text)[0] if text else 0)
        # Smooth cursor animation
        cursor_alpha = int(200 + 55 * math.sin(current_time * 5))
        cursor_surface = pygame.Surface((2, height - 20), pygame.SRCALPHA)
        cursor_color = (0, 0, 0, cursor_alpha)
        pygame.draw.rect(cursor_surface, cursor_color, (0, 0, 2, height - 20))
        input_surface.blit(cursor_surface, (cursor_x, glow_radius + 10))

    # Blit the final input box to the main surface
    surface.blit(input_surface, (x - glow_radius, y - glow_radius))

# Game list item with chess theme
def draw_chess_game_item(surface, rect, game_name, host_name, guest_name=None, status="waiting", is_hovered=False):
    """Draw an enhanced chess-themed game list item with modern visual effects"""
    x, y, width, height = rect

    # Get current time for animations
    current_time = pygame.time.get_ticks() / 1000

    # Create a surface for the game item with a subtle glow
    item_surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
    glow_radius = 10

    # Base colors with classic black-and-white aesthetics
    bg_color = (30, 30, 30) if not is_hovered else (50, 50, 50)  # Dark gray, slightly lighter when hovered

    # Dynamic border color
    if is_hovered:
        # Animated white border when hovered
        t = (math.sin(current_time * 3) + 1) / 2  # Value between 0 and 1
        r = g = b = int(200 + 55 * t)
        border_color = (r, g, b)
    else:
        # Subtle gray pulsing when not hovered
        t = (math.sin(current_time * 0.7) + 1) / 2  # Value between 0 and 1
        r = g = b = int(120 + 30 * t)
        border_color = (r, g, b)

    text_color = (240, 240, 240)  # White text

    # Status colors with animation - classic black-and-white
    base_status_colors = {
        "waiting": (200, 200, 200),  # Light gray
        "in_progress": (255, 255, 255)  # White
    }

    # Animate status colors
    status_color = base_status_colors[status]
    if status == "waiting":
        # Pulsing yellow for waiting
        t = (math.sin(current_time * 2) + 1) / 2  # Value between 0 and 1
        r = int(status_color[0] * (0.9 + 0.1 * t))
        g = int(status_color[1] * (0.9 + 0.1 * t))
        b = int(status_color[2] * (0.9 + 0.1 * t))
        status_color = (r, g, b)
    else:
        # Pulsing green for in progress
        t = (math.sin(current_time * 1.5) + 1) / 2  # Value between 0 and 1
        r = int(status_color[0] * (0.9 + 0.1 * t))
        g = int(status_color[1] * (0.9 + 0.1 * t))
        b = int(status_color[2] * (0.9 + 0.1 * t))
        status_color = (r, g, b)

    # Draw subtle glow effect when hovered
    if is_hovered:
        for i in range(glow_radius, 0, -2):
            alpha = 5 - int(i * 5 / glow_radius)
            glow_color = (border_color[0], border_color[1], border_color[2], alpha)
            pygame.draw.rect(item_surface, glow_color,
                            (glow_radius - i, glow_radius - i,
                             width + i*2, height + i*2),
                            border_radius=10)

    # Draw item background with rounded corners and subtle 3D effect
    shadow_offset = 3
    pygame.draw.rect(item_surface, (20, 20, 50),
                    (glow_radius, glow_radius + shadow_offset, width, height),
                    border_radius=8)  # Shadow
    pygame.draw.rect(item_surface, bg_color,
                    (glow_radius, glow_radius, width, height),
                    border_radius=8)  # Main item

    # Draw inner gradient for 3D effect
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        # Top gets lighter, bottom gets slightly darker
        if i < height / 4:
            alpha = 15 - int(i * 60 / height)
            color = (255, 255, 255, alpha)  # White gradient at top
        elif i > height * 3/4:
            alpha = int((i - height*3/4) * 20 / (height/4))
            color = (0, 0, 0, alpha)  # Black gradient at bottom
        else:
            color = (0, 0, 0, 0)  # Transparent in middle
        pygame.draw.line(gradient_surface, color, (0, i), (width, i))

    # Apply the gradient
    item_surface.blit(gradient_surface, (glow_radius, glow_radius))

    # Draw border with animated thickness when hovered
    border_width = 1
    if is_hovered:
        # Animate border thickness
        border_width = 1 + int(math.sin(current_time * 6) + 1)

    pygame.draw.rect(item_surface, border_color,
                    (glow_radius, glow_radius, width, height),
                    border_width, border_radius=8)

    # Draw enhanced mini chess board on the left with 3D effect
    board_size = height - 24
    board_x = glow_radius + 15
    board_y = glow_radius + 12
    board_rect = (board_x, board_y, board_size, board_size)

    # Create board surface with shadow
    board_surface = pygame.Surface((board_size + 6, board_size + 6), pygame.SRCALPHA)
    pygame.draw.rect(board_surface, (20, 20, 20, 100), (3, 3, board_size, board_size))  # Shadow

    # Draw the chess board pattern with classic black-and-white color scheme
    board_inner = pygame.Surface((board_size, board_size), pygame.SRCALPHA)
    draw_chess_board_pattern(board_inner, (0, 0, board_size, board_size), light_color=(255, 255, 255), dark_color=(0, 0, 0), square_size=board_size//8)

    # Add subtle highlight to board
    highlight = pygame.Surface((board_size, board_size), pygame.SRCALPHA)
    for i in range(board_size):
        alpha = 20 - int(i * 40 / board_size)
        if alpha > 0:
            pygame.draw.line(highlight, (255, 255, 255, alpha), (0, i), (board_size, i))
    board_inner.blit(highlight, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    # Add board to surface with shadow effect
    board_surface.blit(board_inner, (0, 0))
    item_surface.blit(board_surface, board_rect[:2])

    # Draw animated border around board
    pygame.draw.rect(item_surface, border_color,
                    (board_x - 1, board_y - 1, board_size + 2, board_size + 2),
                    1, border_radius=2)

    # Prepare fonts with better styling
    font_large = pygame.font.SysFont('Arial', 24)
    font_small = pygame.font.SysFont('Arial', 18)

    # Game name with shadow and glow - limit length to prevent overflow
    if len(game_name) > 15:
        game_name = game_name[:15] + "..."

    # Draw name shadow
    name_shadow = font_large.render(game_name, True, (20, 20, 40))
    item_surface.blit(name_shadow, (board_x + board_size + 32, board_y + 17))

    # Draw name with subtle glow if hovered
    name_text = font_large.render(game_name, True, text_color)
    if is_hovered:
        # Add subtle glow to text
        glow_text = font_large.render(game_name, True, (255, 255, 200))
        glow_text.set_alpha(50)
        item_surface.blit(glow_text, (board_x + board_size + 29, board_y + 14))

    item_surface.blit(name_text, (board_x + board_size + 30, board_y + 15))

    # Enhanced status badge with glow and animation
    status_text = "Waiting for player" if status == "waiting" else "In progress"
    status_badge = font_small.render(status_text, True, (240, 240, 240))
    badge_width = status_badge.get_width() + 20
    badge_height = 25
    badge_x = glow_radius + width - badge_width - 20
    badge_y = board_y + 15

    # Draw badge with animated glow
    badge_glow_size = 3
    for i in range(badge_glow_size, 0, -1):
        alpha = 10 - i * 3
        glow_color = (status_color[0], status_color[1], status_color[2], alpha)
        pygame.draw.rect(item_surface, glow_color,
                        (badge_x - i, badge_y - i, badge_width + i*2, badge_height + i*2),
                        border_radius=12)

    # Draw badge background with gradient
    pygame.draw.rect(item_surface, status_color,
                    (badge_x, badge_y, badge_width, badge_height),
                    border_radius=12)

    # Add subtle gradient to badge
    badge_gradient = pygame.Surface((badge_width, badge_height), pygame.SRCALPHA)
    for i in range(badge_height):
        alpha = 30 - int(i * 60 / badge_height)
        # Ensure alpha is not negative
        alpha = max(0, alpha)
        pygame.draw.line(badge_gradient, (255, 255, 255, alpha), (0, i), (badge_width, i))

    # Create a mask for the rounded rectangle
    mask = pygame.Surface((badge_width, badge_height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, badge_width, badge_height), border_radius=12)

    # Apply mask to gradient
    badge_gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Apply gradient to badge
    item_surface.blit(badge_gradient, (badge_x, badge_y))

    # Draw badge text with shadow
    shadow_offset = 1
    badge_shadow = font_small.render(status_text, True, (0, 0, 0, 100))
    item_surface.blit(badge_shadow, (badge_x + 10 + shadow_offset, badge_y + 4 + shadow_offset))
    item_surface.blit(status_badge, (badge_x + 10, badge_y + 4))

    # Player info section with enhanced styling
    player_section_x = board_x + board_size + 30

    # Host name with animated white king icon
    king_offset = 0
    if is_hovered:
        king_offset = math.sin(current_time * 3) * 2

    # Draw white king with glow
    king_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    if is_hovered:
        # Add glow to king when hovered
        pygame.draw.circle(king_surface, (255, 255, 200, 30), (16, 16), 12)
    draw_chess_icon(king_surface, "king", "white", (16, 16), 16)
    item_surface.blit(king_surface, (player_section_x, board_y + 45 + king_offset))

    # Draw host text with shadow
    host_shadow = font_small.render(f"White: {host_name}", True, (20, 20, 40))
    item_surface.blit(host_shadow, (player_section_x + 21, board_y + 39))
    host_text = font_small.render(f"White: {host_name}", True, (220, 220, 220))
    item_surface.blit(host_text, (player_section_x + 20, board_y + 38))

    # Guest name with animated black king icon if game is in progress
    if status == "in_progress" and guest_name:
        # Draw black king with glow
        king_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        if is_hovered:
            # Add glow to king when hovered
            pygame.draw.circle(king_surface, (100, 100, 255, 30), (16, 16), 12)
            # Add animation
            king_offset = math.sin(current_time * 3 + 1) * 2
        draw_chess_icon(king_surface, "king", "black", (16, 16), 16)
        item_surface.blit(king_surface, (player_section_x, board_y + 65 + king_offset))

        # Draw guest text with shadow
        guest_shadow = font_small.render(f"Black: {guest_name}", True, (20, 20, 40))
        item_surface.blit(guest_shadow, (player_section_x + 21, board_y + 59))
        guest_text = font_small.render(f"Black: {guest_name}", True, (220, 220, 220))
        item_surface.blit(guest_text, (player_section_x + 20, board_y + 58))

    # Blit the final item to the main surface
    surface.blit(item_surface, (x - glow_radius, y - glow_radius))
