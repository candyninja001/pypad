# convert does the bulk of the parsing work for skills.
# arguments is a dict with values of tuples or json values.
# tuples are structured (index, lambda) where index is 
# the raw data index or slice to put in the lambda function,
# which converts the raw data to a more usuable form.
# json values are constants
def convert(type_name: str, arguments: "{arg_name: (index or slice, lambda) or const_value}"):
    def f(raw_data):
        args = {}
        raw_data = defaultlist(int, raw_data)
               
        for name,t in arguments.items():
            if type(t) == tuple:
                index, funct = t[0], t[1]
                value = raw_data[index]
                args[name] = funct(value)
            else:
                args[name] = t
        return (type_name, args)
    return f


def unimplimented(type_id):
    return convert('unimplimented', {'type': type_id})


def gungho_csv(csv: str) -> [[str]]:
    stop_lead = ''
    result = []
    line = []
    start = 0
    end = 0
    while end < len(csv):
        if start == end:
            if csv[start] == "'":
                stop_lead = "'"
            else:
                stop_lead = ''
        if stop_lead == "'":
            if csv[end:end+2] == "',":
                line.append(csv[start:end+1])
                end += 2
                start = end
            elif csv[end:end+2] == "'\n":
                line.append(csv[start:end+1])
                result.append(line)
                line = []
                end += 2
                start = end
            else:
                end += 1
        else:
            if csv[end] == ',':
                line.append(csv[start:end])
                end += 1
                start = end
            elif csv[end] == '\n':
                line.append(csv[start:end])
                result.append(line)
                line = []
                end += 1
                start = end
            else:
                end += 1

    line.append(csv[start:end])
    result.append(line)
    return result


# base code from https://stackoverflow.com/a/8749640/8150086
class defaultlist(list):
    def __init__(self, fx, initial=[]):
        self._fx = fx
        self.extend(initial)
    def _fill(self, index):
        if type(index) == slice:
            if index.step == None or index.step > 0:
                if index.stop == None:
                    return
                while len(self) <= index.stop:
                    self.append(self._fx())
            else:
                if index.start == None:
                    return
                while len(self) <= index.start:
                    self.append(self._fx())
        else:
            while len(self) <= index:
                self.append(self._fx())
    def __setitem__(self, index, value):
        self._fill(index)
        list.__setitem__(self, index, value)
    def __getitem__(self, index):
        self._fill(index)
        if type(index) == slice:
            return defaultlist(self._fx, list.__getitem__(self, index))
        else:
            return list.__getitem__(self, index)


cc = lambda x: x
multiplier = lambda x: x/100
multiplier_with_default = lambda x: x/100 if x != 0 else 1.0
increase_multiplier = lambda x: (x + 100) /100
single_to_list = lambda x: [x]
collection_to_list = lambda x: list(x)
positive_values_to_list = lambda x: [i for i in x if i > 0]
binary_to_list = lambda x: [i for i,v in enumerate(str(bin(x))[:1:-1]) if v == '1']
list_of_binary_to_list = lambda x: [b for i in x for b in binary_to_list(i)]
hex_to_list = lambda h: [d for d,b in enumerate(str(bin(int(h, 16)))[:1:-1]) if b == '1']
all_attr = [1,2,3,4,5]
