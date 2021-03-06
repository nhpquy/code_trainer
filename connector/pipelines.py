import hashlib
import time

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

    # Khi tao 1 Object Pipeline moi => Python se goi ham _init nay
    # Nen chi can tao 1 object ban dau, de thiet lap ket noi voi Neo4J
    # Sau do gan lai bien result roi thuc hien transform du lieu thanh graph
    # => tiet kiem duoc tgian ket noi voi Neo4j
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


# Class CrawlPipeline ke thua Pipeline de su dung ham init connection cua lop cha
# Va co field result rieng, field de luu ket qua phan tich sau khi crawl du lieu
class CrawlPipeline(Pipeline):
    """
    A pipeline to process Job
    """

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.crawl_result = None

    # Ham transform data, tu du lieu crawl da phan tich sang dang graph cua Neo4j
    # 1 Cau se co cau truc grpah nhu sau:
    # Ghi chu ben file models

    def transform_data(self):
        # Tao Node Entity
        # Voi moi Node (Dinh) cua graph ta se tim trong database xem no da ton tai hay chua bang Id la hash md5 cua no.
        # Vi du: PHP Developer (WordPress, Magento) se la 1 node cua Job, neu co se query len bang id cua node, neu khong co se tao moi

        # Ham query 'get' voi id cua Entity
        entity_model = Entity.get(self.graph, {'id': self.crawl_result.get('entity')['id']})
        # Tao moi neu khong thay
        if entity_model is None:
            entity_model = Entity.create(self.graph, self.crawl_result.get('entity'))

        # Tuong tu nhu vay se den Job: 1 cau se co nhieu Job
        for job in self.crawl_result.get('jobs'):
            job_model = Job.get(self.graph, {'id': job['id']})
            if job_model is None:
                job_model = Job.create(self.graph, job)

            # Them lien ket quan he con voi Job cho Entity
            entity_model.add_job(job_model)

            # Trong moi Job se co cac knowledge
            # => Them 1 vong lap cho cac knowledge thuoc Job, de tao cac lien ket quan he con cho Job voi cac knowledge nay
            for language in self.crawl_result.get('languages'):
                language_model = Language.get(self.graph, {'id': language['id']})
                if language_model is None:
                    language_model = Language.create(self.graph, language)
                    language_model.in_job(job_model)
                    language_model.save(self.graph)
                # Them lien ket quan he con Model voi Job
                job_model.languages.add(language_model)

            for framework in self.crawl_result.get('frameworks'):
                framework_model = Framework.get(self.graph, {'id': framework['id']})
                if framework_model is None:
                    framework_model = Framework.create(self.graph, framework)
                    framework_model.in_job(job_model)
                    framework_model.save(self.graph)
                # Them lien ket quan he con Framework voi Job
                job_model.frameworks.add(framework_model)

            for knowledge in self.crawl_result.get('knowledges'):
                knowledge_model = Language.get(self.graph, {'id': knowledge['id']})
                if knowledge_model is None:
                    knowledge_model = Knowledge.create(self.graph, knowledge)
                    knowledge_model.in_job(job_model)
                    knowledge_model.save(self.graph)
                # Them lien ket quan he con Knowledge voi Job
                job_model.knowledges.add(knowledge_model)

            for device in self.crawl_result.get('devices'):
                device_model = Device.get(self.graph, {'id': device['id']})
                if device_model is None:
                    device_model = Device.create(self.graph, device)
                    device_model.in_job(job_model)
                    device_model.save(self.graph)
                # Them lien ket quan he con Device voi Job
                job_model.devices.add(device_model)

            for experience in self.crawl_result.get('experiences'):
                exp_model = Experience.get(self.graph, {'id': experience['id']})
                if exp_model is None:
                    exp_model = Experience.create(self.graph, experience)
                    exp_model.in_job(job_model)
                    exp_model.save(self.graph)
                # Them lien ket quan he con Exp voi Job
                job_model.experiences.add(exp_model)

            # Sau khi hoan thanh tao cac Node knowledge va cac lien ket cua cac node nay voi node cha Job
            # Luu chung' xuong database bang ham save
            job_model.save(self.graph)

        # Tuo0ng tu Luu Node Entity xuong database: Node Entity nay da co quan he voi cac Job
        entity_model.save(self.graph)


