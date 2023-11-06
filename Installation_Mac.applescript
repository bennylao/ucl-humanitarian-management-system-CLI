tell application "Finder" to set currentDir to (target of front Finder window) as text
tell application "Terminal"
	do script "cd " & (quoted form of POSIX path of currentDir) & "; pip install ."
end tell