import bottle
import datetime
import json
import hashlib
import pkg_resources

from mambas.server import models
from mambas.server import views


class MambasWebserver(bottle.Bottle):

    def __init__(self, database):
        super().__init__()
        self.db = database

        # Gets for component styles
        self.get("/css/<filepath:re:.*\.css>", callback=self.get_css)
        self.get("/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>", callback=self.get_images)
        self.get("/icons/<filepath:re:.*\.(css|svg|woff|woff2|ttf)>", callback=self.get_icons)
        self.get("/js/<filepath:re:.*\.js>", callback=self.get_js)

        # Gets for dashboard
        self.get("/", callback=self.get_index)

        # Gets for projects
        self.get("/projects/<id_project>", callback=self.redirect_project_dashboard)
        self.get("/projects/<id_project>/", callback=self.redirect_project_dashboard)
        self.get("/projects/<id_project>/dashboard", callback=self.get_project_dashboard)
        self.get("/projects/<id_project>/sessions", callback=self.get_project_sessions)
        self.get("/projects/<id_project>/sessions/<id_session>", callback=self.get_session)

        # Posts
        self.post("/projects", callback=self.post_project)
        self.post("/projects/<id_project>/sessions", callback=self.post_session)
        self.post("/projects/<id_project>/sessions/<id_session>/epochs", callback=self.post_epoch)

        # Puts
        self.put("/projects/<id_project>/sessions/<id_session>", callback=self.put_session)

        # Deletes
        self.delete("/projects/<id_project>", callback=self.delete_project)
        self.delete("/projects/<id_project>/sessions/<id_session>", callback=self.delete_session)

        # Gets for api
        self.get("/api/id-for-token", callback=self.api_get_id_project)
    

    def get_css(self, filepath):
        css_path = pkg_resources.resource_filename(__package__, "components/css")
        return bottle.static_file(filepath, root=css_path)

    def get_images(self, filepath):
        images_path = pkg_resources.resource_filename(__package__, "components/img")
        return bottle.static_file(filepath, root=images_path)

    def get_icons(self, filepath):
        icons_path = pkg_resources.resource_filename(__package__, "components/icons")
        return bottle.static_file(filepath, root=icons_path)

    def get_js(self, filepath):
        js_path = pkg_resources.resource_filename(__package__, "components/js")
        return bottle.static_file(filepath, root=js_path)


    def get_index(self):

        view = views.DashboardView()

        navigation_projects = self.db.get_all_projects()
        view.set_navigation_projects(navigation_projects)

        return view.create()


    def redirect_project_dashboard(self, id_project):
        bottle.redirect("/projects/{}/dashboard".format(id_project))
        

    def get_project_dashboard(self, id_project):

        project = self.db.get_project(id_project)

        # TODO: return 404 here if project does not exist

        view = views.ProjectDashboardView()
        view.set_project(project)

        sessions = self.db.get_sessions_for_project(id_project)
        view.set_project_sessions(sessions)

        navigation_projects = self.db.get_all_projects()
        view.set_navigation_projects(navigation_projects)

        return view.create()


    def get_project_sessions(self, id_project):
        
        project = self.db.get_project(id_project)

        # TODO: return 404 here if project does not exist

        view = views.ProjectSessionsView()
        view.set_project(project)

        sessions = self.db.get_sessions_for_project(id_project)
        view.set_project_sessions(sessions)

        navigation_projects = self.db.get_all_projects()
        view.set_navigation_projects(navigation_projects)

        return view.create()


    def get_session(self, id_project, id_session):

        project = self.db.get_project(id_project)

        # TODO: return 404 here if project does not exist

        session = self.db.get_session(id_session)

        # TODO: return 404 here if session does not exist

        view = views.SessionView()
        view.set_project(project)
        view.set_session(session)

        epochs = self.db.get_epochs_for_session(id_session)
        view.set_session_epochs(epochs)

        navigation_projects = self.db.get_all_projects()
        view.set_navigation_projects(navigation_projects)

        return view.create()


    def post_project(self):
        # Load message
        message = json.load(bottle.request.body)

        project_name = message["name"]

        time = datetime.datetime.now()
        time_str = str(time).encode("utf-8")
        hash = hashlib.md5(time_str)
        token = hash.hexdigest()

        # Create project
        project = self.db.create_project(project_name, token)

        # Prepare answer
        answer = {"id": project.id_project}
        bottle.response.content_type = "application/json"
        
        return json.dumps(answer)

    
    def delete_project(self, id_project):
        # Get project
        project = self.db.get_project(id_project)

        # Get sessions for this project
        sessions = self.db.get_sessions_for_project(id_project)

        # Delete all sessions
        for session in sessions:
            self.delete_session(id_project, session.id_session)

        # Delete this project
        self.db.delete_project(project.id_project)


    def delete_session(self, id_project, id_session):
        # Get session
        session = self.db.get_session(id_session)

        # Get epochs for this session
        epochs = self.db.get_epochs_for_session(session.id_session)

        # Delete all epochs
        for epoch in epochs:
            self.db.delete_epoch(epoch.id_epoch)
        
        # Delete this session
        self.db.delete_session(session.id_session)


    def post_session(self, id_project):
        # Get project
        project = self.db.get_project(id_project)
        # TODO: raise error if project not exists
        
        # Increment session counter and get session index for this project
        self.db.increment_project_session_counter(id_project)
        session_index = project.session_counter

        # Create session
        session = self.db.create_session_for_project(session_index, id_project)

        # Prepare answer
        answer = {"id_session": session.id_session}
        bottle.response.content_type = "application/json"
        
        return json.dumps(answer)


    def put_session(self, id_project, id_session):
        # Get project
        project = self.db.get_project(id_project)
        # TODO: raise error id project not exists

        # Get session
        session = self.db.get_session(id_session)
        # TODO: raise error if session not exists

        # Load message
        message = json.load(bottle.request.body)

        if "start" in message and bool(message["start"]):
            # Set session start time
            self.db.set_session_start_time(session.id_session, datetime.datetime.now())

        if "model" in message:
            model = message["model"]
            # TODO: store model in database

        if "end" in message and bool(message["end"]):
            # Set session is_active flag to False
            # TODO: remove flag and use dt_end timestamp
            self.db.set_session_end_time(session.id_session, datetime.datetime.now())

            # Set session end time
            self.db.set_session_inactive(session.id_session)


    def post_epoch(self, id_project, id_session):
        # Get project
        project = self.db.get_project(id_project)
        # TODO: raise error if project not exists

        # Get session
        session = self.db.get_session(id_session)
        # TODO: raise error if session not exists

        # Load message
        message = json.load(bottle.request.body)

        # Get values from message
        epoch_index = message["epoch"]
        metrics = message["metrics"]

        # Store data
        epoch = self.db.create_epoch_for_session(epoch_index, metrics, session.id_session)

        # Prepare answer
        answer = {"id_epoch": epoch.id_epoch}
        bottle.response.content_type = "application/json"
        
        return json.dumps(answer)


    def api_get_id_project(self):
        query = bottle.request.query.decode()

        if not "token" in query:
            bottle.abort(400)

        token = bottle.request.query["token"]

        project = self.db.get_project_by_token(token)
        
        if project is None:
            bottle.abort(404)

        # Prepare answer
        answer = {"id_project": project.id_project}
        bottle.response.content_type = "application/json"
        
        return json.dumps(answer)