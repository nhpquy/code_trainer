import os

input_dir = 'inputs/'
output_dir = 'outputs/'


def get_project_root():
    return os.path.dirname(os.path.abspath(__file__))


def get_input_dir():
    return os.path.join(get_project_root(), input_dir)


def get_output_dir():
    return os.path.join(get_project_root(), output_dir)


def get_input_file(file_name):
    return os.path.join(get_project_root(), input_dir + file_name)


def get_output_file(file_name):
    return os.path.join(get_project_root(), output_dir + file_name)


def get_crawl_cmd(type, crawl_output):
    return 'scrapy crawl {} -o {}'.format(type, get_input_file(crawl_output))


if __name__ == '__main__':
    print(get_crawl_cmd("123", "itviec"))
