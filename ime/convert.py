"""
Convert 梅兰竹菊 PNG images to monochrome C byte arrays for e-ink display.
Resizes to 400x300, applies Floyd-Steinberg dithering for B&W conversion.
"""
from PIL import Image
import os

SRC_DIR = r'd:\py\墨水屏项目\EPD-nRF5\ime'
OUT_H = r'd:\py\墨水屏项目\EPD-nRF5\GUI\decor_bitmaps.h'
OUT_C = r'd:\py\墨水屏项目\EPD-nRF5\GUI\decor_bitmaps.c'

FILES = [
    ('梅.png',   'mei'),
    ('兰花.png', 'lan'),
    ('竹.png',   'zhu'),
    ('菊.png',   'ju'),
]

TARGET_W = 200
TARGET_H = 150

def image_to_mono_bitmap(img_path, target_w, target_h):
    """Convert image to monochrome bitmap with Floyd-Steinberg dithering."""
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        # Composite on white background
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to fit target, maintain aspect ratio, center on canvas
    img_w, img_h = img.size
    scale = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Create blank canvas and paste centered
    canvas = Image.new('L', (target_w, target_h), 255)
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    canvas.paste(img.convert('L'), (offset_x, offset_y))
    
    # Get pixel array
    pixels = list(canvas.getdata())
    
    # Floyd-Steinberg dithering
    for y in range(target_h):
        for x in range(target_w):
            idx = y * target_w + x
            old = pixels[idx]
            new = 0 if old < 128 else 255
            pixels[idx] = new
            err = old - new
            if x + 1 < target_w:       pixels[idx + 1] = min(255, max(0, pixels[idx + 1] + err * 7 // 16))
            if y + 1 < target_h:
                if x > 0:              pixels[idx + target_w - 1] = min(255, max(0, pixels[idx + target_w - 1] + err * 3 // 16))
                pixels[idx + target_w] = min(255, max(0, pixels[idx + target_w] + err * 5 // 16))
                if x + 1 < target_w:   pixels[idx + target_w + 1] = min(255, max(0, pixels[idx + target_w + 1] + err * 1 // 16))
    
    # Convert to 1-bit bitmap (MSB first per byte)
    w_bytes = (target_w + 7) // 8
    bitmap = bytearray(w_bytes * target_h)
    for y in range(target_h):
        for x in range(target_w):
            if pixels[y * target_w + x] < 128:
                bitmap[y * w_bytes + x // 8] |= (0x80 >> (x % 8))
    
    return bitmap, target_w, target_h, w_bytes

def bitmap_to_c_array(name, bitmap, w, h, w_bytes):
    """Generate C array string."""
    lines = []
    lines.append(f'// {name} ({w}x{h}), {len(bitmap)} bytes')
    lines.append(f'static const uint8_t bmp_{name}[] = {{')
    for i in range(0, len(bitmap), 12):
        chunk = bitmap[i:i+12]
        hex_str = ', '.join(f'0x{b:02X}' for b in chunk)
        if i + 12 < len(bitmap):
            hex_str += ','
        lines.append(f'    {hex_str}')
    lines.append('};')
    return '\n'.join(lines)

def main():
    all_c_code = []
    all_h_code = []
    
    all_h_code.append('#ifndef __DECOR_BITMAPS_H')
    all_h_code.append('#define __DECOR_BITMAPS_H')
    all_h_code.append('#include <stdint.h>')
    all_h_code.append('')
    all_h_code.append(f'#define DECOR_BMP_W {TARGET_W}')
    all_h_code.append(f'#define DECOR_BMP_H {TARGET_H}')
    all_h_code.append('')
    
    all_c_code.append('#include "decor_bitmaps.h"')
    all_c_code.append('')
    
    for fn, name in FILES:
        path = os.path.join(SRC_DIR, fn)
        bitmap, w, h, w_bytes = image_to_mono_bitmap(path, TARGET_W, TARGET_H)
        c_arr = bitmap_to_c_array(name, bitmap, w, h, w_bytes)
        all_c_code.append(c_arr)
        all_c_code.append('')
        
        # Header declarations
        all_h_code.append(f'extern const uint8_t bmp_{name}[];')
        
        # Also save as PNG for simulator use
        # Reconstruct B&W image and save
        img = Image.new('1', (w, h))
        img_data = img.load()
        for y in range(h):
            for x in range(w):
                byte_idx = y * w_bytes + x // 8
                bit = (bitmap[byte_idx] >> (7 - (x % 8))) & 1
                img_data[x, y] = 1 - bit  # Invert: 1=white, 0=black in PIL mode '1'
        out_png = os.path.join(SRC_DIR, f'{name}_bw.png')
        img.save(out_png)
        print(f'Saved {out_png}')
    
    all_h_code.append('')
    all_h_code.append('#endif // __DECOR_BITMAPS_H')
    
    with open(OUT_H, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_h_code) + '\n')
    print(f'Written {OUT_H}')
    
    with open(OUT_C, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_c_code) + '\n')
    print(f'Written {OUT_C}')

if __name__ == '__main__':
    main()