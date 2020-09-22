import logging

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, RelatedObjects

# graph = Neo4jConnection(
#     settings.NEO4J_URL,
#     settings.NEO4J_USER,
#     settings.NEO4J_PASSWORD
# ).get_graph()

log = logging.getLogger(__name__)


class NeoGraphObjectException(Exception):
    pass


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    id = Property("id")
    value = Property("value")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def find(cls, matcher, **kwargs):
        """
        Matches the first label by a given keyword arguments
        """
        obj = matcher.match(**kwargs).first()
        return obj

    @classmethod
    def create(cls, graph: Graph, attributes: dict = None):
        """
        Create a label from given attributes.\
        At least the the __primarykey__ must available in the attributes dictionary.
        """
        obj = cls()
        if cls.__primarykey__ not in attributes:
            raise NeoGraphObjectException(f"Primary '{obj.__primarykey__}' not in attributes")
        for attr, attr_value in attributes.items():
            if hasattr(obj, attr) and not isinstance(getattr(obj, attr), RelatedObjects):
                setattr(obj, attr, attr_value)
        graph.create(obj)
        return obj

    @classmethod
    def get(cls, graph: Graph, filters: dict):
        """
        Matches a labels from cls and reduces the result by the given filters.
        """
        obj = cls.match(graph)
        for attr, attr_value in filters.items():
            obj = obj.where(**{attr: attr_value})
        obj = obj.first()
        return obj

    @classmethod
    def get_or_create(cls, graph: Graph, pk=None, attributes: dict = None):
        """
        Serves as helper method to retrieve labels from the graph or create a new one if no label existed
        """
        if pk is None:
            raise NeoGraphObjectException(f"Primary key missing")
        obj = cls.get(graph, filters={cls.__primarykey__: pk})
        if not obj:
            if attributes is not None:
                attributes = {cls.__primarykey__: pk, **attributes}
            else:
                attributes = {cls.__primarykey__: pk}
            obj = cls.create(graph, attributes)
        return obj

    def save(self, graph: Graph):
        """
        Commit a labels from cls.
        """
        graph.push(self)

    def as_dict(self):
        return {
            'id': self.id,
            'value': self.value
        }


class Device(BaseModel):
    __primarylabel__ = "Device"
    __primarykey__ = "id"

    jobs = RelatedFrom('Job', 'REQUIRED_IN')

    def in_job(self, job):
        self.jobs.update(job)


class Knowledge(BaseModel):
    __primarylabel__ = "Knowledge"
    __primarykey__ = "id"

    jobs = RelatedFrom('Job', 'REQUIRED_IN')

    def in_job(self, job):
        self.jobs.update(job)


class Experience(BaseModel):
    __primarylabel__ = "Experience"
    __primarykey__ = "id"

    jobs = RelatedFrom('Job', 'REQUIRED_IN')

    def in_job(self, job):
        self.jobs.update(job)


class Language(BaseModel):
    __primarylabel__ = "Language"
    __primarykey__ = "id"

    jobs = RelatedFrom('Job', 'REQUIRED_IN')

    def in_job(self, job):
        self.jobs.update(job)


class Framework(BaseModel):
    __primarylabel__ = "Framework"
    __primarykey__ = "id"

    jobs = RelatedFrom('Job', 'REQUIRED_IN')

    def in_job(self, job):
        self.jobs.update(job)


class Job(BaseModel):
    __primarylabel__ = "Job"
    __primarykey__ = "id"

    entity = RelatedFrom('Entity', 'IN_ENTITY')
    languages = RelatedTo('Language', 'HAS_LANGUAGE')
    frameworks = RelatedTo('Framework', 'HAS_FRAMEWORK')
    knowledges = RelatedTo('Knowledge', 'HAS_KNOWLEDGE')
    devices = RelatedTo('Device', 'HAS_DEVICE')
    experiences = RelatedTo('Experience', 'HAS_EXPERIENCE')

    def in_entity(self, entity):
        self.entity.update(entity)


class Entity(BaseModel):
    __primarylabel__ = "Entity"
    __primarykey__ = "id"

    create_at = Property("create_at")

    has_job = RelatedTo('Job', 'has_Job')

    def as_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'create_at': self.create_at
        }

    def add_job(self, job):
        self.has_job.add(job)


class URL(BaseModel):
    __primarylabel__ = "URL"
    __primarykey__ = "id"

    entities = RelatedTo('Entity', 'HAS_ENTITY')
