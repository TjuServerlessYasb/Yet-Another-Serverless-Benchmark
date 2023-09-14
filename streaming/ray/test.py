import threading
import time

total = 0


def increment_n_times(n):
    global total
    for i in range(n):
        total += 1


def increment_in_x_threads(x, func, n):
    threads = [threading.Thread(target=func, args=(n,)) for i in range(x)]
    global total
    total = 0
    begin = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(
        'finished in {}s.\ntotal: {}\nexpected: {}\ndifference: {} ({} %)'.format(
            time.time() - begin, total, n * x, n * x - total, 100 - total / n / x * 100
        )
    )


increment_in_x_threads(70, increment_n_times, 5_000_000)
