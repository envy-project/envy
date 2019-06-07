
# This hash function uniquely identifies this project (include path, etc. Remember, building a new image is trivial!)
def getConfigFileHash():
    return 'temp-config-hash'

def getNeededPackages():
    return ['nginx']

def getExtraExecutables():
    return ['/home/alex/creator.sh']

def getProjectBasePath():
    return '/home/alex/fakeproject'
