import collections
import shutil
import subprocess


def validate_image_dependenices():
    """Find the CLI tools needed for manipulating images."""

    required_commands = ('identify', 'convert')
    missing_commands = [
        c for c in required_commands if not bool(shutil.which(c))
    ]

    if missing_commands:
        raise EnvironmentError(f'cannot find commands: {missing_commands}')


ImageDimensions = collections.namedtuple('ImageDimensions',
                                         ['height', 'width'])


def read_image_dimensions(path) -> ImageDimensions:
    """Read dimensions of an image."""

    command = ['identify', '-format', '%wx%h', str(path)]
    result = subprocess.run(command, capture_output=True, check=True)
    width, height = result.stdout.decode('UTF-8').split('x')
    return ImageDimensions(height=int(height), width=int(width))
