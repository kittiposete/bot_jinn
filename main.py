import threading
import datetime

from bot import Subject, BotWorker


def enroll_subject(subject, enroll_time):
    try:
        worker = BotWorker()
        # Wait until the specified datetime
        while enroll_time > datetime.datetime.now():
            # Sleep for a short time to avoid busy waiting
            threading.Event().wait(0.1)
            pass

        worker.refresh()

        worker.enroll(subject)
        print(f"Enrolled: {subject.name}")
    except Exception as e:
        print(f"Enrollment failed for {subject.name}: {e}")
    finally:
        del worker


# List of subjects to enroll
subjects = [
    Subject("เคมี 3", "ว30233", "4"),
    Subject("ฟิสิกส์ 2", "ว30212", "4"),
    Subject("นวัตกรรมเพื่อสังคมอนาคต", "ส32251", "1"),
]

threads = []

# 16 may 2025 17:00
# enroll_time = datetime.datetime(2025, 5, 16, 17, 0, 1)

enroll_time = datetime.datetime(2025, 5, 16, 0, 36, 50)

for subject in subjects:
    t = threading.Thread(target=enroll_subject, args=(subject, enroll_time))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Press enter to exit")
input()
