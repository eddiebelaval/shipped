-- Creates a Mail.app DRAFT (never sends) for a Shipped. release.
-- Usage: osascript shipped-draft.applescript <sender> <subject> <body> <bccCommaList>
on run argv
	set theSender to item 1 of argv
	set theSubject to item 2 of argv
	set theBody to item 3 of argv
	set bccRaw to item 4 of argv

	-- split the comma-separated bcc list
	set AppleScript's text item delimiters to ","
	set bccItems to text items of bccRaw
	set AppleScript's text item delimiters to ""

	tell application "Mail"
		set newMsg to make new outgoing message with properties {subject:theSubject, content:theBody, sender:theSender, visible:false}
		tell newMsg
			repeat with addr in bccItems
				set a to addr as string
				if length of a > 0 then
					make new bcc recipient at end of bcc recipients with properties {address:a}
				end if
			end repeat
		end tell
		save newMsg
	end tell
	return "draft saved"
end run
