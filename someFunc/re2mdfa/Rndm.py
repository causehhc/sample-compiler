import graphviz


def save_and_show(filename, string, end_node, start_node):
    file_dir = filename + '.dot'
    template = open('template.dot').read()
    for e in end_node:
        string += '%s [shape=doublecircle];' % e
    string += 'x [label= "start", shape=none,height=.0,width=.0];x -> {};'.format(start_node)
    string = template % string
    with open(file_dir, 'w') as f:
        f.write(string)
    f.close()
    dot = graphviz.Source(string)
    dot.render(filename, format='png')
    # dot.view(filename)


class Node_regex:
    def __init__(self, begin, end, type=None, sub=None, parts=None, text=None):
        self.begin = begin
        self.end = end
        self.type = type
        self.sub = sub
        self.parts = parts
        self.text = text

    def view(self, tab):
        if self:
            print("{}begin: {}".format('\t' * tab, self.begin))
            print("{}end: {}".format('\t' * tab, self.end))
            if self.type:
                print("{}type: {}".format('\t' * tab, self.type))
            if self.sub:
                print("{}sub: ".format('\t' * tab))
                self.sub.view(tab + 1)
            if self.parts:
                print("{}parts: ".format('\t' * tab))
                for item in self.parts:
                    item.view(tab + 1)
                    print()
            if self.text:
                print("{}text: {}".format('\t' * tab, self.text))


def parseRegex(text):
    def parseSub(text, begin, end, first):
        last = 0
        node = Node_regex(begin, end)
        stack = 0
        parts = []
        if len(text) == 0:
            return 'Error: empty input at ' + begin + '.'
        if first:
            i = 0
            while i <= len(text):
                if i == len(text) or (text[i] == '|' and stack == 0):
                    if last == 0 and i == len(text):
                        return parseSub(text, begin + last, begin + i, False)
                    sub = parseSub(text[last:i], begin + last, begin + i, True)
                    if isinstance(sub, str):
                        return sub
                    parts.append(sub)
                    last = i + 1
                elif text[i] == '(':
                    stack += 1
                elif text[i] == ')':
                    stack -= 1
                i += 1
            if len(parts) == 1:
                return parts[0]
            node.type = 'or'
            node.parts = parts
        else:
            i = 0
            while i < len(text):
                if text[i] == '(':
                    last = i + 1
                    i += 1
                    stack = 1
                    while i < len(text) and stack != 0:
                        if text[i] == '(':
                            stack += 1
                        elif text[i] == ')':
                            stack -= 1
                        i += 1
                    if stack != 0:
                        return 'Error: missing right bracket for ' + (begin + last) + '.'
                    i -= 1
                    sub = parseSub(text[last:i], begin + last, begin + i, True)
                    if isinstance(sub, str):
                        return sub
                    sub.begin -= 1
                    sub.end += 1
                    parts.append(sub)
                elif text[i] == '*':
                    if len(parts) == 0:
                        return 'Error: unexpected * at ' + (begin + i) + '.'
                    tempNode = Node_regex(parts[len(parts) - 1].begin,
                                          parts[len(parts) - 1].end + 1,
                                          type='star',
                                          sub=parts[len(parts) - 1])
                    parts[len(parts) - 1] = tempNode
                elif text[i] == '+':
                    if len(parts) == 0:
                        return 'Error: unexpected + at ' + (begin + i) + '.'
                    virNode = Node_regex(parts[len(parts) - 1].begin,
                                         parts[len(parts) - 1].end + 1,
                                         type='star',
                                         sub=parts[len(parts) - 1])
                    tempNode = Node_regex(parts[len(parts) - 1].begin,
                                          parts[len(parts) - 1].end + 1,
                                          type='cat',
                                          parts=[parts[len(parts) - 1], virNode])
                    parts[len(parts) - 1] = tempNode
                else:
                    tempNode = Node_regex(begin + i,
                                          begin + i + 1,
                                          type='text',
                                          text=text[i])
                    parts.append(tempNode)
                i += 1
            if len(parts) == 1:
                return parts[0]
            node.type = 'cat'
            node.parts = parts
        return node

    return parseSub(text, 0, len(text), True)


