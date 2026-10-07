#!/usr/bin/env python3
"""Generate simple PNG icons (no dependencies): green checkmark on dark rounded-free square.
Full-bleed background so iOS/maskable cropping looks fine. Usage: python3 tools/make_icons.py"""
import struct, zlib, os

BG = (15, 23, 42); FG = (34, 197, 94); WHITE = (241, 245, 249)

def dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return ((px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2) ** 0.5

def render(size):
    s = size
    cx, cy, r = s / 2, s / 2, s * 0.30          # circle (safe zone for maskable)
    w = s * 0.045                                 # check half-thickness
    a, b, c = (s*.38, s*.52), (s*.47, s*.61), (s*.63, s*.42)
    rows = []
    for y in range(s):
        row = bytearray([0])
        for x in range(s):
            # 3x3 supersampling for antialiasing
            acc = [0, 0, 0]
            for sy in range(3):
                for sx in range(3):
                    px, py = x + (sx + .5) / 3, y + (sy + .5) / 3
                    col = BG
                    if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                        col = FG
                        if min(dist_seg(px, py, *a, *b), dist_seg(px, py, *b, *c)) <= w:
                            col = WHITE
                    for i in range(3): acc[i] += col[i]
            row += bytes(v // 9 for v in acc)
        rows.append(bytes(row))
    return b''.join(rows)

def png(size):
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(render(size), 9)) + chunk(b'IEND', b''))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icons')
for name, size in (('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)):
    with open(os.path.join(out, name), 'wb') as f: f.write(png(size))
    print('wrote', name, size)
