import collections
import datetime
import logging
import re
import subprocess

logger = logging.getLogger(__name__)

Pagination = collections.namedtuple('Pagination', ['next', 'previous'])
Project = collections.namedtuple(
    'Project', ['key', 'title', 'description', 'image', 'pattern', 'entries'])
GitInfo = collections.namedtuple('GitInfo',
                                 ['head', 'head_short', 'head_summary'])
Context = collections.namedtuple('Context', [
    'entries',
    'git',
    'latest',
    'pages',
    'pagination',
    'projects',
    'root_directory',
    'timestamp',
])


def shell_command(cmd):
    result = subprocess.run(cmd.split(' '), capture_output=True)
    return result.stdout.decode('UTF-8').strip()


def build_pagination_map(entries=[]) -> dict:
    pagination = {}

    for i, entry in enumerate(entries):
        if i > 0:
            previous_entry = entries[i - 1].filename
        else:
            previous_entry = None

        try:
            next_entry = entries[i + 1].filename
        except IndexError:
            next_entry = None

        pagination[entry.filename] = Pagination(next_entry, previous_entry)

    return pagination


def build_project_map(config) -> dict:
    projects = {}

    for section in config.sections():
        try:
            _, key = section.split('project:')
            title = config[section]['title']
            description = config[section]['description']
            image = config[section]['image']
            pattern = re.compile(config[section]['pattern'])
            project = Project(key=key,
                              title=title,
                              description=description,
                              image=image,
                              pattern=pattern,
                              entries=[])
            logger.debug('extracted %s from config', project)
            projects[key] = project
        except (ValueError, KeyError):
            continue

    return projects


def build_projects(config, entries=[]) -> dict:
    projects = build_project_map(config)

    for entry in entries:
        for project in projects.values():
            if project.pattern.match(entry.description):
                project.entries.append(entry)
                logger.debug('adding %s to %s', entry, project)
                break

    return projects


def gather_git_info() -> GitInfo:
    return GitInfo(
        head=shell_command('git rev-parse HEAD'),
        head_short=shell_command('git rev-parse --short HEAD'),
        head_summary=shell_command('git log -1 --pretty=format:%s HEAD'),
    )


def build_global_context(root_directory=None,
                         config=None,
                         entries=[],
                         pages=[]) -> Context:
    timestamp = datetime.datetime.now()
    logger.debug('created build timestamp %s', timestamp)

    git = gather_git_info()
    logger.debug('gathered git info %s', git)

    pagination = build_pagination_map(entries)
    logger.debug('built pagination map from %d entry file(s)', len(entries))

    projects = build_projects(config=config, entries=entries)
    logger.debug('mapped entries to %d projects', len(projects.keys()))

    latest = entries[-1]
    logger.debug('cached latest entry %s', latest)

    return Context(root_directory=root_directory,
                   timestamp=timestamp,
                   git=git,
                   pagination=pagination,
                   projects=projects,
                   latest=latest,
                   entries=entries,
                   pages=pages)
