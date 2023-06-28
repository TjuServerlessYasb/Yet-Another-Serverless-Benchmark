import threading


def saySorry(ls):
    print("1321？")
    print(ls)
    return "niho43w2"

class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


if __name__ == '__main__':
    threads= []
    for url in range(5):
        # t = threading.Thread(target=saySorry)
        t = threading.Thread(target=saySorry,args=("nini",))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    for t in threads:
        print(t.)