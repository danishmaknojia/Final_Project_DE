from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def index(self):
        self.client.get("/")
        print("Visited index page")

    @task
    def final_four(self):
        self.client.get("/final_four")
        print("Visited final four page")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
