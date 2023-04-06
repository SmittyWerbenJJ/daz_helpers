

dsx = """\
<?xml version="1.0" encoding="UTF-8"?>
<ProductSupplement VERSION="0.1">
 <ProductName VALUE="{pname}"/>
 <ProductStoreIDX VALUE="{pidx}-{psubidx}"/>
 <UserOrderId VALUE="{orderid}"/>
 <UserOrderDate VALUE="{orderdate}"/>
 <InstallerDate VALUE="{installerdate}"/>
 <ProductFileGuid VALUE="{guid}"/>
 <InstallTypes VALUE="Content"/>
 <ProductTags VALUE="DAZStudio4_5"/>
</ProductSupplement>
"""
dsa="""\
// DAZ Studio version 4.10.0.123 filetype DAZ Script

if( App.version >= 67109158 ) //4.0.0.294
{
	var oFile = new DzFile( getScriptFileName() );
	var oAssetMgr = App.getAssetMgr();
	if( oAssetMgr )
	{
		oAssetMgr.queueDBMetaFile( oFile.baseName() );
	}
}
"""

manifest_header = """\
<DAZInstallManifest VERSION="0.1">
 <GlobalID VALUE="{}"/>"""
manifest_line = """ <File TARGET="Content" ACTION="Install" VALUE="{}"/>"""
manifest_footer = """</DAZInstallManifest>
"""

supplement = """\
<ProductSupplement VERSION="0.1">
 <ProductName VALUE="{}"/>
 <InstallTypes VALUE="Content"/>
 <ProductTags VALUE="DAZStudio4_5"/>
</ProductSupplement>
"""


def create_supplement(filelist:list[str]):
    lines=[]
