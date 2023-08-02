Dataset **CWFID** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/q/V/tD/DkjDBIGvZwkFWBECl9HeLGb6CZBatBrf5Vb3dUwN6cx815WdUDJr0j4Sq5CNTWl43fxyBWInzMFxdrhy4Z3kML71TKjwqzl6xec6MfRmKTJpriMuOWDZ891my5bd.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CWFID', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://github.com/cwfid/dataset/archive/refs/tags/v1.0.zip)