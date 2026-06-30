from PIL import Image, ImageDraw
SCREEN_W = 960
SCREEN_H = 640
VIRTUAL_W = 5000
VIRTUAL_H = 5000
ROUTE_SHIFT_X = 100

def to_screen(pt):
    return (
        max(0, int((pt[0] - ROUTE_SHIFT_X) * SCREEN_W / VIRTUAL_W)),
        int(pt[1] * SCREEN_H / VIRTUAL_H),
    )

ROUTE_START = (0, 3101)               # 怪物出生点，起始位置
ROUTE_FORK1 = (1250, 3101)            # 第一个分岔点入口，怪物先到达这里
ROUTE_FORK1_UP = (1250, 1900)         # 第一个分岔点向上分支
ROUTE_FORK1_RIGHT = (1723, 3101)      # 第一个分岔点向右分支
ROUTE_FIRST_MERGE = (1723, 1900)      # 第一个分岔后汇合点
ROUTE_AFTER_MERGE_RIGHT = (2400, 1900) # 第一个汇合之后的向右移动节点
ROUTE_AFTER_MERGE_DOWN = (2400, 3050) # 向右后向下的转折点
ROUTE_FORK2 = (3100, 3050)            # 第二个分岔点入口
ROUTE_FORK2_UP = (3100, 1000)         # 第二个分岔点向上分支起点
ROUTE_FORK2_RIGHT = (3850, 3050)      # 第二个分岔点向右分支起点
ROUTE_SECOND_MERGE = (3850, 1000)     # 第二个分岔后汇合点
ROUTE_END = (4522, 1000)              # 终点，怪物到达则失败
route_options = [
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_UP,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_UP,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_RIGHT,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_UP,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_UP,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_RIGHT,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_RIGHT,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_RIGHT,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
]

im = Image.open('icon/background.jpg')
d = ImageDraw.Draw(im)
for route in route_options:
    pts = [to_screen(pt) for pt in route]
    d.line(pts, fill=(255, 0, 0), width=6)
    for p in pts:
        d.ellipse((p[0]-8, p[1]-8, p[0]+8, p[1]+8), fill=(0, 255, 0))
im.save('route_overlay.png')
print('saved route_overlay.png')
print([ [to_screen(pt) for pt in route] for route in route_options])