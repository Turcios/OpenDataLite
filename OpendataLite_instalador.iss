[Setup]
AppName=OpenDataLite
AppVersion=2.0
DefaultDirName={pf}\OpenDataLite
DefaultGroupName=OpenDataLite
OutputBaseFilename=OpenDataLite_Instalador
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\OpenDataLite.exe
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\OpenDataLite.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\OpenDataLite"; Filename: "{app}\OpenDataLite.exe"; IconFilename: "{app}\OpenDataLite.exe"
Name: "{commondesktop}\OpenDataLite"; Filename: "{app}\OpenDataLite.exe"; IconFilename: "{app}\OpenDataLite.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Opciones adicionales:"
