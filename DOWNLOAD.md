Dataset **CWFID** can be downloaded in Supervisely format:

 [Download](https://assets.supervise.ly/supervisely-supervisely-assets-public/teams_storage/N/M/hu/jnnPR4So6FMAxBE27XEu8UcGpq0k1f29lQlznwNzLgnWoCgKTPSrtW5rqNMhUC9ytyZwHjB2Q4GwOVDanhB2LGG6ZDuokTxAx7rmxf2f3uJlctCJ62kq7ThB0Ztb.tar)

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