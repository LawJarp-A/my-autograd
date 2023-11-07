# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['Value']

# %% ../nbs/00_core.ipynb 3
# This class stores the Scalar values that we will use that contain the backpropagation information
class Value:
    "This class stores the Scalar values that we will use that contain the backpropagation information"
    def __init__(self, data, _children=(), _op='', label=""):
        self.data = data
        self.grad = 0
        # The children are the values that were used to calculate this value
        self._children = _children
        # The op is the operation that was used to calculate this value
        self._op = _op
        # The backward function is the function that will be used to calculate the gradient
        self._backward = lambda: None
        self.label = label
    
    # Define how operators are used on the Value class

    # Addition
    def __add__(self, other):
        "Define how addition works on the Value class"
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        # Define the backward function
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        
        return out
    
    # Multiplication
    def __mul__(self, other):
        "Define how multiplication works on the Value class"
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        # Define the backward function
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        
        return out

    # Power
    def __pow__(self, other):
        "Define how power works on the Value class"
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        "Define how the ReLU function works on the Value class"
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out
    
    # The Backward function
    def backward(self):
        "Define the backward function"
        # Start with a gradient of 1
        self.grad = 1
        # Topological sort
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        
        # For each node in the topological sort from the end, run the backward function
        for v in reversed(topo):
            v._backward()
