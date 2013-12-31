class Trie(object):
    trie_count = 0
    def __init__(self):
        Trie.trie_count += 1
        self._d = {}
    
    def add(self, word):
        if len(word) == 0:
            self._d['\0'] = None
            return
        if word[0] not in self._d:
            self._d[word[0]] = Trie()
        self._d[word[0]].add(word[1:])
    
    def __contains__(self, word):
        if not word:
            return True
        if word[0] in self._d:
            return self._d[word[0]].__contains__(word[1:])
        return False

    def find_prefix(self, prefix):
        if not prefix:
            return self
        c = prefix[0]
        if c in self._d:
            return self._d[c].find_prefix( prefix[1:] )
        return None

    def __str__(self):
        return self.pretty_str('')

    def pretty_str(self, prefix):
        indent = ' ' * len(prefix)
        s = ''
        for c in sorted(self._d.keys()):
            if c == '\0':
                s += indent + '* ' + prefix + '\n'
            else:
                s += indent + c + '\n'
                s += self._d[c].pretty_str(prefix + c)
        return s

    def items(self):
        return self._d.items()

    def keys(self):
        return self._d.keys()

    def allwords(self):
        l = []
        self._accumulate_terminals(l, '')
        return l

    def _accumulate_terminals(self, l, prefix):
        for c, subtrie in self._d.items():
            if c == '\0':
                l.append(prefix)
            else:
                subtrie._accumulate_terminals(l, prefix + c)

def load_wordlist(filename, min_word_length):
    """Word filename must be sorted, one word per line"""
    f = open(filename)
    s = f.read()
    words = s.split()
    
    maxlen = 0
    t = Trie()
    
    # Note that the words list is already sorted.
    last_word = None
    for word in words:
        if (last_word is None or not word.startswith(last_word)):
            if len(word) >= min_word_length:
                last_word = word
                t.add(word)
                maxlen = max(maxlen, len(word))

    #print "Total nodes:", Trie.trie_count
    #print "Longest word has {} chars".format(maxlen)
    return t
    
def minimax(trie, prefix, player_sign):
    INFINITY = 100000
    MAXLEN = 100

    if '\0' in trie.keys():
        # We found the end of a word, which means the other player already lost.
        # This is a win for us.
        score = player_sign * ( MAXLEN-len(prefix) ) # MAXLEN - length means shorter words are better.
        return score, ""

    moves = {}
    for c, subtrie in trie.items():
        score, best_suffix = minimax(subtrie, prefix + c, -1*player_sign)
        moves[c] = (score, best_suffix)

    for move, (score, suffix) in moves.items():
        winning_score = -INFINITY*player_sign
        if player_sign*score > player_sign*winning_score:
            winning_move = move
            winning_score = score
            winning_suffix = suffix
    return winning_score, winning_move + winning_suffix    


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: {} <prefix>\n".format( sys.argv[0] ))
        sys.stderr.write("Where <prefix> is the letters played so far.\n")
        sys.exit(1)

    # Load words into trie
    t = load_wordlist( 'WORD.LST', min_word_length=4 )    

    # Run minimax
    initial_prefix = sys.argv[1]
    next_player = (-1)**len(initial_prefix)
    score, suffix = minimax(t.find_prefix(initial_prefix), initial_prefix, next_player)

    # Who won?
    if score > 0:
        print "Player 2 loses:", initial_prefix + suffix
    else:
        print "Player 1 loses:", initial_prefix + suffix
    


