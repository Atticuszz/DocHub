#include <stdio.h>
#include <string.h>
#define MAX_LEN 100
#define INFINITE 1000

typedef struct graph
{
int nodenum; // 顶点数
int edgenum; // 边数
int matrix[MAX_LEN][MAX_LEN]; // 存储图的邻接矩阵
}Graph;

typedef struct stack // 定义堆栈结构体类型
{
int top;
int printout[MAX_LEN];
}Stack;

void InitStack(Stack *s) // 初始化堆栈
{
s->top = -1; // 栈为空时栈顶指针top=-1
memset(s->printout,0,sizeof(int)*MAX_LEN); // 对内存块进行置零
}

void push(Stack \*s,int m) // 入栈
{
s->printout[++(s->top)] = m;
}

int pop(Stack \*s) // 出栈
{
return s->printout[s->top--];
}

int in[MAX_LEN]; // 若in[i] = 1,则说明顶点vi已在集合S中
int dist[MAX_LEN]; // dist[i]是"顶点vs"到"顶点i"的最短路径的长度
int prev[MAX_LEN]; // prev[i]的值是"顶点vs"到"顶点i"的最短路径所经历的全部顶点中,位于"顶点i"之前的那个顶点

void InitGraph(Graph \*g,int n)
{
int i, j;
for(i = 1; i <= n; i++) // 初始化邻接矩阵
{
for(j = 1; j <= n;j++)
{
if(i == j) g->matrix[i][j] = 0;
else g->matrix[i][j] = INFINITE;
}
}

    for(i=1;i<=n;i++)
    {
         in[i] = 0;
         dist[i] = INFINITE;
         prev[i] = 0;
    }

}

int main()
{
int n,m,i,I,J,weight,count,min,k,temp;

    while(scanf("%d %d",&n,&m)) // 输入顶点数和边数
    {
        Graph mGraph;
        mGraph.edgenum = m;
        mGraph.nodenum = n;
        InitGraph(&mGraph, n);

        for(i = 0; i < m; i++)
        {
            scanf("%d %d %d", &I, &J, &weight);
            mGraph.matrix[I][J] = weight;  // 根据输入填充邻接矩阵
            mGraph.matrix[J][I] = weight;
        }

        in[1] = 1;    // 初始时只包含源顶点1，即S＝{1}
        prev[1] = 1;
        dist[1] = 0;  // 1到1的距离为0

        for(i = 2; i <= n; i++)
        {
            dist[i] = mGraph.matrix[1][i]; // 其它各点到顶点vs的距离
            if(dist[i] != INFINITE) prev[i] = 1;
        }

        count = 0;
        while(count < n-1)  // 遍历n-1次
        {
            min = INFINITE;
            for(i = 1; i <= n; i++)
            {
                if(in[i] == 0 && dist[i] < min) // 查找最近点(从U中选取一个距离vs最小的顶点k)
                {
                    min = dist[i];
                    k = i;
                }
            }
            in[k] = 1;     // 标记查找到的最近点,加入S中

            for(i = 1; i <= n; i++)  // update the distance
            {
                if( in[i]==0 && (min + mGraph.matrix[k][i])<dist[i] ) // 判断是vs直接连v[i]短,还是经过v[k]连接v[i]更短
                {
                    dist[i] = min + mGraph.matrix[k][i];   // 更新dist
                    prev[i] = k;      // 记录前驱顶点
                }
            }

            count++;
        }


        Stack s;
        for(i = 1; i <= n; i++)
        {
            temp = i;
            InitStack(&s);
            if(prev[temp] == 0)
            {
                printf("no path\n");
                continue;
            }
            while(prev[temp] != 1)
            {
                push(&s, prev[temp]);
                temp = prev[temp];
            }
            printf("1-->");
            while(s.top != -1) // 判断栈是否为空
            {
                printf("%d-->", pop(&s)); // 输出最短路径
            }
            printf("%d  min length is %d\n", i, dist[i]);

        }

    }
    getchar();
    return 0;

}
