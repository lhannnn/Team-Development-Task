#to do list '超级困难组'


del list_tasks():
    """用于查看当有哪些任务"""
    try：
        with open("todo.txt", "r") as f:
            lines = f.readlines()
        if not lines:
            print("empty")
            return
        for i, line in enumerate(lines,1):
            print(f"{i}. {line.strip()}")
    except FileNotFoundError:
        print("(no tasks yet)")



#用户端



#后台数据处理端
#数据存储端
#数据输入输出端