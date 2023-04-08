from pathlib import Path
import re
from io import StringIO

template="""\
<ProductSupplement VERSION="0.1">
    <ProductName VALUE="{}" />
    <InstallTypes VALUE="Content" />
    <ProductTags VALUE="DAZStudio4_5" />
</ProductSupplement>
"""

class Supplement:
    def __init__(self, productName: str) -> None:
        self.data=template.format(productName)

    def toString(self):
        return self.data
