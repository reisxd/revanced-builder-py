class Configuration:
    def __init__(self):
        self.files = {
            'cli': '',
            'integrations': '',
            'patches': '',
            'patches-json': '',
            'microg': ''
        }

        self.patches = {
            'patches': [],
            'recommendedVersions': [],
            'packages': [],
            'includedPatches': []
        }

        self.apps = []

    def GetApps(self):
        return self.apps
    
    def SetApps(self, val):
        self.apps = val

    def GetFiles(self):
        return self.files

    def SetFiles(self, property, val):
        self.files[property] = val

    def GetPatches(self):
        return self.patches

    def SetPatches(self, property, val):
        self.patches[property] = val