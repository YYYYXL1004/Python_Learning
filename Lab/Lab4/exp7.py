import time

class TimeoutQueue:
    def __init__(self, maxsize):
        self.queue = []
        self.maxsize = maxsize

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) >= self.maxsize

    def resize(self, new_size):
        self.maxsize = new_size

    def put(self, item, timeout=0):
        start_time = time.time()
        while self.is_full():
            if time.time() - start_time >= timeout:
                raise TimeoutError("入队超时：队列已满")
            time.sleep(0.1)  # 避免死循环跑满CPU
        self.queue.append(item)

    def get(self, timeout=0):
        start_time = time.time()
        while self.is_empty():
            if time.time() - start_time >= timeout:
                raise TimeoutError("出队超时：队列为空")
            time.sleep(0.1)
        return self.queue.pop(0)

if __name__ == "__main__":
    q = TimeoutQueue(2)
    
    try:
        print("--- 测试正常入队 ---")
        q.put("A")
        q.put("B")
        print(f"队列状态: {q.queue}, 是否满: {q.is_full()}")
        
        print("\n--- 测试入队超时 ---")
        print("尝试放入 C，等待 1.5 秒...")
        q.put("C", timeout=1.5)
    except TimeoutError as e:
        print(f"异常捕获: {e}")

    try:
        print("\n--- 测试修改队列大小 ---")
        q.resize(5)
        print(f"修改后是否满: {q.is_full()}")
        q.put("C")
        print(f"队列状态: {q.queue}")
        
        print("\n--- 测试正常出队 ---")
        print(f"出队元素: {q.get()}")
        print(f"出队元素: {q.get()}")
        print(f"出队元素: {q.get()}")
        print(f"队列状态: {q.queue}, 是否空: {q.is_empty()}")
        
        print("\n--- 测试出队超时 ---")
        print("尝试从空队列取元素，等待 1.5 秒...")
        q.get(timeout=1.5)
    except TimeoutError as e:
        print(f"异常捕获: {e}")