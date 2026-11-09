#!/usr/bin/env python3
"""
Pixel Banner SVG Generator v3
Generates an ultra-clean, museum-grade monochrome pixel/terminal banner for Nomik.
"""

def generate_pixel_banner():
    # 11-row pixel font with smooth diagonal on N and balanced geometry
    font_11 = {
        'N': [
            '1100000011',
            '1110000011',
            '1111000011',
            '1101100011',
            '1100110011',
            '1100110011',
            '1100011011',
            '1100001111',
            '1100000111',
            '1100000111',
            '1100000011'
        ],
        'O': [
            '0011111100',
            '0111111110',
            '1100000011',
            '1100000011',
            '1100000011',
            '1100000011',
            '1100000011',
            '1100000011',
            '1100000011',
            '0111111110',
            '0011111100'
        ],
        'M': [
            '11000000011',
            '11100000111',
            '11110001111',
            '11011011011',
            '11001110011',
            '11000100011',
            '11000000011',
            '11000000011',
            '11000000011',
            '11000000011',
            '11000000011'
        ],
        'I': [
            '11111111',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '00011000',
            '11111111'
        ],
        'K': [
            '1100000011',
            '1100000110',
            '1100001100',
            '1100011000',
            '1100110000',
            '1111100000',
            '1100110000',
            '1100011000',
            '1100001100',
            '1100000110',
            '1100000011'
        ]
    }

    svg_w, svg_h = 1200, 380
    px_size = 9
    gap = 2
    pitch = px_size + gap

    word = ['N', 'O', 'M', 'I', 'K']
    spacings = [3, 3, 3, 3] # spacing cols between letters: N-O, O-M, M-I, I-K

    # Compute total width
    char_widths = [len(font_11[c][0]) for c in word]
    total_cols = sum(char_widths) + sum(spacings) # 10+3 + 10+3 + 11+3 + 8+3 + 10 = 61 cols
    total_width = total_cols * pitch # 61 * 11 = 671px

    # Mathematically centered on canvas
    start_x = (svg_w - total_width) / 2 # 264.5px
    start_y = 96

    rects = []
    curr_x = start_x
    for idx, c in enumerate(word):
        grid = font_11[c]
        cols = len(grid[0])
        for r_idx, row in enumerate(grid):
            for c_idx, val in enumerate(row):
                if val == '1':
                    x = curr_x + c_idx * pitch
                    y = start_y + r_idx * pitch
                    rects.append(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{px_size}" height="{px_size}" rx="0.5" fill="#FFFFFF"/>')
        curr_x += cols * pitch
        if idx < len(spacings):
            curr_x += spacings[idx] * pitch

    pixel_svg = "\n".join(rects)

    # Dot matrix background pattern
    dot_pattern = []
    for dx in range(40, svg_w - 40, 24):
        for dy in range(40, svg_h - 40, 24):
            dot_pattern.append(f'<circle cx="{dx}" cy="{dy}" r="0.6" fill="#141418"/>')
    dots_svg = "\n    ".join(dot_pattern)

    # Framing reticle coordinates
    ret_pad_x = 36
    ret_pad_y = 14
    ret_x1 = start_x - ret_pad_x
    ret_x2 = start_x + total_width + ret_pad_x
    ret_y1 = start_y - ret_pad_y
    ret_y2 = start_y + (11 * pitch) + ret_pad_y
    ret_arm = 16

    svg_content = f'''<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Minimalist Pitch Black Canvas -->
  <rect width="{svg_w}" height="{svg_h}" fill="#050505"/>
  <rect x="0.5" y="0.5" width="{svg_w-1}" height="{svg_h-1}" stroke="#1F1F24" stroke-width="1"/>

  <!-- Subtle Hardware Dot-Matrix Pattern -->
  <g opacity="0.6">
    {dots_svg}
  </g>

  <!-- Precision Corner Registration Crosshairs -->
  <g stroke="#3F3F46" stroke-width="1">
    <!-- Top-Left -->
    <line x1="24" y1="24" x2="36" y2="24"/>
    <line x1="24" y1="24" x2="24" y2="36"/>
    <!-- Top-Right -->
    <line x1="{svg_w-24}" y1="24" x2="{svg_w-36}" y2="24"/>
    <line x1="{svg_w-24}" y1="24" x2="{svg_w-24}" y2="36"/>
    <!-- Bottom-Left -->
    <line x1="24" y1="{svg_h-24}" x2="36" y2="{svg_h-24}"/>
    <line x1="24" y1="{svg_h-24}" x2="24" y2="{svg_h-36}"/>
    <!-- Bottom-Right -->
    <line x1="{svg_w-24}" y1="{svg_h-24}" x2="{svg_w-36}" y2="{svg_h-24}"/>
    <line x1="{svg_w-24}" y1="{svg_h-24}" x2="{svg_w-24}" y2="{svg_h-36}"/>
  </g>

  <!-- Top Monospace Status Header -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-size="11" letter-spacing="2" fill="#71717A">
    <text x="56" y="50">[SYS.01 // NOMIK.ENGINE]</text>
    <text x="600" y="50" text-anchor="middle" fill="#A1A1AA">THE AI SKILL THAT NAMED ITSELF</text>
    <text x="1144" y="50" text-anchor="end">BY RAUL ALIYEV (@RALLYCODES)</text>
  </g>

  <!-- Top Hairline Divider -->
  <line x1="56" y1="68" x2="1144" y2="68" stroke="#1A1A1E" stroke-width="1"/>

  <!-- Technical Framing Reticle for Wordmark -->
  <g stroke="#27272A" stroke-width="1.2" fill="none">
    <!-- Top-Left Bracket -->
    <path d="M {ret_x1 + ret_arm} {ret_y1} L {ret_x1} {ret_y1} L {ret_x1} {ret_y1 + ret_arm}"/>
    <!-- Top-Right Bracket -->
    <path d="M {ret_x2 - ret_arm} {ret_y1} L {ret_x2} {ret_y1} L {ret_x2} {ret_y1 + ret_arm}"/>
    <!-- Bottom-Left Bracket -->
    <path d="M {ret_x1 + ret_arm} {ret_y2} L {ret_x1} {ret_y2} L {ret_x1} {ret_y2 - ret_arm}"/>
    <!-- Bottom-Right Bracket -->
    <path d="M {ret_x2 - ret_arm} {ret_y2} L {ret_x2} {ret_y2} L {ret_x2} {ret_y2 - ret_arm}"/>
  </g>

  <!-- Centered Pixelated NOMIK Typography -->
  <g id="pixel-wordmark">
{pixel_svg}
  </g>

  <!-- Terminal Subtitle Section -->
  <g transform="translate(600, 256)" text-anchor="middle">
    <text font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-weight="600" font-size="14.5" letter-spacing="3.5" fill="#F4F4F5">
      &gt; BILLION-DOLLAR BRAND NAMING &amp; DOMAIN ENGINE<tspan fill="#71717A">_</tspan>
    </text>
    <text y="28" font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-weight="400" font-size="12" letter-spacing="1.2" fill="#71717A">
      COGNITIVE SOUND-SYMBOLISM · ZERO AI SLOP · REAL-TIME ICANN VERIFICATION
    </text>
  </g>

  <!-- Bottom Hairline Divider -->
  <line x1="56" y1="322" x2="1144" y2="322" stroke="#1A1A1E" stroke-width="1"/>

  <!-- Bottom Terminal Status Bar -->
  <g transform="translate(56, 348)" font-family="-apple-system, BlinkMacSystemFont, 'SF Mono', 'Segoe UI Mono', monospace" font-size="10" letter-spacing="1.5" fill="#71717A">
    <text x="0" y="0"><tspan fill="#A1A1AA">[01]</tspan> 7 AGENCY TAXONOMIES</text>
    <text x="270" y="0"><tspan fill="#A1A1AA">[02]</tspan> ZERO AI SLOP CODE</text>
    <text x="540" y="0"><tspan fill="#A1A1AA">[03]</tspan> REAL-TIME ICANN RDAP</text>
    <text x="810" y="0"><tspan fill="#A1A1AA">[04]</tspan> TRADEMARK KNOCKOUT</text>
    <text x="1088" y="0" text-anchor="end" fill="#52525B">NPX NOMIK</text>
  </g>
</svg>'''
    return svg_content

if __name__ == '__main__':
    svg = generate_pixel_banner()
    paths = [
        'c:/Users/RAUL/Downloads/skills/nomik/assets/banner.svg',
        'c:/Users/RAUL/.agents/skills/nomik/assets/banner.svg'
    ]
    for p in paths:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"Generated pixel banner at: {p}")
