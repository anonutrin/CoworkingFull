class GSheetAuthError(Exception):
    def __init__(self, message="Authentication Error"):
        self.message = message
        super().__init__(self.message)


class GSheetLoadError(Exception):
    def __init__(self, message="Sheet load error"):
        self.message = message
        super().__init__(self.message)


class GSheetExportError(Exception):
    def __init__(self, message="Export error"):
        self.message = message
        super().__init__(self.message)
