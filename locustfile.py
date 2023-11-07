from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def view_main_page(self):
        self.client.get("/courses")

    @task
    def view_course_page(self):
        self.client.get("/courses/btcusdt")
        self.client.get("/courses/btcrub")
        self.client.get("/courses/ercrub")
        self.client.get("/courses/ercusdt")
        self.client.get("/courses/ethrub")
        self.client.get("/courses/ethusdt")
        self.client.get("/courses/trcrub")
        self.client.get("/courses/trcusdt")
