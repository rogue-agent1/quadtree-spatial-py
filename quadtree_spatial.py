#!/usr/bin/env python3
"""Quadtree for 2D spatial queries and collision detection."""
import sys, random

class Rect:
    def __init__(self, x, y, w, h): self.x=x; self.y=y; self.w=w; self.h=h
    def contains(self, px, py): return self.x<=px<self.x+self.w and self.y<=py<self.y+self.h
    def intersects(self, r):
        return not (r.x>self.x+self.w or r.x+r.w<self.x or r.y>self.y+self.h or r.y+r.h<self.y)

class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary; self.capacity = capacity
        self.points = []; self.divided = False; self.children = []
    def insert(self, px, py, data=None):
        if not self.boundary.contains(px, py): return False
        if len(self.points) < self.capacity:
            self.points.append((px, py, data)); return True
        if not self.divided: self._subdivide()
        for c in self.children:
            if c.insert(px, py, data): return True
        return False
    def _subdivide(self):
        b = self.boundary; hw, hh = b.w/2, b.h/2
        self.children = [QuadTree(Rect(b.x+dx, b.y+dy, hw, hh), self.capacity)
                         for dx, dy in [(0,0),(hw,0),(0,hh),(hw,hh)]]
        self.divided = True
    def query(self, rect):
        found = []
        if not self.boundary.intersects(rect): return found
        for px, py, data in self.points:
            if rect.contains(px, py): found.append((px, py, data))
        if self.divided:
            for c in self.children: found.extend(c.query(rect))
        return found

if __name__ == "__main__":
    qt = QuadTree(Rect(0, 0, 100, 100))
    random.seed(42)
    for i in range(50): qt.insert(random.uniform(0,100), random.uniform(0,100), f"p{i}")
    results = qt.query(Rect(20, 20, 30, 30))
    print(f"Points in (20,20)-(50,50): {len(results)}")
    for x, y, d in results[:5]: print(f"  ({x:.1f}, {y:.1f}) {d}")
