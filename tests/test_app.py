# tests/test_app.py

import unittest
import os
from app import app
import base64

os.environ['TESTING'] = 'true'


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        "Open home and check it's content"
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>NR | Home</title>" in html
        assert '<img src="https://i.ibb.co/9wxwvLF/profile-square.jpg" alt="Home Page Portrait">' in html
        assert 'Production Engineer' in html
        assert '''I am an entry-level <span><b>Systems Analyst</b></span> or <span><b>Production Engineer</b></span> with a strong foundation in computer science and
            cloud computing. I graduated with a BS in Computer Science from UTSA, and I am able to work independently
            and as part of a team. I am passionate about learning new technologies and solving complex problems.''' in html
        assert 'download="Nicolas Ruiz.pdf"' in html

    def test_about(self):
        "Open about and check it's content"
        response = self.client.get("/about")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>NR | About</title>" in html
        assert "About <span>Me</span>" in html
        assert '''I was born in Plano, TX, and spent most of my childhood in Kansas. It was there that I discovered my passion
            for coding
            through a video game design class. When I returned to Texas for my Junior year, I continued exploring this
            interest in
            my new high school.
            <br>
            This led me to pursue a degree in computer science at The University of Texas at San Antonio. Throughout my
            studies, I
            focused on cloud and systems, gaining valuable insights from professors and peers alike.
            <br>
            In May 2023, I graduated and began working as an MLH Fellow, eager to gain more hands-on experience. I'm now
            seeking a
            role where I can apply my knowledge and continue learning alongside a collaborative team.''' in html
        assert '<img src="https://i.ibb.co/ccT9tVM/bros.jpg" alt="Photo with brothers">' in html
        assert "Where I've <span>Been</span>" in html
        assert "<script src=\"https://cdn.maptiler.com/maplibre-gl-js/v2.4.0/maplibre-gl.js\"></script>" in html
        assert "js/map_script.js" in html
        assert "updateArrowRotation();" in html

    def test_education(self):
        "Open education and check it's content"
        response = self.client.get("/education")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>NR | Education</title>" in html
        assert "<div class=\"year\"><i class='bx bxs-calendar'></i> 2018 - 2023</div>" in html
        assert "Production Engineering Fellow - MLH Fellowship" in html
        assert "<div class=\"year\"><i class='bx bxs-calendar'></i> May 2021 - May 2022</div>" in html
        assert "Smithson Valley High School" in html
        assert '<div class="education-box">' in html

    def test_pnh(self):
        "Open projects & hobbies and check it's content"
        response = self.client.get("/pnh")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Latest <span>Projects</span>" in html
        assert "Venture into the unknown and collect all your favorite cryptids." in html
        assert 'RowdE-Books' in html
        assert 'CryptidCoin' in html
        assert 'Social Circle' in html in html
        assert 'My <span>Hobbies</span>' in html
        assert 'Learning Instruments' in html
        assert 'Attending Hackathons' in html
        assert 'Mechanical Keyboards' in html
        
    def test_contact_me(self):
        "Open contact me and check it's content"
        response = self.client.get("/contact-me")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>NR | Contact Me</title>" in html
        assert "Contact <span>Me!</span>" in html
        assert '<input type="submit" value="Send Message" class="btn" onclick="return validateAndSubmit(event)">' in html
        assert '<input type="number" class="form-control" id="numberInput" name="number" placeholder="Mobile Number">' in html
        assert '<form id="contactForm" method="POST">' in html in html
        assert '<div class="input-box">' in html
        assert '<section class="contact" id="contact">' in html

    def test_timeline_route(self):
        "Open timeline, check it's content, post, and check again"
        # test GET
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>NR | Timeline</title>" in html
        assert '<form id="timelineForm" method="POST" action="/timeline">' in html
        assert '<input type="submit" value="Post" class="btn">' in html
        assert "document.getElementById('timelineForm').addEventListener('submit', function (event)" in html
        assert "updateArrowRotation();"

        # test POST for two users and use GET to test the results
        response = self.client.post("/timeline",
                                    data={"name": "John", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"})
        assert response.status_code == 201
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "John" in html
        assert "Hello world, I'm John!"

        response = self.client.post("/timeline",
                                    data={"name": "Jane", "email": "jane@example.com",
                                          "content": "Hello world, I'm Jane!"})
        assert response.status_code == 201
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Jane" in html
        assert "Hello world, I'm Jane!"
        assert "John" in html
        assert "Hello world, I'm John!"

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
        
    def get_basic_auth_headers(self):
        username = "testing"
        password = "testing"
        auth_string = f"{username}:{password}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {auth_base64}'}

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
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
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
                                          "content": "Hello world, I'm Jane!"},
                                    headers=self.get_basic_auth_headers())
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
        response = self.client.delete(f"/api/timeline_post/2",
                                    headers=self.get_basic_auth_headers())
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

        response = self.client.delete(f"/api/timeline_post/1",
                                    headers=self.get_basic_auth_headers())
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
                                    data={"email": "john@example.com", "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing content
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "john@example.com", "content": ""},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request missing email
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Empty field" in json["error"]

        # POST request with malformed email
        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "not-an-email",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "email",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "email.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "name@email",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe", "email": "name@email.c",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid email" in json["error"]

        # POST request with malformed name
        response = self.client.post("/api/timeline_post",
                                    data={"name": "J0hn Doe", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe!", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe;", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe123", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe{}", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]

        response = self.client.post("/api/timeline_post",
                                    data={"name": "John Doe@", "email": "john@example.com",
                                          "content": "Hello world, I'm John!"},
                                    headers=self.get_basic_auth_headers())
        assert response.status_code == 400
        json = response.get_json()
        assert json is not None and "error" in json
        assert "Invalid name" in json["error"]


if __name__ == '__main__':
    unittest.main()
