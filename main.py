import datetime
import threading

from bot import Subject, BotWorker


def enroll_subject(subject, enroll_time, worker):
    try:
        worker.login()
        # Wait until the specified datetime
        while False:
            # Sleep for a short time to avoid busy waiting
            threading.Event().wait(0.3)
            pass

        worker.refresh()
        worker.enroll(subject)
        print(f"Enrolled: {subject.name}")
        # wait for 2 minutes
        print("press enter to continue")
        input()
    except Exception as e:
        print(f"Enrollment failed for {subject.name}: {e}")
        raise e
    finally:
        del worker


# List of subjects to enroll
subjects = [
    Subject("คณิตศาสตร์เพิ่มเติม 10", "ค32234", "6"),
    Subject("พรีแคลคูลัส 2", "ค32209", "1"),
    Subject("ฟิสิกส์ 3", "ว30213", "5"),
    Subject("เคมี 4", "ว30234", "2"),
    Subject("เศรษฐศาสตร์น่ารู้", "ส30233", "1"),
    Subject("นวัตกรรมผู้ประกอบการ", "ส33254", "1"),
]

threads = []

# 16 may 2025 17:00
enroll_time = datetime.datetime(2025, 9, 4, 17, 0, 1)
#
# enroll_time = datetime.datetime(2025, 5, 16, 12, 5, 00)

for subject in subjects:
    worker = BotWorker()
    t = threading.Thread(target=enroll_subject, args=(subject, enroll_time, worker))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Press enter to exit")
input()
