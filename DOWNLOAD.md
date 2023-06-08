Dataset CWFID can be downloaded in Supervisely format:

[Download](https://assets.supervise.ly/supervisely-supervisely-assets-public/teams_storage/q/V/tD/DkjDBIGvZwkFWBECl9HeLGb6CZBatBrf5Vb3dUwN6cx815WdUDJr0j4Sq5CNTWl43fxyBWInzMFxdrhy4Z3kML71TKjwqzl6xec6MfRmKTJpriMuOWDZ891my5bd.tar)

or download with the following python code:
``` bash
pip install --upgrade dataset-tools
```

``` python
import dataset_tools as dtools

dtools.download(dataset=CWFID, dst_dir='~/datasets/CWFID'')```The data in original format can be [downloaded here](https://github.com/cwfid/dataset/releases)