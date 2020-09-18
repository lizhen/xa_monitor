import pylas
from datetime import datetime

building = {'x': 494105.112, 'y': 4326351.499, 'z': 14.4}
radius = 1

with pylas.open('d:/workspace/xad1_cloud.las') as fh:
    print('Date from Header:', fh.header.date)
    print('Software from Header:', fh.header.generating_software)
    print('Points from Header:', fh.header.point_count)

    x_scale, x_offset = fh.header.x_scale, fh.header.x_offset
    y_scale, y_offset = fh.header.y_scale, fh.header.y_offset
    z_scale, z_offset = fh.header.z_scale, fh.header.z_offset

    las = fh.read()

    print('S1:', datetime.now())
    for point in las.points:
        z = round(point[2] * z_scale + z_offset)

        if z < 10:
            continue

        x = round(point[0] * x_scale + x_offset)
        y = round(point[1] * y_scale + y_offset)

        min_x = round(building['x'] - radius)
        max_x = round(building['x'] + radius)
        min_y = round(building['y'] - radius)
        max_y = round(building['y'] + radius)

        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue
        print('x:', x, 'y:', y, 'z:', round(z))

    print('S2:', datetime.now())