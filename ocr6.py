
import json
import os
from pathlib import Path
import datasets
from PIL import Image
import pandas as pd

logger = datasets.logging.get_logger(__name__)
_CITATION = """\
@article{Sun2021SpatialDG,
  title={Spatial Dual-Modality Graph Reasoning for Key Information Extraction},
  author={Hongbin Sun and Zhanghui Kuang and Xiaoyu Yue and Chenhao Lin and Wayne Zhang},
  journal={ArXiv},
  year={2021},
  volume={abs/2103.14470}
}
"""
_DESCRIPTION = """\
WildReceipt is a collection of receipts. It contains, for each photo, a list of OCRs - with the bounding box, text, and class. It contains 1765 photos, with 25 classes, and 50000 text boxes. The goal is to benchmark "key information extraction" - extracting key information from documents
https://arxiv.org/abs/2103.14470
"""

def load_image(image_path):
    image = Image.open(image_path)
    w, h = image.size
    return image, (w,h)

def normalize_bbox(bbox, size):
    return [
        int(1000 * bbox[0] / size[0]),
        int(1000 * bbox[1] / size[1]),
        int(1000 * bbox[2] / size[0]),
        int(1000 * bbox[3] / size[1]),
    ]


_URLS = ["https://download.openmmlab.com/mmocr/data/wildreceipt.tar"]

class DatasetConfig(datasets.BuilderConfig):
    """BuilderConfig for WildReceipt Dataset"""
    def __init__(self, **kwargs):
        """BuilderConfig for WildReceipt Dataset.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DatasetConfig, self).__init__(**kwargs)


class WildReceipt(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        DatasetConfig(name="WildReceipt", version=datasets.Version("1.0.0"), description="WildReceipt dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "words": datasets.Sequence(datasets.Value("string")),
                    "bboxes": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names = ['Ignore',  'Store_name_value', 'Store_name_key', 'Store_addr_value', 'Store_addr_key', 'Tel_value', 'Tel_key', 'Date_value', 'Date_key', 'Time_value', 'Time_key', 'Prod_item_value', 'Prod_item_key', 'Prod_quantity_value', 'Prod_quantity_key', 'Prod_price_value', 'Prod_price_key', 'Subtotal_value', 'Subtotal_key', 'Tax_value', 'Tax_key', 'Tips_value', 'Tips_key', 'Total_value', 'Total_key', 'Others']
                            )
                    ),
                    "image_path": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            citation=_CITATION,
            homepage="",
        )




    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        """Uses local files located with data_dir"""
        downloaded_file = dl_manager.download_and_extract(_URLS)
        dest = Path(downloaded_file[0])/'wildreceipt'

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": dest/"train.txt", "dest": dest}
            ),            
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": dest/"test.txt", "dest": dest}
            ),
        ]

    def _generate_examples(self, filepath, dest):

        df = pd.read_csv(dest/'class_list.txt', delimiter='\s', header=None)
        id2labels = dict(zip(df[0].tolist(), df[1].tolist()))


        logger.info("⏳ Generating examples from = %s", filepath)

        item_list = []
        with open(filepath, 'r') as f:
            for line in f:
                item_list.append(line.rstrip('\n\r'))
        
        for guid, fname in enumerate(item_list):

            data = json.loads(fname)
            image_path = dest/data['file_name']
            image, size = load_image(image_path)
            boxes = [[i['box'][6], i['box'][7], i['box'][2], i['box'][3]] for i in data['annotations']]

            text = [i['text'] for i in data['annotations']]
            label = [id2labels[i['label']] for i in data['annotations']]
            
            #print(boxes)
            #for i in boxes:
            #  print(i)
            boxes = [normalize_bbox(box, size) for box in boxes]
            
            flag=0
            #print(image_path)
            for i in boxes:
              #print(i)
              for j in i:
                if j>1000:
                  flag+=1
                  #print(j)
                  pass
            if flag>0: print(image_path)
            print("words", text)
            print("bboxes",boxes)
 
            yield guid, {"id": str(guid), "words": text, "bboxes": boxes, "ner_tags": label, "image_path": image_path}

