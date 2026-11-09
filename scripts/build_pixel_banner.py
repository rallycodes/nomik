#!/usr/bin/env python3
"""
Pixel Banner SVG Generator
Generates a pristine, minimalist black-and-white pixel/terminal banner for Nomik.
"""

def generate_banner_svg():
    font = {
        'N': [
            '11000011',
            '11100011',
            '11110011',
            '11011011',
            '11011011',
            '11001111',
            '11000111',
            '11000011',
            '11000011'
        ],
        'O': [
            '00111100',
            '01111110',
            '11000011',
            '11000011',
            '11000011',
            '11000011',
            '11000011',
            '01111110',
            '00111100'
        ],
        'M': [
            '110000011',
            '111000111',
            '111101111',
            '110111011',
            '110010011',
            '110000011',
            '110000011',
            '110000011',
            '110000011'
        ],
        'I': [
            '111111',
            '001100',
            '001100',
            '001100',
            '001100',
            '001100',
            '001100',
            '001100',
            '111111'
        ],
        'K': [
            '11000011',
            '11000110',
            '11001100',
            '11011000',
            '11110000',
            '11011000',
            '11001100',
            '11000110',
            '11000011'
        ]
    }

    word = 'NOMIK'
    spacing = 2
    px_size = 9
    gap = 2.5
    pitch = px_size + gap

    # Calculate total width to center perfectly
    char_widths = [len(font[c][0]) for c in word]
    total_cols = sum(char_widths) + (len(word) - 1) * spacing
    total_width = total_cols * pitch

    svg_width = 1200
    svg_height = 360

    start_x = (svg_width - total_width) / 2
    start_y = 100

    pixel_rects = []
    curr_x = start_x
    for char in word:
        grid = font[char]
        char_cols = len(grid[0])
        for r_idx, row in enumerate(grid):
            for c_idx, val in enumerate(row):
                if val == '1':
                    x = curr_x + c_idx * pitch
                    y = start_y + r_idx * pitch
                    pixel_rects.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{px_size}" height="{px_size}" rx="1" fill="#FFFFFF"/>')
        curr_x += (char_cols + spacing) * pitch

    pixel_svg = "\n".join(pixel_rects)

    # Dot matrix background pattern
    dot_pattern = []
    for dx in range(50, 1160, 24):
        for dy in range(40, 330, 24):
            dot_pattern.append(f'<circle cx="{dx}" cy="{dy}" r="0.75" fill="#222222"/>')
    dots_svg = "\n    ".join(dot_pattern)

    svg_content = f'''<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Minimalist Pitch Black Canvas -->
  <rect width="{svg_width}" height="{svg_height}" fill="#050505"/>
  <rect x="0.5" y="0.5" width="{svg_width-1}" height="{svg_height-1}" stroke="#1F1F1F" stroke-width="1"/>

  <!-- Subtle Pixel Dot-Matrix Background -->
  <g opacity="0.6">
    {dots_svg}
  </g>

  <!-- Technical Corner Registration Crosshairs -->
  <g stroke="#444444" stroke-width="1">
    <!-- Top-Left -->
    <line x1="20" y1="20" x2="32" y2="20"/>
    <line x1="20" y1="20" x2="20" y2="32"/>
    <!-- Top-Right -->
    <line x1="1180" y1="20" x2="1168" y2="20"/>
    <line x1="1180" y1="20" x2="1180" y2="32"/>
    <!-- Bottom-Left -->
    <line x1="20" y1="340" x2="32" y2="340"/>
    <line x1="20" y1="340" x2="20" y2="328"/>
    <!-- Bottom-Right -->
    <line x1="1180" y1="340" x2="1168" y2="340"/>
    <line x1="1180" y1="340" x2="1180" y2="328"/>
  </g>

  <!-- Top Monospace Status Header -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-size="11" letter-spacing="2" fill="#71717A">
    <text x="56" y="52">[SYS.01] NOMIK TERMINAL</text>
    <text x="600" y="52" text-anchor="middle" fill="#A1A1AA">THE AI SKILL THAT NAMED ITSELF</text>
    <text x="1144" y="52" text-anchor="end">BY RAUL ALIYEV (@RALLYCODES)</text>
  </g>

  <!-- Hairline Divider -->
  <line x1="56" y1="68" x2="1144" y2="68" stroke="#1F1F1F" stroke-width="1"/>

  <!-- Centered Pixelated NOMIK Typography -->
  <g id="pixel-wordmark">
{pixel_svg}
  </g>

  <!-- Terminal Subtitle -->
  <g transform="translate(600, 245)" text-anchor="middle">
    <text font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-weight="500" font-size="14" letter-spacing="3" fill="#E4E4E7">
      &gt; BILLION-DOLLAR BRAND NAMING &amp; DOMAIN ENGINE<tspan fill="#71717A">_</tspan>
    </text>
    <text y="28" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif" font-weight="400" font-size="14" letter-spacing="0.2" fill="#71717A">
      Cognitive phonosemantics, zero AI slop, and real-time ICANN verification.
    </text>
  </g>

  <!-- Bottom Hairline Divider -->
  <line x1="56" y1="300" x2="1144" y2="300" stroke="#1F1F1F" stroke-width="1"/>

  <!-- Bottom Terminal Status Bar -->
  <g transform="translate(56, 324)" font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-size="10" letter-spacing="1.5" fill="#71717A">
    <text x="0" y="0"><tspan fill="#A1A1AA">[01]</tspan> 7 AGENCY TAXONOMIES</text>
    <text x="270" y="0"><tspan fill="#A1A1AA">[02]</tspan> ZERO AI SLOP CODE</text>
    <text x="540" y="0"><tspan fill="#A1A1AA">[03]</tspan> REAL-TIME ICANN RDAP</text>
    <text x="810" y="0"><tspan fill="#A1A1AA">[04]</tspan> TRADEMARK KNOCKOUT</text>
    <text x="1088" y="0" text-anchor="end" fill="#52525B">MIT LICENSE</text>
  </g>
</svg>'''
    return svg_content

if __name__ == '__main__':
    svg = generate_banner_svg()
    with open('c:/Users/RAUL/Downloads/skills/nomik/assets/banner.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated pixel banner SVG successfully!")