class Node_nfa:
    def __init__(self, type, edges, id):
        self.type = type
        self.edges = edges
        self.id = id
        self.__start = None
        self.__accept = []
        self.__dot_edge = ''

    def view(self):
        self.generateGraph(self, [])
        save_and_show('out/nfa', self.__dot_edge, self.__accept, self.__start)

    def generateGraph(self, node, exist_node):
        if node.type == 'start':
            self.__start = node.id
        if node.type == 'accept':
            self.__accept.append(node.id)
        if len(node.edges) == 0:
            return
        exist_node.append(node.id)
        for item in node.edges:
            flag = False
            if item[1].id not in exist_node:
                flag = True
            exist_node.append(item[1].id)
            temp = '\t{} -> {}[label={}];\n'.format(node.id, item[1].id, item[0])
            self.__dot_edge += temp
            if flag:
                self.generateGraph(item[1], exist_node)


def regexToNfa(text):
    def generateGraph(node_regex, start, end, count):
        if start.id is None:
            start.id = count
            count += 1
        if node_regex.type == 'text':
            start.edges.append([node_regex.text, end])
        elif node_regex.type == 'cat':
            last = start
            i = 0
            while i < len(node_regex.parts) - 1:
                temp = Node_nfa('', [], None)
                count = generateGraph(node_regex.parts[i], last, temp, count)
                last = temp
                i += 1
            count = generateGraph(node_regex.parts[len(node_regex.parts) - 1], last, end, count)
        elif node_regex.type == 'or':
            i = 0
            while i < len(node_regex.parts):
                tempStart = Node_nfa('', [], None)
                tempEnd = Node_nfa('', [['eps', end]], None)
                start.edges.append(['eps', tempStart])
                count = generateGraph(node_regex.parts[i], tempStart, tempEnd, count)
                i += 1
        elif node_regex.type == 'star':
            tempStart = Node_nfa('', [], None)
            tempEnd = Node_nfa('', [['eps', tempStart], ['eps', end]], None)
            start.edges.append(['eps', tempStart])
            start.edges.append(['eps', end])
            count = generateGraph(node_regex.sub, tempStart, tempEnd, count)
        if end.id is None:
            end.id = count
            count += 1
        return count

    ast = parseRegex(text)
    start = Node_nfa('start', [], None)
    accept = Node_nfa('accept', [], None)
    if isinstance(ast, str):
        return ast
    generateGraph(ast, start, accept, 0)
    return start


class Node_dfa:
    def __init__(self, key=None, items=None, symbols=None, type=None, edges=None, trans=None, id=None):
        self.key = key
        self.items = items
        self.symbols = symbols
        self.type = type
        self.edges = edges
        self.trans = trans
        self.id = id
        self.__start = 'A'
        self.__accept = []
        self.__dot_edge = ''

    def view(self):
        self.generateGraph(self, [])
        save_and_show('out/dfa', self.__dot_edge, self.__accept, self.__start)

    def generateGraph(self, node, exist_node):
        if node.type == 'accept':
            self.__accept.append(node.id)
        if len(node.edges) == 0:
            return
        exist_node.append(node.id)
        for item in node.edges:
            flag = False
            if item[1].id not in exist_node:
                flag = True
            exist_node.append(item[1].id)
            temp = '\t{} -> {}[label={}];\n'.format(node.id, item[1].id, item[0])
            self.__dot_edge += temp
            if flag:
                self.generateGraph(item[1], exist_node)


