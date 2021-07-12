import collections
import re

from newsrc import load_config, logger

Project = collections.namedtuple('Project', 'key, pattern')


def projects_from_config(config):
    projects = []

    for section in config.sections():
        if section.startswith('project:'):
            _, key = section.split('project:')
            pattern = config[section]['pattern']
            project = Project(key, pattern)
            projects.append(project)

    return projects


def build_project_map(entries=[]):
    """
    builds a map of projects to their list of entries
    """
    config = load_config()

    result = collections.defaultdict(list)
    projects = projects_from_config(config)

    for entry in entries:
        for project in projects:
            if re.match(project.pattern, entry.description):
                logger.debug('adding %s to %s', entry, project)
                result[project.key].append({
                    'description': entry.description,
                    'permalink': entry.permalink,
                })
                break

    return result
