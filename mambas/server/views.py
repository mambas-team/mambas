import bottle
import pkg_resources

class BaseView():

    def __init__(self):
        self.view_model = {}
        self.view_model["navigation_projects"] = []
        header_path = pkg_resources.resource_filename(__package__, self.template_path("header"))
        self.view_model["header_path"] = header_path
        footer_path = pkg_resources.resource_filename(__package__, self.template_path("footer"))
        self.view_model["footer_path"] = footer_path
        self.view_model["icons"] = []

    def set_navigation_projects(self, projects):
        for project in projects:
            navigation_project = {}
            navigation_project["name"] = project.name
            navigation_project["id"] = project.id_project
            self.view_model["navigation_projects"].append(navigation_project)

    def template_path(self, type):
        # TODO: check if template file exists otherwise raise error
        return "components/html/{}.tpl.html".format(type)


class DashboardView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "dashboard"

    def create(self):
        template_path = pkg_resources.resource_filename(__package__, self.template_path(self.type))

        self.view_model["title"] = "Dashboard"

        icon_create_project = {}
        icon_create_project["type"] = "create_project"
        self.view_model["icons"].append(icon_create_project)

        view = bottle.template(template_path, self.view_model)
        return view


class ProjectDashboardView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "project_dashboard"
        
    def set_project(self, project):
        self.project = project

    def set_project_sessions(self, sessions):
        self.sessions = sessions

    def create(self):
        template_path = pkg_resources.resource_filename(__package__, self.template_path(self.type))

        # Set view model
        self.view_model["title"] = self.project.name
        # TODO: change to token
        self.view_model["token"] = self.project.id_project
        self.view_model["delete_url"] = "/projects/{}".format(self.project.id_project)
        self.view_model["number_sessions"] = len(self.sessions)

        icon_display_token = {}
        icon_display_token["type"] = "display_token"
        icon_display_token["token"] = self.project.token
        self.view_model["icons"].append(icon_display_token)

        icon_delete_project = {}
        icon_delete_project["type"] = "delete_project"
        icon_delete_project["project_name"] = self.project.name
        icon_delete_project["id_project"] = self.project.id_project
        self.view_model["icons"].append(icon_delete_project)

        view = bottle.template(template_path, self.view_model)
        return view


class ProjectSessionsView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "project_sessions"
        
    def set_project(self, project):
        self.project = project

    def set_project_sessions(self, sessions):
        self.sessions = sessions

    def create(self):
        template_path = pkg_resources.resource_filename(__package__, self.template_path(self.type))

        # Set view model
        self.view_model["title"] = self.project.name
        # TODO: change to token
        self.view_model["token"] = self.project.id_project
        self.view_model["delete_url"] = "/projects/{}".format(self.project.id_project)
        
        self.view_model["list_sessions"] = []
        for session in self.sessions:
            list_session = {}
            list_session["id"] = session.id_session
            list_session["index"] = session.index
            list_session["start_date"] = session.dt_start
            if session.dt_start is not None and session.dt_end is not None:
                list_session["duration"] = session.dt_end - session.dt_start
            list_session["is_active"] = session.is_active
            list_session["host"] = session.host
            list_session["id_project"] = self.project.id_project
            list_session["session_name"] = "{}: {}".format(self.project.name, session.index)
            self.view_model["list_sessions"].append(list_session)

        icon_display_token = {}
        icon_display_token["type"] = "display_token"
        icon_display_token["token"] = self.project.token
        self.view_model["icons"].append(icon_display_token)

        icon_delete_project = {}
        icon_delete_project["type"] = "delete_project"
        icon_delete_project["project_name"] = self.project.name
        icon_delete_project["id_project"] = self.project.id_project
        self.view_model["icons"].append(icon_delete_project)

        view = bottle.template(template_path, self.view_model)
        return view


class SessionView(BaseView):

    def __init__(self):
        super().__init__()
        self.type = "session"

    def set_project(self, project):
        self.project = project
      
    def set_session(self, session):
        self.session = session

    def set_session_epochs(self, epochs):
        self.epochs = epochs

    def create(self):
        template_path = pkg_resources.resource_filename(__package__, self.template_path(self.type))

        # Set view model
        self.view_model["title"] = "{}: Session {}".format(self.project.name, self.session.index)
        self.view_model["delete_url"] = "/projects/{}/sessions/{}".format(
            self.project.id_project, self.session.id_session)

        # Dictionary to store all graphs
        self.view_model["graphs"] = {}

        for epoch in self.epochs:
            for k, v in epoch.metrics.items():
                if "loss" in k:
                    graph_name = "loss"
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]):
                        self.view_model["graphs"][graph_name].append({"epoch": epoch.index})
                    next(d for d in self.view_model["graphs"][graph_name] if d["epoch"] == epoch.index)[k] = v
                elif "acc" in k:
                    graph_name = "acc"
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]):
                        self.view_model["graphs"][graph_name].append({"epoch": epoch.index})
                    next(d for d in self.view_model["graphs"][graph_name] if d["epoch"] == epoch.index)[k] = v
                else:
                    graph_name = k
                    if not graph_name in self.view_model["graphs"].keys():
                        self.view_model["graphs"][graph_name] = []
                    if not any(d["epoch"] == epoch.index for d in self.view_model["graphs"][graph_name]):
                        self.view_model["graphs"][graph_name].append({"epoch": epoch.index})
                    next(d for d in self.view_model["graphs"][graph_name] if d["epoch"] == epoch.index)[k] = v


        self.view_model["is_active"] = self.session.is_active
        self.view_model["number_epochs"] = len(self.epochs)
        if self.session.dt_start is not None and self.session.dt_end is not None:
            self.view_model["duration"] = self.session.dt_end - self.session.dt_start

        icon_delete_session = {}
        icon_delete_session["type"] = "delete_session"
        icon_delete_session["session_name"] = "{}: {}".format(self.project.name, self.session.index)
        icon_delete_session["id_session"] = self.session.id_session
        icon_delete_session["id_project"] = self.session.id_project
        self.view_model["icons"].append(icon_delete_session)

        view = bottle.template(template_path, self.view_model)
        return view