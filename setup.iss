; Inno Setup Script for Overscoped Sandwich Simulator

[Setup]
AppId={{8B3F1D2A-4C5E-4B7D-9E1A-2F3B4C5D6E7F}
AppName=Overscoped Sandwich Simulator
AppVersion=1.0.0
AppPublisher=Dyvorn
DefaultDirName={autopf}\Overscoped Sandwich Simulator
DefaultGroupName=Overscoped Sandwich Simulator
AllowNoIcons=yes
LicenseFile=README.md
OutputDir=installer
OutputBaseFilename=Overscoped.Sandwich.Simulator.Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The main executable from the dist folder
Source: "dist\Overscoped Sandwich Simulator.exe"; DestDir: "{app}"; Flags: ignoreversion
; Bundling external assets (though PyInstaller bundles them, keeping them here ensures a fallback if using directory mode)
Source: "images\*"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "sounds\*"; DestDir: "{app}\sounds"; Flags: ignoreversion recursesubdirs createallsubdirs
; Initial empty data files
Source: "save_data.json"; DestDir: "{userappdata}\Overscoped Sandwich Simulator"; Flags: ignoreversion uninsneveruninstall
Source: "collectibles.json"; DestDir: "{userappdata}\Overscoped Sandwich Simulator"; Flags: ignoreversion uninsneveruninstall

[Icons]
Name: "{group}\Overscoped Sandwich Simulator"; Filename: "{app}\Overscoped Sandwich Simulator.exe"
Name: "{group}\{cm:UninstallProgram,Overscoped Sandwich Simulator}"; Filename: "{unindis}"
Name: "{autodesktop}\Overscoped Sandwich Simulator"; Filename: "{app}\Overscoped Sandwich Simulator.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Overscoped Sandwich Simulator.exe"; Description: "{cm:LaunchProgram,Overscoped Sandwich Simulator}"; Flags: nowait postinstall skipifsilent

[Code]
// Ensure the AppData directory exists on installation
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    ForceDirectories(ExpandConstant('{userappdata}\Overscoped Sandwich Simulator'));
  end;
end;
