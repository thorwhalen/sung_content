"""Code to access thorwhalen/sung_content data with ease

Note on requirements:
Minimum:   pip install graze
Optionally (for get_table function): pip install tabled

"""

org, repo, branch = 'thorwhalen/sung_content/main'.split('/')
DFLT_CONTENT_URL = (
    f'https://raw.githubusercontent.com/{org}/{repo}/{branch}' + '/{}'
).format  # function returning url of raw content from


def get_content_bytes(
    key, max_age=None, *, cache_locally=True, content_url=DFLT_CONTENT_URL
):
    """Get bytes of content from `thorwhalen/content`, automatically caching locally.

    ```
    # add max_age=1e-6 if you want to update the data with the remote data
    b = get_content_bytes('tables/csv/projects.csv', max_age=None)
    ```
    """
    url = content_url(key)

    if cache_locally:
        from graze import graze
        import os

        if isinstance(cache_locally, str):
            rootdir = cache_locally
            assert os.path.isdir(
                rootdir
            ), f"cache_locally: {rootdir} is not a directory"
            return graze(url, rootdir, max_age=max_age)
        return graze(url, max_age=max_age)
    else:
        import requests

        return requests.get(url).content


def get_table(
    key, max_age=None, *, content_url=DFLT_CONTENT_URL, **extra_decoder_kwargs
):
    from tabled import get_table as _get_table

    bytes_ = get_content_bytes(key, max_age=max_age, content_url=content_url)
    ext = key.split('.')[-1] if '.' in key else None
    return _get_table(bytes_, ext=ext, **extra_decoder_kwargs)
