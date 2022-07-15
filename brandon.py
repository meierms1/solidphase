import sys
print("Hello")
print(sys.argv)
OpenDatabase("localhost:"+sys.argv[1], 0)
AddPlot("Pseudocolor", "Temp", 1, 1)
DrawPlots()
