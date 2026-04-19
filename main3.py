import warnings
warnings.filterwarnings('ignore')

from PIL import Image, ImageDraw  # noqa
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt  # noqa


WIDTH, HEIGHT = 600, 600
COLORS = ('black', 'red', 'green', 'blue', 'violet', 'orange', 'cyan', 'magenta', 'yellow', 'brown')
CLUSTER_MIN_COUNT = 1
CLUSTER_MAX_COUNT = len(COLORS)
ITERATION_COUNT = 1000


def generate_linearly_inseparable_data() -> list[list[int]]:
    pts = []
    
    # Кластер 1: Внутренний круг (плотный)
    n_inner = 150
    for _ in range(n_inner):
        radius = np.random.uniform(0, 70)
        angle = np.random.uniform(0, 2 * np.pi)
        x = WIDTH // 2 + radius * np.cos(angle)
        y = HEIGHT // 2 + radius * np.sin(angle)
        pts.append([int(x), int(y), -1])

    # Кластер 2: Внешнее кольцо (вокруг первого)
    n_outer = 300
    for _ in range(n_outer):
        radius = np.random.uniform(140, 200) # Радиус больше, чем у первого
        angle = np.random.uniform(0, 2 * np.pi)
        x = WIDTH // 2 + radius * np.cos(angle)
        y = HEIGHT // 2 + radius * np.sin(angle)
        pts.append([int(x), int(y), -1])

    return pts


def calculate_inertia(
        points: list[list[int]],
        centers: list[list[int]]
) -> int:
    sse = 0
    for point in points:
        sse += min(
            (point[0] - centers[i][0]) ** 2 + (point[1] - centers[i][1]) ** 2
            for i in range(len(centers))
        )
    return sse


def find_distance(
        p1: list[int],
        p2: list[int]
) -> float:
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def draw_point(
        draw: ImageDraw,
        x: int,
        y: int,
        ind: int,
        r: int = 3
):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=COLORS[ind + 1])


def draw_center(
        draw: ImageDraw,
        x: int,
        y: int,
        ind: int,
        r: int = 3):
    draw.rectangle((x - r, y - r, x + r, y + r), fill=COLORS[ind + 1], outline="black")


def find_nearest_center(
        point: list[int],
        centers: list[list[int]]
) -> int:
    min_dist = float('inf')
    best_ind = 0
    for ind in range(len(centers)):
        center = centers[ind]
        distance = find_distance(center, point)
        if distance < min_dist:
            min_dist = distance
            best_ind = ind
    return best_ind


def assign_points(
        points: list[list[int]],
        centers: list[list[int]]):
    for i in range(len(points)):
        points[i][2] = find_nearest_center(points[i], centers)


def find_center_of_mass(
        ind: int,
        points: list[list[int]]
) -> np.ndarray:
    res = np.array([.0, .0])
    cnt = 0
    for i in range(len(points)):
        point = points[i]
        if point[2] == ind:
            res[0] += point[0]
            res[1] += point[1]
            cnt += 1
    if cnt == 0:
        return res
    return res / cnt


def shift_centers(centers: list[list[int]], points: list[list[int]]):
    for ind in range(len(centers)):
        center_ = find_center_of_mass(ind, points)
        centers[ind] = [*center_, ind]


def draw_all(
        draw: ImageDraw,
        points: list[list[int]],
        centers: list[list[int]]
):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="white")
    for i in range(len(points)):
        point = points[i]
        draw_point(draw, *point)
    for i in range(len(centers)):
        center = centers[i]
        draw_center(draw, *center)


def find_elbow(inertias: list[float]):
    k_vals_norm = (np.arange(CLUSTER_MIN_COUNT, CLUSTER_MAX_COUNT)
                   / (CLUSTER_MAX_COUNT - CLUSTER_MIN_COUNT))
    inertias_norm = np.array(inertias) / inertias[0]
    p0 = np.array([k_vals_norm[0], inertias_norm[0]])
    p1 = np.array([k_vals_norm[-1], inertias_norm[-1]])

    distances = []
    for i in range(len(k_vals_norm)):
        p = np.array([k_vals_norm[i], inertias_norm[i]])
        d = np.abs(np.cross(p1 - p0, p - p0)) / np.linalg.norm(p1 - p0)
        distances.append(d)

    elbow_idx = np.argmax(distances)
    optimal_k = k_vals_norm[elbow_idx] * (CLUSTER_MAX_COUNT - CLUSTER_MIN_COUNT)
    print(f"Оптимальное кол-во кластеров: {optimal_k}")


# np.random.seed(2123123123)

pts = generate_linearly_inseparable_data()
pts_count = len(pts)
print(f"Сгенерировано точек: {pts_count}")

inertias = []

for center_count in range(CLUSTER_MIN_COUNT, CLUSTER_MAX_COUNT):
    center_x = np.random.randint(low=10, high=WIDTH - 10, size=center_count)
    center_y = np.random.randint(low=10, high=HEIGHT - 10, size=center_count)
    centers = [[center_x[i], center_y[i], i] for i in range(center_count)]

    im = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    sse = 0
    for i in range(ITERATION_COUNT):
        if i > 0: shift_centers(centers, pts)
        assign_points(pts, centers)
        if i == ITERATION_COUNT - 1:
            draw_all(draw, pts, centers)
            sse = calculate_inertia(pts, centers)
            draw.text((10, 10), f"{sse=}", fill="black")
            im.save(f"dop_task_1/img_dop{center_count, i}.jpg", quality=95)

    inertias.append(sse)

find_elbow(inertias)
plt.plot(inertias)
plt.show()
