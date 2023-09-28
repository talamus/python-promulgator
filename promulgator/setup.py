from .__imports import *


def get_content_files_to_be_published(paths: list[Path]) -> list[dict]:
    """### Seek files to be published

    Takes a list of misc paths. (Either markdown files, or whole directories.)

    Returns a list of dictionaries:
    ```
    {
        "content_file": "<name of a content file>",
        "content_path": "<location of the content file, relative to root_dir>",
        "root_dir": "<root_directory>",
        "config": "<full configuration for the content file>"
    }
    ```

    Throws `FileSeekingError` if something goes wrong.
    """
    content_files = {}  # (content_dir, content_file) -> (root_dir, root_config)

    for path in paths:
        content_dir, content_file = _split_to_dir_and_filename(path)
        root_dir, root_config = _seek_content_root(content_dir)

        if content_file is None:  # we have a directory:
            content_files.update(
                _seek_content_files(content_dir, (root_dir, root_config))
            )
        else:  # We have a single file:
            content_files = {(content_dir, content_file): (root_dir, root_config)}

    return _trim_paths_and_expand_configs(content_files)


def _split_to_dir_and_filename(content: Path) -> tuple[DirName, FileName]:
    """### Split user provided path into absolute dir and a filename

    If path is a directory, then the filename is `None`.

    Throws `FileSeekingError` if file is not a markdown file,
    or dir is not found.
    """
    content = os.path.abspath(content)

    if os.path.isfile(content):
        content_dir, content_file = os.path.split(content)

        # Sanity check:
        if not CONTENT_FILE_RE.search(content_file):
            raise FileSeekingError(f"{content} is not a markdown file")

    elif os.path.isdir(content):
        content_dir = content
        content_file = None

    else:
        raise FileSeekingError(f"{content} is not a file or directory")

    return (content_dir, content_file)


def _seek_content_root(content_dir: DirName) -> tuple[DirName, Config]:
    """### Try to find the content root directory and read the configuration

    Seek nearest parent directory that has a `.promulgator[.y[a]ml]` file.
    Read it, and return the `root_dir` and `root_config`.

    Throws `FileSeekingError` if no parent directory is found.
    """
    current_dir = os.path.abspath(content_dir)

    for limit in range(999):  # Better than `while True:`...
        for file in os.listdir(current_dir):
            if ROOT_CONFIG_FILE_RE.search(file):
                with open(os.path.join(current_dir, file)) as stream:
                    root_config = yaml.safe_load(stream)
                return (current_dir, root_config)

        (current_dir, previous_dir) = os.path.split(current_dir)

        if current_dir == previous_dir:
            break

    raise FileSeekingError(
        ".promulgator file was not found in " f"the parent directories of {content_dir}"
    )


def _seek_content_files(
    content_dir: DirName, payload: any
) -> list[tuple[DirName, FileName]]:
    """### Seek all content files from a directory and all of its subdirectories
    Returns a dictionary: `(content_dir, content_file) -> payload`
    """
    content_files = {}

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if CONTENT_FILE_RE.search(file):
                content_files[(root, file)] = payload

    return content_files


def _trim_paths_and_expand_configs(
    content_files: dict[tuple[DirName, FileName], tuple[DirName, Config]],
) -> list[dict]:
    """### Do the final pruning to the content file list

    Takes a dictionary: `(content_dir, content_file) -> (root_dir, root_config)`

    Builds (recursively and cumulatively) configuration for `content_dir`
    and trims `content_dir` to be relative to the `root_dir`.

    Returns a list of dictionaries:
    ```
    {
        "content_file": "<name of a content file>",
        "content_path": "<location of the content file, relative to root_dir>",
        "root_dir": "<root_directory>",
        "config": "<full configuration for the content file>"
    }
    ```
    """
    config_cache = {}  # absolute_dir -> configuration

    def get_config(absolute_dir, root_dir, root_config):
        """Return full configuration for `absolute_dir`."""
        nonlocal config_cache

        if absolute_dir in config_cache:
            return config_cache[absolute_dir]

        config = {}
        for file in os.listdir(absolute_dir):
            if METADATA_FILE_RE.search(file):
                with open(os.path.join(absolute_dir, file)) as stream:
                    config = yaml.safe_load(stream)

        if absolute_dir == root_dir:
            parent_config = root_config
        else:
            parent_config = get_config(
                os.path.split(absolute_dir)[0], root_dir, root_config
            )

        config_cache[absolute_dir] = parent_config | config
        return config_cache[absolute_dir]

    pruned_list = []
    for content, root in content_files.items():
        pruned_list.append(
            {
                "content_path": os.path.relpath(content[0], root[0]),
                "content_file": content[1],
                "root_dir": root[0],
                "config": get_config(content[0], *root),
            }
        )
    return pruned_list
