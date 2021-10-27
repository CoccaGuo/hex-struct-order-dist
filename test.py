from main import Point

p = Point(1, 2)
plist = [Point(1, 3), Point(2, 3), Point(1, 2)]
print(p in plist)
p2 = Point(1, 2)
print(p ==p2)
print(p is p2)