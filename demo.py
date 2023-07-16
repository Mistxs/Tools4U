from apscheduler.schedulers.blocking import BlockingScheduler

i = 0
def shedulertest():
    print("test")
    global i
    i += 1
    if i == 5:
        print(i/0)


def start():
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(shedulertest, 'interval', seconds=2)
        scheduler.start()
    except Exception as e:
        print(f"Ошибка sheduler : {e}")


start()