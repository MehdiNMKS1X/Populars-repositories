import csv
import math 

class Mushroom:
    def __init__(self, edible: bool):
        self.edible = edible
        self.attribute = {}
        
    def is_edible(self) -> bool:
        return self.edible
    
    def add_attribute(self, name: str, value: str) -> None:
        self.attribute[name] = value
    
    def get_attribute(self, name: str) -> str:
        return self.attribute.get(name, None)
    
def load_dataset(path: str) -> list[Mushroom]:
    mushrooms = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        first_line = True
        for row in reader:
            if first_line:
                attributes = row
                first_line = False
            else:
                mush = Mushroom(row[0] == 'Yes') # si est comestible
                for i in range(1, len(row)):
                    mush.add_attribute(attributes[i], row[i])
                mushrooms.append(mush)
    print(mushrooms[0].is_edible(), "looooongeuuuur" , len(mushrooms))
    return mushrooms

class Node:
    def __init__(self, criterion: str, is_leaf: bool=False):
        self.criterion_ = criterion
        self.is_leaf = is_leaf
        self.edges_ = []
        
    def is_leaf(self) -> bool:
       return self.is_leaf
    
    def add_edge(self, label: str, child: 'Node') -> bool:
        self.edges.append((child, label))
    
class Edge:
    def __init__(self, parent: Node, child: Node, label: str): 
        self.parent_ = parent
        self.child_ = child
        self.label_ = label
    
def entropy(mushrooms: list[Mushroom]) -> float:
   edible_count = sum(1 for mushroom in mushrooms if list(str(mushrooms == 'edible')))
   total_edible = len(mushrooms)
   
   py = edible_count / total_edible
   if py == 0 or py == 1:
       return 0
   return -py * math.log2(py) -(1 - py) * math.log2(1 - py)
   
def gain_entropy(mushrooms: list[Mushroom]) -> tuple[str, float]:
    entropy_value = entropy(mushrooms)
    total_count = len(mushrooms)
    mush = defaultdict(list)
    
    for mushroom in mushrooms:
        mush[mushroom.attributes[attribute]].append(mushroom)
        
        weight_entropy = 0
        for subset in mush.values():
            subset_entropy = entropy(subset)
            weight_entropy += len(subset) / total_count * subsest_entropy
        
        return entropy_value  - weight_entropy

    
def build_decision_tree(mushrooms: list):
    
    """
    Build a decision tree from the dataset.
    :param mushrooms: List of Mushroom objects.
    :return: Root node of the decision tree.
    """
    
    root = Node(None)
    best_criterion = None
    best_gain = 0
    attributes = list(mushrooms[0].attribute.keys())

    for attribute in attributes:
        gain = entropy(mushrooms)
        values = set([mushroom.get_attribute(attribute) for mushroom in mushrooms])
        for value in values:
            subset = [mushroom for mushroom in mushrooms if mushroom.get_attribute(attribute) == value]
            gain -= len(subset) / len(mushrooms) * entropy(subset)
        if gain > best_gain:
            best_gain = gain
            best_criterion = attribute
            
    if best_criterion is None:
        return root
    
    root.criterion_ = best_criterion
    values = set([mushroom.get_attribute(best_criterion) for mushroom in mushrooms])
    for value in values:
        subset = [mushroom for mushroom in mushrooms if mushroom.get_attribute(best_criterion) == value]
        if entropy(subset) == 0:
            child = Node('Yes', is_leaf=False) if subset[0].is_edible() else Node('No', is_leaf=True)
        else:
            child = build_decision_tree(subset)
        root.add_edge(value, child)
    print(f"First criterion: {best_criterion}")
    return root

def is_edible(root: Node, mushrooms: Mushroom) -> str:
    tree = build_decision_tree(mushrooms=[mushrooms])
    nextnode = root
    if not nextnode is mushrooms:
        return False
    node = nextnode
    return nextnode.criterion_ == 'Yes'                                                                   