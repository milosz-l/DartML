from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    """
    Perform simple load test by just visiting pages
    without interacting with any buttons or uploading any files.
    """

    wait_time = between(1, 5)

    @task
    def home_page(self):
        self.client.get(url="")
    
    @task
    def sample_page(self):
        self.client.get(url="/Sample")
    
    @task
    def explore_page(self):
        self.client.get(url="/Explore")
    
    @task
    def modify_and_model_page(self):
        self.client.get(url="/Modify_&_Model")
    
    @task
    def assess_page(self):
        self.client.get(url="/Assess")