from __future__ import annotations

from collections import deque

class TrieNode:

    __slots__ = ('parent', 'childs', 'symbol', 'is_end')

    def __init__(self, parent: TrieNode | None = None, childs: dict[str, TrieNode] | None = None, symbol: str = ""):
        self.parent = parent 
        self.childs = childs if childs else {}
        self.symbol = symbol
        self.is_end = False

    def search(self, s: deque[str] | str) -> bool:
        curr = self
        for sym in s:
            ch = curr.childs.get(sym, None)
            if ch is None:
                return False
            curr = ch
        return curr.is_end
    
    def add(self, s: str | deque[str]) -> None:
        if isinstance(s, str):
            s = deque(s)

        curr = self
        for sym in s:
            if sym not in curr.childs:
                curr.childs[sym] = TrieNode(parent=curr, symbol=sym)
            curr = curr.childs[sym]
        curr.is_end = True

    def __repr__(self) -> str:
        return f"Trienode: {self.symbol}"
