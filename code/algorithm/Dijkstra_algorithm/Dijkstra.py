# 编辑人员：张彬
# 开发时间：2024/2/4 9:32

MAX_LEN = 100
INFINITE = 1000


class Graph:
    def __init__(self, n):
        self.nodenum = n
        self.matrix = [[INFINITE for _ in range(n)] for _ in range(n)]
        for i in range(n):
            self.matrix[i][i] = 0


def init_graph(n):
    return Graph(n)


def dijkstra(graph, start=0):
    n = graph.nodenum
    in_set = [False] * n
    dist = [INFINITE] * n
    prev = [None] * n

    dist[start] = 0
    prev[start] = start
    in_set[start] = True

    for i in range(1, n):
        dist[i] = graph.matrix[start][i]
        if dist[i] < INFINITE:
            prev[i] = start

    for _ in range(n - 1):
        min_dist = INFINITE
        k = -1
        for i in range(n):
            if not in_set[i] and dist[i] < min_dist:
                min_dist = dist[i]
                k = i
        in_set[k] = True

        for i in range(n):
            if not in_set[i] and (min_dist + graph.matrix[k][i]) < dist[i]:
                dist[i] = min_dist + graph.matrix[k][i]
                prev[i] = k

    return dist, prev


def print_path(prev, start, end):
    path = []
    while end is not None and end != start:
        path.append(end)
        end = prev[end]
    path.append(start)
    path.reverse()

    return path


if __name__ == "__main__":
    print("Please input the information of graph!\nthe vertex & edge number of the graph.以“ ”分隔。")
    n, m = map(int, input().split())
    graph = init_graph(n)

    print("请依次输入每条边的两个顶点和权值，每个值之间用空格分隔：")
    for _ in range(m):
        i, j, weight = map(int, input().split())
        graph.matrix[i - 1][j - 1] = weight
        graph.matrix[j - 1][i - 1] = weight

    print("请输入起始顶点和结束顶点，用空格分隔（顶点编号从1开始）：")
    start, end = map(int, input().split())
    start -= 1  # 调整索引，因为Python中列表索引从0开始
    end -= 1

    dist, prev = dijkstra(graph, start)

    if prev[end] is not None:
        path = print_path(prev, start, end)
        print(f"{start + 1} --> {' --> '.join(map(lambda x: str(x + 1), path))}  min length is {dist[end]}")
    else:
        print(f"从{start + 1}到{end + 1}没有路径。")
