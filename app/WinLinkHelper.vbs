Dim linkname, target, workdir, args, arg_array
Dim WS, WinLink

linkname = Wscript.Arguments.Named("linkname")
target = Wscript.Arguments.Named("target")
workdir = Wscript.Arguments.Named("workdir")
args = Wscript.Arguments.Named("args")

If (linkname = "") Or (target = "") Then Wscript.Quit (1)
If workdir = "" Then workdir = Left(target, InStrRev(target, "\"))
If Not args = "" Then
	arg_array = Split(args, ",")
	args = ""
	For Each i In arg_array
		args = args + Chr(34) + i + Chr(34)
		args = args + " "
	Next
	End If
Set WS = CreateObject("Wscript.Shell")
linkname = WS.SpecialFolders("Desktop") + "\" + linkname + ".lnk"

Wscript.Echo ("正在创建快捷方式：'" + linkname + "' ===> '" + target + " " + args + "'")

Set WinLink = WS.CreateShortcut(linkname)
WinLink.TargetPath = target
WinLink.Arguments = args
WinLink.WorkingDirectory = workdir
WinLink.Save

Set WinLink = Nothing
Set WS = Nothing
Wscript.Quit (200)
