# Visit 3.1.4 log file
ScriptVersion = "3.1.4"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
ShowAllWindows()
OpenDatabase("localhost:/home/mmeierdo/SolidPhase/output06/02400cell/Header", 0)
# The UpdateDBPluginInfo RPC is not supported in the VisIt module so it will not be logged.
AddPlot("Pseudocolor", "Temp", 1, 1)
DrawPlots()