if __name__ == '__main__':
    entity = "{\"title\":[\"PHP Developer (WordPress, Magento)\"],\"mo_ta\":[\"Working with BA, designers discuss website design and function.\",\"Building the website front-end.\",\"Creating the website architecture.\",\"Building and managing the website back-end including database and server integration.\",\"Generating WordPress themes and plugins.\",\"Conducting website performance tests.\",\"Troubleshooting website issues.\",\"Monitoring the performance of the live website.\",\"Responsible for the assigned project.\"],\"yeu_cau\":[\"Proven work experience with 3+ years of PHP developer or 2+ years of Wordpress developer.\",\"Knowledge of front-end technologies including CSS3, JavaScript, HTML5, and jQuery.\",\"Knowledge of code versioning tools, such as Git.\",\"Experience working with debugging tools such as Chrome Inspector and Firebug.\",\"Good at problem-solving.\",\"Good understanding of website architecture and aesthetics.\",\"Good communication skills.\",\"Experience with e-commerce plugins like Woocommerce.\",\"Knowledge of Magento is an advantage.\",\"Knowledge of CSS preprocessors including SCSS, SASS or LESS.\",\"Good English skills.\",\"Good presentation skills.\",\"Ability to project manage.\",\"Knowledge of issue tracking tools, such as Jira.\"]}"
    job = {
        'id': hashlib.md5('PHP Developer (WordPress, Magento)'.encode('utf-8')).hexdigest(),
        'value': 'PHP Developer (WordPress, Magento)'
    }
    language1 = {
        'id': hashlib.md5('PHP'.encode('utf-8')).hexdigest(),
        'value': 'PHP'
    }
    language2 = {
        'id': hashlib.md5('HTML5'.encode('utf-8')).hexdigest(),
        'value': 'HTML5'
    }
    language3 = {
        'id': hashlib.md5('jQuery'.encode('utf-8')).hexdigest(),
        'value': 'jQuery'
    }
    framework = {
        'id': hashlib.md5('Wordpress'.encode('utf-8')).hexdigest(),
        'value': 'Wordpress'
    }
    knowledge1 = {
        'id': hashlib.md5('Knowledge of CSS preprocessors including SCSS, SASS or LESS'.encode('utf-8')).hexdigest(),
        'value': 'Knowledge of CSS preprocessors including SCSS, SASS or LESS'
    }
    knowledge2 = {
        'id': hashlib.md5('Good English skills'.encode('utf-8')).hexdigest(),
        'value': 'Good English skills'
    }
    knowledge3 = {
        'id': hashlib.md5('Ability to project manage'.encode('utf-8')).hexdigest(),
        'value': 'Ability to project manage'
    }
    experience1 = {
        'id': hashlib.md5('3+ years of PHP developer'.encode('utf-8')).hexdigest(),
        'value': '3+ years of PHP developer'
    }
    experience2 = {
        'id': hashlib.md5('2+ years of Wordpress developer'.encode('utf-8')).hexdigest(),
        'value': '2+ years of Wordpress developer'
    }

    result = {
        'entity': {
            'id': hashlib.md5(entity.encode('utf-8')).hexdigest(),
            'value': entity,
            'created_at': time.time()
        },
        'jobs': [job],
        'languages': [language1, language2, language3],
        'frameworks': [framework],
        'knowledges': [knowledge1, knowledge2, knowledge3],
        'devices': [],
        'experiences': [experience1, experience2]
    }

    crawl_pipeline = CrawlPipeline()
    crawl_pipeline.crawl_result = result
    crawl_pipeline.transform_data()