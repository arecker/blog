import collections
import re

from newsrc import load_config, logger

Project = collections.namedtuple('Project', 'key, pattern')


def each_project_section(config):
    for section in config.sections():
        if section.startswith('project:'):
            _, key = section.split('project:')
            pattern = re.escape(config[section]['pattern'])
            project = Project(key, pattern)
            yield project


def build_project_map(entries=[]):
    """
    builds a map of projects to their list of entries
    """
    config = load_config()

    result = collections.defaultdict(list)

    for entry in entries:
        for project in each_project_section(config):
            if re.match(project.pattern, entry.description):
                logger.debug('adding %s to %s', entry, project)
                result[project.key].append(entry)
                break

    return result
