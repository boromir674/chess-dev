import json
import pandas
import numpy as np


class RoundTripEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Variation):
            return obj
        return super(RoundTripEncoder, self).default(obj)


class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return obj


class OpeningsDataset:
    _extractors = {'m': lambda x: x['m'].split(' '),
                    'len': lambda x: len(x['m'].split(' '))}
    _computed_fields = ['len']

    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls)
        x._df = pandas.DataFrame({field: [cls._extractors.get(field, lambda x: x[field])(variation_dict) for variation_dict in args[0]]
                                  for field in list(args[0][0].keys()) + cls._computed_fields})
        x._df = x._df.set_index('id')
        return x

    def __len__(self):
        return len(self._df)

    @property
    def most_analyzed(self):
        return self._df.loc[df['len'].idxmax()]

    @property
    def least_analyzed(self):
        return self._df.loc[df['len'].idxmin()]

    def to_json_string(self, human_redable=True):
        if human_redable:
            indent = 2
        else:
            indent = None
        return json.dumps(self, cls=RoundTripEncoder, indent=indent)

    def save_as_json(self, file_path, human_redable=True):
        if human_redable:
            indent = 2
        else:
            indent = None
        with open(file_path, 'w') as fp:
            json.dump(self, fp, cls=RoundTripEncoder, indent=indent)

    @classmethod
    def create_from_json(cls, file_path):
        with open(file_path, 'r') as fp:
            variations_list = json.load(fp, cls=RoundTripDecoder)
        return OpeningsDataset(variations_list)

class Variation:
    def __new__(cls, *args, **kwargs):
        x = super().__new__(cls)
        return x

if __name__ == '__main__':
    opd = OpeningsDataset.create_from_json('./openings.json')