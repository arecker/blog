import configparser
import os

from newsrc import files


class ConfigFileProblem(BaseException):
    """
    Something preventing BLOG from loading the config file.
    """


def load_config(config_path=files.join('blog.conf')):
    """
    Loads the program config from config_path
    """
    if not os.path.exists(config_path):
        raise ConfigFileProblem(
            f'cannot load config, {config_path} does not exist!')

    if not os.access(config_path, os.R_OK):
        raise ConfigFileProblem(
            f'cannot load config, {config_path} is not readable!')

    parser = configparser.ConfigParser()
    parser.read(config_path)
    return parser
