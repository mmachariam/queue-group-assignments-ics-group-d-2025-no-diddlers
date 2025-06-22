class PrintQueueManager:
    def __init__(self, capacity=10, expiry_time=30):
        self.capacity = capacity
        self.expiry_time = expiry_time
        self.queue = []
        self.current_time = 0
        self.expired_jobs_log = []

    def remove_expired_jobs(self):
        expired_jobs = []
        remaining_jobs = []

        for job in self.queue:
            waiting_time = self.current_time - job['Time-in']

            if waiting_time >= self.expiry_time:
                #expired
                expired_jobs.append(job)
                self._notify_job_expiry(job)
            else:
                #valid
                remaining_jobs.append(job)

        #Update queue with non-expired
        self.queue = remaining_jobs

        self.expired_jobs_log.extend(expired_jobs)

        return expired_jobs

    def _notify_job_expiry(self, job):
        print(f"JOB EXPIRED: User {job['user_id']}, Job{job['job_id']}"
              f"(waited {self.current_time - job['Time-in']} ticks)")

    def update_waiting_times(self):
        for job in self.queue:
            job['waiting_time'] = self.current_time - job['Time-in']

    def get_jobs_near_expiry(self, warning_threshold=5):
        near_expiry = []
        for job in self.queue:
            waiting_time = self.current_time - job['Time-in']
            time_until_expiry = self.expiry_time - waiting_time
            if 0 < time_until_expiry <= warning_threshold:
                near_expiry.append(job)
        return near_expiry

    def show_status(self):

        print(f"\n Queue status (Time: {self.current_time})")
        print(f"Queue size: {len(self.queue)}/{self.capacity}")
        print(f"Expiry time: {self.expiry_time} ticks")

        if not self.queue:
            print("Queue is empty")
            return

        print("\nCurrent jobs:")

        for i, job in enumerate(self.queue):
            time_left = self.expiry_time - job['waiting_time']
            status = "EXPIRING SOON" if time_left <= 3 else "OK"
            print(f"{i + 1}. User {job['user_id']}, Job {job['job_id']} "
                  f"(Priority: {job['priority']}, Waiting: {job['waiting_time']}t, "
                  f"Expires in: {time_left}t) {status}")

        # Show jobs near expiry
        near_expiry = self.get_jobs_near_expiry()
        if near_expiry:
            print(f"\n  {len(near_expiry)} job(s) expiring soon!")



