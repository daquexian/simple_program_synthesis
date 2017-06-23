import sys, abc, re
from itertools import product
from functools import reduce


class Dag(object):
    def __init__(self, n, n1, n2, edges=None, w=None):
        self.n = n
        self.source = n1
        self.dest = n2
        self.edges = edges
        self.w = w

    def __str__(self):
        return str(self.w)

    def __repr__(self):
        return self.__str__()

    def get_path(self):
        # type: () -> list
        ret = []
        for edge in self.edges:
            if not any(edge.a):
                path = [edge]
                res = self.__get_path(path)
                if res:
                    ret.append(path)
        return ret

    def __get_path(self, path):
        last_edge = path[-1]
        if last_edge.b == self.dest:
            return True
        for edge in self.edges:
            if edge.a == last_edge.b:
                path.append(edge)
                if self.__get_path(path):
                    return True
                path.pop(-1)
        return False


class Edge(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __hash__(self):
        return 31 * hash(self.a) + hash(self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __cmp__(self, other):
        if self.a == other.a and self.b == other.b:
            return 0
        if self.a < other.a or (self.a == self.a and self.b < other.b):
            return -1
        return 1

    def __repr__(self):
        return "<Edge: " + str(self.a) + ", " + str(self.b) + ">"

    def __str__(self):
        return self.__repr__()


class Token(object):
    __metaclass__ = abc.ABCMeta

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    @abc.abstractmethod
    def reg_str(self):
        return


class StartToken(Token):
    def __init__(self):
        super(StartToken, self).__init__()

    def __repr__(self):
        return "StartToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"^"


class EndToken(Token):
    def __init__(self):
        super(EndToken, self).__init__()

    def __repr__(self):
        return "EndToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"$"


class AlphaToken(Token):
    def __init__(self):
        super(AlphaToken, self).__init__()

    def __repr__(self):
        return "AlphaToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"(?<![A-Za-z])[A-Za-z]+(?![A-Za-z])"

class NumToken(Token):
    def __init__(self):
        super(NumToken, self).__init__()

    def __repr__(self):
        return "NumToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"(?<!\d)\d+(?!\d)"


class SpaceToken(Token):
    def __init__(self):
        super(SpaceToken, self).__init__()

    def __repr__(self):
        return "SpaceToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"(?<! ) +(?! )"


class UpperToken(Token):
    def __init__(self):
        super(UpperToken, self).__init__()

    def __repr__(self):
        return "UpperToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"(?<![A-Z])[A-Z]+(?![A-Z])"


class LowerToken(Token):
    def __init__(self):
        super(LowerToken, self).__init__()

    def __repr__(self):
        return "LowerToken"

    def __str__(self):
        return self.__repr__()

    def reg_str(self):
        return r"(?<![a-z])[a-z]+(?![a-z])"


class Node(object):
    def __init__(self):
        pass


class Expression(object):
    def __init__(self):
        pass


class Substr(Expression):
    def __init__(self, p1, p2):
        super(Substr, self).__init__()
        self.vi = 0
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return "<Substr: " + str(self.p1) + ", " + str(self.p2) + ">"

    def __str__(self):
        return self.__repr__()


class ConstStr(Expression):
    def __init__(self, s):
        super(ConstStr, self).__init__()
        self.s = s

    def __eq__(self, other):
        return self.s == other.s

    def __hash__(self):
        return hash(self.s)

    def __cmp__(self, other):
        return self.s.__cmp__(other.s)

    def __repr__(self):
        return "<ConstStr: " + str(self.s) + ">"

    def __str__(self):
        return self.__repr__()


class Loop(Expression):
    def __init__(self, exp):
        super(Loop, self).__init__()
        self.exp = exp

    def __eq__(self, other):
        return self.exp == other.exp

    def __hash__(self):
        return hash(self.exp)


class CPos(object):
    def __init__(self, pos):
        self.pos = pos

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)

    def __cmp__(self, other):
        return self.pos.__cmp__(other.pos)

    def __repr__(self):
        return "<CPos: " + str(self.pos) + ">"

    def __str__(self):
        return self.__repr__()

    def match(self, str):
        if self.pos < 0:
            return len(str) + self.pos + 1
        return self.pos


class Pos(object):
    def __init__(self, reg_list1, reg_list2, c=set()):
        self.reg_list1, self.reg_list2 = reg_list1, reg_list2
        self.c = c

    def __repr__(self):
        return "<Pos: " + str(self.reg_list1) + str(self.reg_list2) + str(self.c) + ">"

    def __str__(self):
        return self.__repr__()

    def match(self, string):
        tokens1 = tuple((item[0] for item in self.reg_list1))
        tokens2 = tuple((item[0] for item in self.reg_list2))

        matches = []
        for i in range(len(string)):
            if match_start(string[i:], tokens2)[0] and match_end(string[:i], tokens1)[0]:
                matches.append(i)

        if len(matches) == 0:
            return None
        return matches[next(iter(self.c))]


def intersect_pos(pos_set1, pos_set2):
    res = set()

    for op1 in pos_set1:
        for op2 in pos_set2:
            if isinstance(op1, CPos) and isinstance(op2, CPos):
                if op1 == op2:
                    res.add(CPos(op1.pos))
            elif isinstance(op1, Pos) and isinstance(op2, Pos):
                rl1 = intersect_regex(op1.reg_list1, op2.reg_list1)
                rl2 = intersect_regex(op1.reg_list2, op2.reg_list2)
                c = op1.c.intersection(op2.c)
                if rl1 is not None and rl2 is not None and len(c) > 0:
                    res.add(Pos(rl1,
                                rl2,
                                c))

    return res


def intersect_regex(rl1, rl2):
    res = None

    if len(rl1) == len(rl2):
        res = [tuple(set(rl1[i]) & set(rl2[i])) for i in range(len(rl1))]

        for item in res:
            if len(item) == 0:
                return None

    return res


def intersect(op1, op2):
    res = None

    if isinstance(op1, Dag) and isinstance(op2, Dag):
        res = Dag(list(product(op1.n, op2.n)), op1.source + op2.source, op1.dest + op2.dest)
        res.edges = list((Edge(edge1.a + edge2.a, edge1.b + edge2.b) for
                          edge1, edge2 in product(op1.edges, op2.edges)))
        res.w = {Edge(edge1.a + edge2.a, edge1.b + edge2.b): set(
            filter(lambda x: x is not None, (intersect(f1, f2) for f1 in op1.w[edge1] for f2 in op2.w[edge2])))
            for edge1, edge2 in product(op1.edges, op2.edges)}
        res.w = {k: v for k, v in res.w.items() if len(v) > 0}
        res.edges = res.w.keys()

    elif isinstance(op1, Substr) and isinstance(op2, Substr):
        if op1.vi == op2.vi:
            p1 = intersect_pos(op1.p1, op2.p1)
            p2 = intersect_pos(op1.p2, op2.p2)
            if len(p1) > 0 and len(p2) > 0:
                res = Substr(p1, p2)
    elif isinstance(op1, ConstStr) and isinstance(op2, ConstStr):
        if op1 == op2:
            res = op1
    elif isinstance(op1, Loop) and isinstance(op2, Loop):
        res = Loop(intersect(op1.exp, op2.exp))

    return res


def generate_str(sigma, s):
    n = list(range(len(s) + 1))
    source = (0,)
    dest = (len(s),)
    edges = list((Edge((x[0],), (x[1],)) for x in filter(lambda x: x[0] < x[1], product(n, n))))
    W = {}
    for edge in edges:
        w = {ConstStr(s[edge.a[0]: edge.b[0]])}
        w = w.union(generate_substring(sigma, s[edge.a[0]: edge.b[0]]))
        W[edge] = w
    W = generate_loop(sigma, s, W)
    return Dag(n, source, dest, edges, W)


def intersect_list(l1, l2):
    # type: (list, list) -> list
    return list(set(l1) & set(l2))


def generate_partition(T):
    # type: (set) -> set
    res = None
    for item1 in T:
        for item2 in T:
            pass


def generate_loop(sigma, s, W):
    # type: (list(str), str, dict) -> dict
    return W


def generate_substring(sigma, substr):
    # type: (list(str), str) -> set
    res = set()

    for string in sigma:
        begin = 0
        while True:
            begin = string.find(substr, begin)
            if begin == -1:
                break

            Y1 = generate_position(string, begin)
            Y2 = generate_position(string, begin + len(substr))

            begin += 1

            res.add(Substr(Y1, Y2))

    return res


def generate_position(s, k):
    res = {CPos(k), CPos(-(len(s) - k + 1))}

    reps = (t[0] for t in calculate_iparts(s))

    n = 1
    rl1 = []
    rl2 = []
    pos1 = []
    pos2 = []
    while True:
        matched = False
        temp_rl = tuple(product(*((reps,) * n)))
        for r in temp_rl:
            match_res = match_end(s[:k], r)
            if match_res[0]:
                matched = True
                rl1.append(r)
                pos1.append(match_res[1])

            match_res = match_start(s[k:], r)
            if match_res[0]:
                matched = True
                rl2.append(r)
                pos2.append(k + match_res[2])

        n += 1

        if not matched:
            break

    for x, y in product(range(len(rl1)), range(len(rl2))):
        rl = rl1[x] + rl2[y]
        match_res = match(s, rl)

        for i, res_item in enumerate(match_res):
            if res_item[1] == pos1[x] and res_item[2] == pos2[y]:
                r1 = generate_regex(rl1[x], s)
                r2 = generate_regex(rl2[y], s)
                # res.add(Pos(r1, r2, {i, -(len(match_res) - i + 1)}))
                res.add(Pos(r1, r2, {i, -(len(match_res) - i)}))

    return res


def generate_regex(r, s):
    global iparts

    res = []

    for token in r:
        for ipart in iparts[s]:
            if token in ipart:
                res.append(ipart)

    return res


def get_reg_str(token_list):
    reg_str = ""
    for item in token_list:
        '''
        if isinstance(item, StartToken):
            reg_str += r"^"
        elif isinstance(item, AlphaToken):
            reg_str += r"(?<![A-Za-z])[A-Za-z]+(?![A-Za-z])"
        elif isinstance(item, NumToken):
            reg_str += r"(?<!\d)\d+(?!\d)"
        elif isinstance(item, EndToken):
            reg_str += r"$"
        elif isinstance(item, SpaceToken):
            reg_str += r"(?<! ) +(?! )"
            '''
        reg_str += item.reg_str()

    return reg_str


def match(s, reg):
    reg_str = get_reg_str(reg)

    return list(((m.group(0), m.start(), m.end()) for m in re.finditer(reg_str, s)))


def match_start(s, token_list):
    reg_str = get_reg_str(token_list)

    m = re.match(reg_str, s)

    res = []
    if m is not None:
        res.append(True)
        res.append(m.start())
        res.append(m.end())
    else:
        res.append(False)

    return res


def match_end(s, token_list):
    reg_str = get_reg_str(token_list) + r"$"

    m = re.search(reg_str, s)

    res = []
    if m is not None:
        res.append(True)
        res.append(m.start())
        res.append(m.end())
    else:
        res.append(False)

    return res


def calculate_iparts(s):
    return (NumToken(),), (AlphaToken(),), (StartToken(),), (EndToken(),), (SpaceToken(),), (UpperToken(),), (LowerToken(),)


def apply_path(operations, string):
    # type: (list, str) -> str
    res = ''
    for op in operations:
        if isinstance(op, Substr):
            p1 = next(iter(op.p1))
            p2 = next(iter(op.p2))
            ind1 = p1.match(string)
            ind2 = p2.match(string)

            if ind1 is None or ind2 is None:
                return None

            res = res + string[ind1: ind2]

    return res

if __name__ == "__main__":
    i = 0
    iparts = dict()
    dag = None
    while True:
        l = sys.stdin.readline().strip()
        if l == '':
            break
        long_str, sub_str = l.split(",")
        iparts[long_str] = calculate_iparts(long_str)
        this_dag = generate_str((long_str,), sub_str)
        if dag is None:
            dag = this_dag
        else:
            dag = intersect(dag, this_dag)

    paths = dag.get_path()
    if len(paths) > 0:
        # path = min(paths, key=len)
        paths = sorted(paths, key=len)
        for path in paths:
            edges = [next(iter(dag.w[k])) for k in path]
            print(edges)

        while True:
            long_str = sys.stdin.readline()
            for path in paths:
                edges = [next(iter(dag.w[k])) for k in path]
                res = apply_path(edges, long_str)
                if res is not None:
                    print(res)
                    break
            else:
                print("Can't handle it")

    else:
        print("Can't handle it")

