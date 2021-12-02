import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import md5
from random import choice

def generate_coin():
    while True:
        number = "".join([choice("0123456789") for i in range(50)])
        number_hash = md5(number.encode("utf-8")).hexdigest()

        if number_hash.endswith("0" * 5):
            return number_hash



def start_generator(workers_count, target):
    with ProcessPoolExecutor(max_workers=workers_count) as executor:
        tasks_count = workers_count if workers_count > target else target
        tasks = {executor.submit(generate_coin) for i in range(tasks_count)}

        count = 0
        start_time = time.time()
        for task in as_completed(tasks):
            print(task.result())
            count += 1
            if count >= target:
                end_time = time.time()
                print("--- %s seconds ---" % round(end_time - start_time, 2))
                break

        executor.shutdown(wait=False)

if __name__ == '__main__':
    start_generator(20, 2)