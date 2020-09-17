import logging

from py2neo import Graph, NodeMatcher

log = logging.getLogger(__name__)


class Pipeline:
    """
    The Pipeline to define the processing of the data
    """

    def __init__(self, config, *args, **kwargs):
        self._name = type(self).__name__
        self._config = config
        self.graph = None
        self.matcher = None
        self._init_neo4j()

    def _init_neo4j(self):
        hostname = self._config['NEO4J']['hostname']
        protocol = self._config['NEO4J']['protocol']
        port = self._config['NEO4J']['port']
        db = self._config['NEO4J']['db']
        user = self._config['NEO4J']['user']
        password = self._config['NEO4J']['password']
        self.graph = Graph(f"{protocol}://{hostname}:{port}/{db}",
                           user=user,
                           password=password)
        self.matcher = NodeMatcher(self.graph)

    @property
    def full_name(self):
        return self._name

    @property
    def name(self):
        name, _ = self._name.split("Pipeline")
        return name

    def get_config_attribute(self, attr: str, section: str = None) -> str:
        """
        Extracts an attribute from an certain section in the configuration file. \
        The default section is the pipeline name it self.
        """
        if section is None:
            section = self.full_name
        try:
            pipe_section = self._config[section]
            attr_value = pipe_section[attr]
            return attr_value
        except KeyError:
            # raise PipelineException(f"Attribute '{attr}' is not defined in {section}.")
            # raise PipelineException(f"Requested pipeline '{section}' is not configured.")
            pass

    def request_data(self, *args, **kwargs):
        """
        Abstract method to implement the request of data
        """
        raise NotImplementedError()

    def transform_data(self, *args, **kwargs):
        """
        Abstract method to transform the requested data into a another format
        """
        raise NotImplementedError()

    def commit_data(self, *args, **kwargs):
        """
        Abstract method for writing transformed data to somewhere
        """
        raise NotImplementedError()


class JobPipeline(Pipeline):
    """
    A pipeline to process Job
    """

    def __init__(self, config, *arg, **kwargs):
        super().__init__(config, *arg, **kwargs)
        self.issues = None
        self.issue_model_list = []

    def request_data(self):
        self.issues = self.project.issues.list(all=True)

    def transform_data(self):
        for issue in self.issues:
            issue_model = models.Issue.create(self.graph, issue.attributes)
            # issue_model.belongs_to.update(self.project_model)

            author_id = issue.attributes.get('author')
            if author_id:
                author_id = author_id['id']
                author_dict = models.User.match(self.graph, author_id).first()
                issue_model.created_by.update(author_dict)

            for assignee in issue.attributes.get('assignees'):
                assignee_id = assignee['id']
                author_dict = models.User.match(self.graph, assignee_id).first()
                issue_model.was_assigned.update(author_dict)

            assignee = issue.attributes.get('assignee')
            if assignee:
                assignee_id = assignee['id']
                author_dict = models.User.match(self.graph, assignee_id).first()
                issue_model.is_assigned.update(author_dict)

            closer_id = issue.attributes.get('closed_by')
            if closer_id:
                closer_id = closer_id['id']
                author_dict = models.User.match(self.graph, closer_id).first()
                issue_model.closed_by.update(author_dict)

            for label_name in issue.attributes.get('labels'):
                lbl_match = models.Label.match(self.graph).where(f"_.name =~ '{label_name}'")
                if lbl_match:
                    issue_model.has_label.update(lbl_match.first())

            milestone_id = issue.attributes.get('milestone')
            if milestone_id:
                milestone_id = milestone_id['id']
                milestone_match = models.Milestone.match(self.graph, milestone_id)
                if milestone_match:
                    issue_model.has_milestone.update(milestone_match.first())

            if issue.attributes.get('has_tasks') is True:
                task_status = issue.attributes.get('task_completion_status')
                issue_model.task_count = task_status.get('task_count')
                issue_model.task_completed = task_status.get('completed_count')

            for note in issue.notes.list():
                note_model = models.Note.get_or_create(self.graph, note.id, note.attributes)
                # note_model.belongs_to.update(self.project_model)
                if note.attributes.get('author'):
                    author_dict = note.attributes.get('author')
                    author_obj = models.User.match(self.graph, author_dict['id']).first()
                    note_model.has_author.update(author_obj)
                for award_emoji in note.awardemojis.list():
                    emoji_model = models.AwardEmoji.get_or_create(self.graph, award_emoji.id, award_emoji.attributes)
                    if award_emoji.attributes.get('user'):
                        awarder_dict = award_emoji.attributes.get('user')
                        awarder_obj = models.User.match(self.graph, awarder_dict['id']).first()
                        emoji_model.was_awarded_by.update(awarder_obj)
                    self.graph.push(emoji_model)
                    note_model.was_awarded_with.update(emoji_model)
                self.graph.push(note_model)
                issue_model.has_note.update(note_model)

            for award_emoji in issue.awardemojis.list():
                emoji_model = models.AwardEmoji.get_or_create(self.graph, award_emoji.id, award_emoji.attributes)
                if award_emoji.attributes.get('user'):
                    awarder_dict = award_emoji.attributes.get('user')
                    awarder_obj = models.User.match(self.graph, awarder_dict['id']).first()
                    emoji_model.was_awarded_by.update(awarder_obj)
                self.graph.push(emoji_model)
                issue_model.was_awarded_with.update(emoji_model)
            self.issue_model_list.append(issue_model)

    def commit_data(self):
        for issue_model in self.issue_model_list:
            self.graph.push(issue_model)
