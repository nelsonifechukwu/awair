from app.models import User, Darla, Uuid
from app.generateID import Generate
from app.extensions import db
from app.passwords import Password
from config import Config
import os
class TestDatabase:
    pass
class TestClasses:
    def test_password(self):
        # encrypt
        password = "Pass"
        key, encrypted = Password().encrypt_password(password)
        assert isinstance(encrypted, str)
        assert isinstance(key, str)
        # decrypt
        decrypted = Password(key).decrypt_password(encrypted)
        assert password == decrypted
    def test_generateID(self):
        id = Generate(10).id
        assert len(id) ==10
        assert isinstance(id,str)

class TestRegisterLogin:
    def test_register_and_login(self, app, client):
        with app.app_context():
            id = "123w45t67r"
            new_darla = Darla(device_id=id)
            db.session.add(new_darla)
            db.session.commit()

        response = client.post("/signup", data={"name": "yo", "username": "yo", "email": "yo@yahoo.com", "password": "yo"})
        assert response.status_code == 301

        response = client.post("/login", data={"username": "yo", "password": "yo"})
        assert response.status_code == 302

        with app.app_context():
            assert Darla.query.count() == 1
            assert User.query.count() == 1
            assert len(Darla.query.first().device_id) == 10

    def test_dashboard_routes(self, app, client):
        with app.app_context():
            id = "123w45t67r"
            new_darla = Darla(device_id=id)
            db.session.add(new_darla)
            db.session.commit()

        signup_response = client.post("/signup", data={"name":"yo", "username":"yo", "email":"yo@yahoo.com", "password":"yo"})
        assert signup_response.status_code == 301 

        login_response = client.post("/login", data={"username": "yo", "password": "yo"})
        assert login_response.status_code == 302

        redirect = client.get("/dashboard/1")
        assert redirect.status_code == 200

        # Add more tests for other routes

