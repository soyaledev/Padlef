; Script de instalación para Padlef usando Inno Setup
; Para compilar: Abre este archivo en Inno Setup Compiler y presiona F9

[Setup]
AppName=Padlef
AppVersion=1.0.0
AppPublisher=Padlef
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
DefaultDirName={autopf}\Padlef
DefaultGroupName=Padlef
AllowNoIcons=yes
LicenseFile=
OutputDir=installer
OutputBaseFilename=Padlef-Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\mdPdf.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*.dll"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Padlef"; Filename: "{app}\mdPdf.exe"
Name: "{group}\{cm:UninstallProgram,Padlef}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Padlef"; Filename: "{app}\mdPdf.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Padlef"; Filename: "{app}\mdPdf.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\mdPdf.exe"; Description: "{cm:LaunchProgram,Padlef}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'Bienvenido al instalador de Padlef';
  WizardForm.WelcomeLabel2.Caption := 'Padlef - Conversor de Archivos a PDF' + #13#10 + #13#10 +
    'Convierte archivos Markdown, texto y código fuente a PDF con resaltado de sintaxis.' + #13#10 + #13#10 +
    'Formatos soportados:' + #13#10 +
    '• Markdown (.md)' + #13#10 +
    '• Texto (.txt)' + #13#10 +
    '• Código fuente (.js, .jsx, .py, .java, .c, .cpp, .html, .css, etc.)';
end;

