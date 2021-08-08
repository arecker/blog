import collections
import contextlib

TargetGroup = collections.namedtuple('TargetGroup',
                                     ['singular', 'plural', 'targets'])


def entries_target_group(root_directory, wrapper):
    group = TargetGroup(
        singular='entry',
        plural='entries',
        targets=[],
    )

    for path in sorted(root_directory.glob('entries/*.*')):
        group.targets.append(wrapper(path))

    return group


def pages_target_group(root_directory, wrapper):
    group = TargetGroup(
        singular='page',
        plural='pages',
        targets=[],
    )

    for path in sorted(root_directory.glob('pages/*.*')):
        group.targets.append(wrapper(path))

    return group
