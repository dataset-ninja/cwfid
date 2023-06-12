Dataset **CWFID** can be downloaded in Supervisely format:

 [Download](https://assets.supervise.ly/supervisely-supervisely-assets-public/teams_storage/q/V/tD/DkjDBIGvZwkFWBECl9HeLGb6CZBatBrf5Vb3dUwN6cx815WdUDJr0j4Sq5CNTWl43fxyBWInzMFxdrhy4Z3kML71TKjwqzl6xec6MfRmKTJpriMuOWDZ891my5bd.tar)

As an alternative, it can be downloaded with dataset-tools package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CWFID', dst_dir='~/dtools/datasets/CWFID.tar')
```
The data in original format can be 🔗 [downloaded here](https://github.com/cwfid/dataset/archive/refs/tags/v1.0.zip)