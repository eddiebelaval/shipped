-- Creates a Mail.app message for a Shipped. release: a DRAFT, or SENT when mode is "send".
-- Usage: osascript shipped-draft.applescript <sender> <subject> <body> <bccCommaList> [draft|send]
-- send_mode "send" enabled by Eddie 2026-10-11 ("yes switch them to send"): editions were sitting
-- unsent in Drafts because nothing told him a draft was waiting.
on run argv
	set theSender to item 1 of argv
	set theSubject to item 2 of argv
	set theBody to item 3 of argv
	set bccRaw to item 4 of argv
	set theMode to "draft"
	if (count of argv) > 4 then set theMode to item 5 of argv

	-- split the comma-separated bcc list
	set AppleScript's text item delimiters to ","
	set bccItems to text items of bccRaw
	set AppleScript's text item delimiters to ""

	tell application "Mail"
		set newMsg to make new outgoing message with properties {subject:theSubject, content:theBody, sender:theSender, visible:false}
		tell newMsg
			-- To: the sender's own address, so a BCC-only send is never refused; readers stay on BCC.
			if theMode is "send" then make new to recipient at end of to recipients with properties {address:theSender}
			repeat with addr in bccItems
				set a to addr as string
				if length of a > 0 then
					make new bcc recipient at end of bcc recipients with properties {address:a}
				end if
			end repeat
		end tell
		if theMode is "send" then
			send newMsg
			return "sent"
		else
			save newMsg
			return "draft saved"
		end if
	end tell
end run