def nfaToDfa(nfa):
    def getClosure(nodes):
        closure = []
        stack = []
        symbols = []
        type = ''
        i = 0
        while i < len(nodes):
            stack.append(nodes[i])
            closure.append(nodes[i])
            if nodes[i].type == 'accept':
                type = 'accept'
            i += 1
        while len(stack) > 0:
            top = stack.pop()
            i = 0
            while i < len(top.edges):
                if top.edges[i][0] == 'eps':
                    if top.edges[i][1] not in closure:
                        stack.append(top.edges[i][1])
                        closure.append(top.edges[i][1])
                        if top.edges[i][1].type == 'accept':
                            type = 'accept'
                else:
                    if top.edges[i][0] not in symbols:
                        symbols.append(top.edges[i][0])
                i += 1
        closure.sort(key=lambda node: node.id)
        symbols.sort()
        key = ''
        for item in closure:
            key += ',{}'.format(item.id)
        key = key[1:len(key)]
        ans = Node_dfa(key=key,
                       items=closure,
                       symbols=symbols,
                       type=type,
                       edges=[],
                       trans={})
        return ans

    def getClosureMove(closure, symbol):
        nexts = []
        i = 0
        while i < len(closure.items):
            node = closure.items[i]
            j = 0
            while j < len(node.edges):
                if symbol == node.edges[j][0]:
                    if node.edges[j][1] not in nexts:
                        nexts.append(node.edges[j][1])
                j += 1
            i += 1
        return getClosure(nexts)

    def toAlphaCount(n):
        return chr(65 + n)

    first = getClosure([nfa])
    states = {}
    front = 0
    queue = [first]
    count = 0
    first.id = toAlphaCount(count)
    states[first.key] = first
    while front < len(queue):
        top = queue[front]
        front += 1
        i = 0
        while i < len(top.symbols):
            closure = getClosureMove(top, top.symbols[i])
            if closure.key not in states:
                count += 1
                closure.id = toAlphaCount(count)
                states[closure.key] = closure
                queue.append(closure)
            top.trans[top.symbols[i]] = states[closure.key]
            top.edges.append([top.symbols[i], states[closure.key]])
            i += 1
    return first


class Node_mdfa:
    def __init__(self, key=None, items=None, symbols=None, type=None, edges=None, trans=None, id=None):
        self.key = key
        self.items = items
        self.symbols = symbols
        self.type = type
        self.edges = edges
        self.trans = trans
        self.id = id
        self.__start = '1'
        self.__accept = []
        self.__dot_edge = ''

    def view(self):
        self.generateGraph(self, [])
        self.__dot_edge = self.__dot_edge.replace(',', '_')
        save_and_show('out/mdfa', self.__dot_edge, self.__accept, self.__start)

    def generateGraph(self, node, exist_node):
        if node.type == 'accept':
            self.__accept.append(node.id)
        if len(node.edges) == 0:
            return
        exist_node.append(node.id)
        for item in node.edges:
            flag = False
            if item[1].id not in exist_node:
                flag = True
            exist_node.append(item[1].id)
            temp = '\t{} -> {}[label={}];\n'.format(node.id, item[1].id, item[0])
            self.__dot_edge += temp
            if flag:
                self.generateGraph(item[1], exist_node)


