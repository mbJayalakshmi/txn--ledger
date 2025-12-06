import threading
from app import crud

def transfer_thread():
    try:
        crud.transfer_funds(1, 2, 10)
    except Exception as e:
        print(e)

threads = [threading.Thread(target=transfer_thread) for _ in range(10)]
[t.start() for t in threads]
[t.join() for t in threads]

print(crud.get_account(1))
print(crud.get_account(2))
