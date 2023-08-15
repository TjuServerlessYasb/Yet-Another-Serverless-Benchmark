import asyncio
import time

async def func1(num):
    print('--func1 start--')
    await asyncio.sleep(num)
    print('--func1 done--')
    return 'func1 ok'

async def func2(num):
    print('--func2 start--')
    await asyncio.sleep(num)
    print('--func2 done--')
    return 'func2 ok'


async def main():
    task1 = asyncio.ensure_future(func1(3))
    task2 = asyncio.ensure_future(func2(5))
    tasks = [task1, task2]
    res = await asyncio.gather(*tasks)
    return res
    # done, pending = await asyncio.wait(tasks)
    # for t in done:
    #     print(t.result())
    # print(done)
    # print(pending)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    print(result)
