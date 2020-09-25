from py2neo import NodeMatcher

from connector import settings
from connector.models import *
from connector.neo4jconnector import Neo4jConnection

log = logging.getLogger(__name__)


class Pipeline:
    """
    The Pipeline to define the processing of the data
    """

    def __init__(self, *args, **kwargs):
        self._name = type(self).__name__
        self.graph = None
        self.matcher = None
        self._init_neo4j()

    def _init_neo4j(self):
        self.graph = Neo4jConnection(
            settings.NEO4J_URL,
            settings.NEO4J_USER,
            settings.NEO4J_PASSWORD
        ).get_graph()
        self.matcher = NodeMatcher(self.graph)

    @property
    def full_name(self):
        return self._name

    @property
    def name(self):
        name, _ = self._name.split("Pipeline")
        return name

    def transform_data(self, *args, **kwargs):
        """
        Abstract method to transform the requested data into a another format
        """
        raise NotImplementedError()


class CrawlPipeline(Pipeline):
    """
    A pipeline to process Job
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.crawl_result = None

    def transform_data(self):
        entity_model = Entity.get(self.graph, {'id': self.crawl_result.get('entity')['id']})
        if entity_model is None:
            entity_model = Entity.create(self.graph, self.crawl_result.get('entity'))

        for job in self.crawl_result.get('jobs'):
            job_model = Job.get(self.graph, {'id': job['id']}).first()
            if job_model is None:
                job_model = Job.create(self.graph, job)
            entity_model.add_job(job_model)

            for language in self.crawl_result.get('languages'):
                language_model = Language.get(self.graph, {'id': language['id']}).first()
                if language_model is None:
                    language_model = Language.create(self.graph, language)
                    language_model.in_job(job_model)
                    language_model.save(self.graph)
                job_model.languages.update(language_model)

            for framework in self.crawl_result.get('frameworks'):
                framework_model = Framework.get(self.graph, {'id': framework['id']}).first()
                if framework_model is None:
                    framework_model = Framework.create(self.graph, framework)
                    framework_model.in_job(job_model)
                    framework_model.save(self.graph)
                job_model.frameworks.update(framework_model)

            for knowledge in self.crawl_result.get('knowledges'):
                knowledge_model = Language.get(self.graph, {'id': knowledge['id']}).first()
                if knowledge_model is None:
                    knowledge_model = Knowledge.create(self.graph, knowledge)
                    knowledge_model.in_job(job_model)
                    knowledge_model.save(self.graph)
                job_model.knowledges.update(knowledge_model)

            for device in self.crawl_result.get('devices'):
                device_model = Device.get(self.graph, {'id': device['id']}).first()
                if device_model is None:
                    device_model = Device.create(self.graph, device)
                    device_model.in_job(job_model)
                    device_model.save(self.graph)
                job_model.devices.update(device_model)

            for experience in self.crawl_result.get('experiences'):
                exp_model = Experience.get(self.graph, {'id': experience['id']}).first()
                if exp_model is None:
                    exp_model = Experience.create(self.graph, experience)
                    exp_model.in_job(job_model)
                    exp_model.save(self.graph)
                job_model.experiences.update(exp_model)

            job_model.save(self.graph)

        entity_model.save(self.graph)