class TestDashboardRoutes:
    def login_method(self, app, client):
        with app.app_context():
            id = "123w45t67r"
            new_darla = Darla(device_id=id)
            db.session.add(new_darla)
            db.session.commit()

        client.post("/signup", data={"name":"yo", "username":"yo", "email":"yo@yahoo.com", "password":"yo"})
        session = client.post("/login", data={"username": "yo", "password": "yo"})
        add_device_response = client.post("/dashboard/1", data={"uuid": id})
        assert add_device_response.status_code == 302

        with app.app_context():
            assert Uuid.query.count() == 1
            assert Uuid.query.first().user_id == 1
        return session.headers.get("Set-Cookie").split(";")[0],id
        # assert TestDashboardRoutes.cookie == "123"
    def test_add_device_to_dashboard(self, app, client):
        session, id = self.login_method(app, client)
        response = client.get("/dashboard/1/123", headers ={"Cookie":session})
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}")
        assert response.status_code == 200
        assert "Data" in response.data.decode()
        
    def test_dashboard_list(self, client, app):
        session, id = self.login_method(app, client)
        response = client.get(f"/dashboard/1/{id}/airquality",headers ={"Cookie":session})
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/airquality", headers = {'Hx-Request': 'true'})
        assert response.status_code == 200
        response = client.get(f"/dashboard/1/{id}/tph")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/tph", headers = {'Hx-Request': 'true'})
        assert response.status_code == 200
        response = client.get(f"/dashboard/1/{id}/wind")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/wind", headers = {'Hx-Request': 'true'})
        assert response.status_code == 200
        response = client.get(f"/dashboard/1/{id}/precipitation")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/precipitation", headers = {'Hx-Request': 'true'})
        assert response.status_code == 200
        
    def test_dashboard_graph(self, client,app):
        session, id = self.login_method(app, client)
        # tph
        response = client.get(f"/dashboard/1/{id}/charts/1/tph",headers ={"Cookie":session})
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/tph/latest")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/1/tph",headers ={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        assert isinstance(response.data.decode(), str)
        response = response.json
        assert isinstance(response, dict)
        assert 'labels' in response
        assert isinstance(response['labels'], list)
        assert 'temperature_data' in response
        assert isinstance(response['temperature_data'], list)
        assert 'humidity_data' in response
        assert isinstance(response['humidity_data'], list)
        assert 'pressure_data' in response
        assert isinstance(response['pressure_data'], list)
        response = client.get(f"/dashboard/1/{id}/charts/tph/latest",headers ={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        response = response.json
        assert isinstance(response, dict)
        assert len(response) == 0
        
        
        # air
        response = client.get(f"/dashboard/1/{id}/charts/1/air")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/air/latest")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/1/air",headers ={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        assert isinstance(response.data.decode(), str)
        response = response.json
        assert isinstance(response, dict)
        assert 'labels' in response
        assert isinstance(response['labels'], list)
        assert 'pmtwo_data' in response
        assert isinstance(response['pmtwo_data'], list)
        assert 'pmten_data' in response
        assert isinstance(response['pmten_data'], list)
        assert 'co_data' in response
        assert isinstance(response['co_data'], list)
        response = client.get(f"/dashboard/1/{id}/charts/air/latest",headers ={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        response = response.json
        assert isinstance(response, dict)
        assert len(response) == 0
        
        # wind
        response = client.get(f"/dashboard/1/{id}/charts/1/wind")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/1/wind", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        response = response.json
        assert isinstance(response, list)
        response = client.get(f"/dashboard/1/{id}/charts/wind/latest")
        assert response.status_code == 404
        response = client.get(f"/dashboard/1/{id}/charts/wind/latest", headers={'X-Requested-With': 'XMLHttpRequest'})
        assert response.status_code == 200
        response = response.json
        assert isinstance(response, dict)
        assert "date" in response
        assert "speed" in response
        assert "direction" in response
    def test_map_location(self, app, client):
        pass

class TestUploads(TestDashboardRoutes):
    def test_image_upload(self,app,client):
        session, id = self.login_method(app, client)
        response = client.get("/dashboard/1", headers={"Cookie":session})
        assert response.status_code == 302
        response = client.get(f"/dashboard/1/{id}")
        assert response.status_code == 200
        # print(response.data.decode())
        assert b"Data" in response.data
        response = client.get("/dashboard/1/profile/upload")
        assert response.status_code == 405
        data =   {'profile':(open('/Users/spaceinafrica/Downloads/bus.jpeg','rb'),'bus.jpeg')
        }
        headers = {'Content-Type': 'multipart/form-data'}
        response =client.post("/dashboard/1/profile/upload", headers=headers, data=data)
        assert response.status_code == 201
        with app.app_context():
            assert User.query.filter_by(id=1).first().profile_picture == "1__bus.jpeg"
        assert os.path.exists(Config.UPLOADS+"1__bus.jpeg") 
        # Remove
        response =client.post("/dashboard/1/profile/remove")
        assert response.status_code == 405
        response = client.get("/dashboard/1/profile/remove")
        assert response.status_code == 302
        with app.app_context():
            assert User.query.filter_by(id=1).first().profile_picture == None
        assert not os.path.exists(Config.UPLOADS+ "1__bus.jpeg") 
        
    


    
# import responses
# # More research has to be done on mocking !!!!!!!!!!!!!!!!!!!!!!!!!!
# # @responses.activate
# # def test_google(client):
# #     responses.add(
# #         responses.GET,
# #         'https://accounts.google.com/.well-known/openid-configuration',
# #         json={
# #             "authorization_endpoint": "https://accounts.google.com/o/oauth2/auth",
# #             "token_endpoint": "https://accounts.google.com/o/oauth2/token",
# #             "userinfo_endpoint": "https://www.googleapis.com/oauth2/v3/userinfo",
# #         },
# #         status=200,
# #     )
# #     responses.add(
# #         responses.POST,
# #         'https://accounts.google.com/o/oauth2/token',
# #         json={
# #             "access_token": "mock_access_token",
# #             "expires_in": 3600,
# #             "token_type": "Bearer",
# #         },
# #         status=200,
# #     )
# #     responses.add(
# #         responses.GET,
# #         'https://www.googleapis.com/oauth2/v3/userinfo',
# #         json={
# #             "sub": "mock_user_id",
# #             "email": "mock@example.com",
# #             "email_verified": True,
# #             "given_name": "Mock",
# #             "picture": "https://example.com/mock.jpg",
# #         },
# #         status=200,
# #     )
# #     response = client.get('/googlelogin')
# #     # print(response.data.decode())
# #     assert response.status_code == 302
# #     response = client.get('/googlelogin/callback')
# #     # print(response.data.decode())
# #     assert response.status_code == 200
# #     assert b'mock_access_token' in response.data