def minDfa(dfa):
    def getReverseEdges(start):
        front = 0
        queue = [start]
        visited = {}
        symbols = {}
        idMap = {}
        revEdges = {}
        visited[start.id] = True
        while front < len(queue):
            top = queue[front]
            front += 1
            idMap[top.id] = top
            i = 0
            while i < len(top.symbols):
                symbol = top.symbols[i]
                if symbol not in symbols:
                    symbols[symbol] = True
                next = top.trans[symbol]
                if next.id not in revEdges:
                    revEdges[next.id] = {}
                if symbol not in revEdges[next.id]:
                    revEdges[next.id][symbol] = []
                revEdges[next.id][symbol].append(top.id)
                if next.id not in visited:
                    visited[next.id] = True
                    queue.append(next)
                i += 1
        return [list(symbols.keys()), idMap, revEdges]

    def hopcroft(symbols, idMap, revEdges):
        ids = list(idMap.keys())
        ids.sort()
        partitions = {}
        front = 0
        queue = []
        visited = {}
        group1 = []
        group2 = []
        i = 0
        while i < len(ids):
            if idMap[ids[i]].type == 'accept':
                group1.append(ids[i])
            else:
                group2.append(ids[i])
            i += 1
        key = ''
        for item in group1:
            key += ',{}'.format(item)
        key = key[1:len(key)]
        partitions[key] = group1
        queue.append(key)
        visited[key] = 0
        if len(group2) != 0:
            key = ''
            for item in group2:
                key += ',{}'.format(item)
            key = key[1:len(key)]
            partitions[key] = group2
            queue.append(key)
        while front < len(queue):
            top = queue[front]
            front += 1
            if top:
                top = top.split(',')
                i = 0
                while i < len(symbols):
                    symbol = symbols[i]
                    revGroup = {}
                    j = 0
                    while j < len(top):
                        if (top[j] in revEdges) and (symbol in revEdges[top[j]]):
                            k = 0
                            while k < len(revEdges[top[j]][symbol]):
                                revGroup[revEdges[top[j]][symbol][k]] = True
                                k += 1
                        j += 1
                    keys = list(partitions.keys())
                    j = 0
                    while j < len(keys):
                        key = keys[j]
                        group1 = []
                        group2 = []
                        k = 0
                        while k < len(partitions[key]):
                            if partitions[key][k] in revGroup:
                                group1.append(partitions[key][k])
                            else:
                                group2.append(partitions[key][k])
                            k += 1
                        if len(group1) != 0 and len(group2) != 0:
                            del partitions[key]
                            key1 = ''
                            for item in group1:
                                key1 += ',{}'.format(item)
                            key1 = key1[1:len(key1)]
                            key2 = ''
                            for item in group2:
                                key2 += ',{}'.format(item)
                            key2 = key2[1:len(key2)]
                            partitions[key1] = group1
                            partitions[key2] = group2
                            if key1 in visited:
                                queue[visited[key1]] = None
                                visited[key1] = len(queue)
                                queue.append(key1)
                                visited[key2] = len(queue)
                                queue.append(key2)
                            elif len(group1) <= len(group2):
                                visited[key1] = len(queue)
                                queue.append(key1)
                            else:
                                visited[key2] = len(queue)
                                queue.append(key2)
                        j += 1
                    i += 1
        return list(partitions.values())

    def buildMinNfa(start, partitions, idMap, revEdges):
        nodes = []
        group = {}
        edges = {}
        partitions.sort()
        i = 0
        while i < len(partitions):
            if start.id in partitions[i]:
                if i > 0:
                    partitions[i], partitions[0] = partitions[0], partitions[i]
                break
            i += 1
        i = 0
        while i < len(partitions):
            temp = ''
            for item in partitions[i]:
                temp += ',{}'.format(item)
            temp = temp[1:len(temp)]
            node = Node_mdfa(id=str(i + 1),
                             key=temp,
                             items=[],
                             symbols=[],
                             type=idMap[partitions[i][0]].type,
                             edges=[],
                             trans={})
            j = 0
            while j < len(partitions[i]):
                node.items.append(idMap[partitions[i][j]])
                group[partitions[i][j]] = i
                j += 1
            edges[i] = {}
            nodes.append(node)
            i += 1

        revEdges_keys = list(revEdges.keys())
        for to in revEdges_keys:
            revEdges_to_keys = list(revEdges[to].keys())
            for symbol in revEdges_to_keys:
                for from_i in revEdges[to][symbol]:
                    if group[to] not in edges[group[from_i]]:
                        edges[group[from_i]][group[to]] = {}
                    edges[group[from_i]][group[to]][symbol] = True

        edges_keys = list(edges.keys())
        for from_i in edges_keys:
            edges_from_keys = list(edges[from_i].keys())
            for to in edges_from_keys:
                symbol = list(edges[from_i][to].keys())
                symbol.sort()
                temp = ''
                for item in symbol:
                    temp += ',{}'.format(item)
                temp = temp[1:len(temp)]
                symbol = temp
                nodes[from_i].symbols.append(symbol)
                nodes[from_i].edges.append([symbol, nodes[to]])
                nodes[from_i].trans[symbol] = nodes[to]

        return nodes[0]

    edgesTuple = getReverseEdges(dfa)
    symbols = edgesTuple[0]
    idMap = edgesTuple[1]
    revEdges = edgesTuple[2]
    partitions = hopcroft(symbols, idMap, revEdges)
    return buildMinNfa(dfa, partitions, idMap, revEdges)


def anls(text):
    nfa = regexToNfa(text)
    nfa.view()
    dfa = nfaToDfa(nfa)
    dfa.view()
    mdfa = minDfa(dfa)
    mdfa.view()


def main():
    anls('aa|bbc*')


if __name__ == '__main__':
    main()
