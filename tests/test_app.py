# tests/test_app.py

import unittest
import os
from app import app

os.environ['TESTING'] = 'true'


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        "Open home and check it's content"
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Home</title>" in html
        assert '<img src="https://i.ibb.co/9wxwvLF/profile-square.jpg" alt="Home Page Portrait">' in html
        assert 'Production Engineer' in html
        assert '''I am an entry-level Systems Analyst or Production Engineer with a strong foundation in computer science and
            cloud computing. I graduated with a BS in Computer Science from UTSA, and I am able to work independently
            and aspart of a team. I am passionate about learning new technologies and solving complex problems.''' in html
        assert '<div href="" class="btn">Download Resume</div>' in html

    def test_about(self):
        "Open about and check it's content"
        response = self.client.get("/about")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>About</title>" in html
        assert "About <span>Me</span>" in html
        assert '''Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident explicabo cumque dignissimos odit? Rem
            vitae
            inventore saepe doloremque? Dicta laboriosam quod in impedit deserunt voluptate. Excepturi temporibus
            cupiditate
            accusamus iusto quae nihil laboriosam quasi, nobis debitis voluptatem hic? Nulla eligendi et, nam earum
            excepturi tempora? Enim.''' in html
        assert '<img src="https://i.ibb.co/ccT9tVM/bros.jpg" alt="Photo with brothers">' in html
        assert "Where I've <span>been</span>" in html
        assert "<script src=\"https://cdn.maptiler.com/maplibre-gl-js/v2.4.0/maplibre-gl.js\"></script>" in html
        assert "js/map_script.js" in html

    def test_education(self):
        "Open education and check it's content"
        response = self.client.get("/education")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Education</title>" in html
        assert "<div class=\"year\"><i class='bx bxs-calendar'></i> 2018 - 2023</div>" in html
        assert "Production Engineering Fellow - MLH Fellowship" in html
        assert "<div class=\"year\"><i class='bx bxs-calendar'></i> May 2021 - May 2022</div>" in html
        assert "Smithson Valley High School" in html

    def test_projects(self):
        "Open projects and check it's content"
        response = self.client.get("/projects")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Projects</title>" in html
        assert "My Past Work Experience" in html
        assert '''Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolores illum omnis, perspiciatis nisi
                accusantium
                libero ut! Vitae voluptates deleniti, dignissimos repellendus, alias pariatur eos dolorum vero expedita
                illum eum quod?''' in html
        assert 'Project 1' in html
        assert 'Project 2' in html

    def test_hobbies(self):
        "Open hobbies and check it's content"
        response = self.client.get("/hobbies")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Hobbies</title>" in html
        assert 'Learning Instruments' in html
        assert 'Attending Hackathons' in html
        assert 'Mechanical Keyboards' in html

    def test_timeline_route(self):
        "Open timeline, check it's content, post, and check again"
        # test GET
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert '<form id="timelineForm" method="POST" action="/timeline">' in html
        assert '<button type="submit" class="btn btn-primary mb-3">Post</button>' in html
        assert "document.getElementById('timelineForm').addEventListener('submit', function (event)" in html

        # test POST for two users and use GET to test the results
        response = self.client.post("/timeline",
                                    data={"name": "John", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 201
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert '<form id="timelineForm" method="POST" action="/timeline">' in html
        assert '<button type="submit" class="btn btn-primary mb-3">Post</button>' in html
        assert "John" in html
        assert "Hello world, I'm John!"
        assert "document.getElementById('timelineForm').addEventListener('submit', function (event)" in html

        response = self.client.post("/timeline",
                                    data={"name": "Jane", "email": "jane@example.com",
                                          "content": "Hello world, I'm Jane!"})
        assert response.status_code == 201
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert '<form id="timelineForm" method="POST" action="/timeline">' in html
        assert '<button type="submit" class="btn btn-primary mb-3">Post</button>' in html
        assert "Jane" in html
        assert "Hello world, I'm Jane!"
        assert "John" in html
        assert "Hello world, I'm John!"
        assert "document.getElementById('timelineForm').addEventListener('submit', function (event)" in html

    def test_malformed_timeline_post(self):
        "Test timeline POST requests with malformed data"
        # POST request missing name
        response = self.client.post("/timeline",
                                    data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing content
        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing email
        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request with malformed email
        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "not-an-email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "email.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "name@email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe", "email": "name@email.c",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        # POST request with malformed name
        response = self.client.post("/timeline",
                                    data={"name": "J0hn Doe", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe!", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe;", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe123", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe{}", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/timeline",
                                    data={"name": "John Doe@", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

    def test_incorrect_route(self):
        "Open a route that doesn't exist and check the return"
        response = self.client.get("/non_existent_route")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)


class AppApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_timeline_api(self):
        "Test all the timeline api endpoints"
        # test GET
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # test POST for two users and use GET to test the results
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 201
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm John!"
        assert json["timeline_posts"][0]["id"] == 1

        response = self.client.post("/api/timeline_post",
                                    data={"name": "Jane", "email": "jane@example.com",
                                          "content": "Hello world, I'm Jane!"})
        assert response.status_code == 201
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2
        assert json["timeline_posts"][0]["name"] == "Jane"
        assert json["timeline_posts"][0]["email"] == "jane@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm Jane!"
        assert json["timeline_posts"][0]["id"] == 2
        assert json["timeline_posts"][1]["name"] == "John"
        assert json["timeline_posts"][1]["email"] == "john@example.com"
        assert json["timeline_posts"][1]["content"] == "Hello world, I'm John!"
        assert json["timeline_posts"][1]["id"] == 1

        # test DELETE for both posts and use GET to test the results
        response = self.client.delete(f"/api/timeline_post/2")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "message" in json
        assert json["message"] == "Timeline post deleted successfully"

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm John!"
        assert json["timeline_posts"][0]["id"] == 1

        response = self.client.delete(f"/api/timeline_post/1")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "message" in json
        assert json["message"] == "Timeline post deleted successfully"

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None and "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_malformed_timeline_api_post(self):
        "Test timeline api POST requests with malformed data"
        # POST request missing name
        response = self.client.post("/api/timeline_post",
                                    data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing content
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing email
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request with malformed email
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "not-an-email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "email.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "name@email",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "name@email.c",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        # POST request with malformed name
        response = self.client.post("/api/timeline_post",
                                    data={"name": "J0hn Doe", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe!", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe;", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe123", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe{}", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe@", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]


if __name__ == '__main__':
    unittest.main()
