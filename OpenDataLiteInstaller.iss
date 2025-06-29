
[Setup]
AppName=OpenDataLite
AppVersion=1.0.0
AppPublisher=Keren Loáiciga Fallas y Viviana López Turcios
DefaultDirName={pf}\OpenDataLite
DefaultGroupName=OpenDataLite
OutputDir=C:\Users\keren\Desktop\Python\OpenDataLite v2
OutputBaseFilename=OpenDataLite_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "C:\Users\keren\Desktop\Python\OpenDataLite v2\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\OpenDataLite"; Filename: "{app}\OpenDataLite.exe"
Name: "{commondesktop}\OpenDataLite"; Filename: "{app}\OpenDataLite.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"

[Run]
Filename: "{app}\OpenDataLite.exe"; Description: "Iniciar OpenDataLite"; Flags: nowait postinstall skipifsilent

