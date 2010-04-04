/*
    Template script for movact-convert: a JavaScript movact frontend
    Copyright (C) 2009, 2010  Niels Serup

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
//  Maintained by Niels Serup <ns@metanohi.org>
/**********************************************************************/

function loadMovact() {
	meta = %s // JSON meta data from movact-convert goes here
	main = %s // JSON main data from movact-convert goes here
	
	// Create core elements
	wrapper = document.getElementById('wrapper')
	dyn = document.createElement('div')
	wrapper.appendChild(dyn)
	
	visitedParts = []
	partName = 'start'
	storyDone = false
	cookieJustSat = false
	
	if (autoload())
		start()
	else
		appendLinkingText(meta.title, 'start', start)
		// At this point the game will start when the user clicks on the element
}

function start() {
	header = document.createElement('h1')
	button_back = document.createElement('button')
	button_back.appendChild(createText(meta['back button']))
	button_back.onclick = function() {
		back()
	}
	button_reset = document.createElement('button')
	button_reset.appendChild(createText(meta['reset button']))
	button_reset.onclick = function() {
		reset()
	}
	
	// Remove stupid elements
	while (wrapper.childNodes.length > 1) {
		if (wrapper.firstChild != dyn)
			wrapper.removeChild(wrapper.firstChild)
	}
	
	// Insert smart elements
	wrapper.insertBefore(header, dyn)
	wrapper.insertBefore(button_back, dyn)
	wrapper.insertBefore(button_reset, dyn)
	wrapper.insertBefore(separator(), dyn)
	
	///////////\  /
	run() ////  \/
}

function separator() {
	return document.createElement('hr')
}

function popParts() {
	// Remove last element
	var vpn = []
	for (var i = 0; i < visitedParts.length-1; i++) {
		vpn[i] = visitedParts[i]
	}
	visitedParts = vpn
}

function back() {
	if (visitedParts.length > 1) {
		popParts()
		partName = visitedParts[visitedParts.length-1]
		popParts()
		run()
	}
}

function reset() {
	if (storyDone || confirm(meta['confirm-gui'])) {
		partName = visitedParts[0]
		visitedParts = []
		clearCookie()
		cookieJustSat = true
		run()
	}
}

function removeChilds(elem) {
	while (dyn.childNodes.length > 0) {
		dyn.removeChild(dyn.firstChild)
	}
}

function createParagraph() {
	return document.createElement('p')
}

function createText(text) {
	return document.createTextNode(text)
}

function appendStaticText(text) {
	var elem = createParagraph()
	elem.innerHTML = text
	dyn.appendChild(elem)
}

function appendLinkingText(text, reference, func) {
	var elem = createParagraph()
	var span = document.createElement('span')
	span.reference = reference
	if (func == undefined)
		var func = goTo
	span.onclick = function() {
		func(this.reference)
	}
	elem.appendChild(span)
	span.innerHTML = text
	dyn.appendChild(elem)
}

function goTo(part_name) {
	partName = part_name
	run()
}

function run() {
	var part, refsNum, text, i, p
	removeChilds()
	part = main[partName]
	
	text = meta.title + ' ["' + partName + '"] (' + visitedParts.length + ')'
	header.innerHTML = text
	document.title = text
	
	refsNum = 0
	text = ''
	for (var i = 1; i < part.length; i++) {
		x = part[i]
		if (x[0]) {
			var txt = x[1]
			if (txt == '')
				txt = '&nbsp;'
			appendStaticText(txt)
		}
		else {
			p = self.meta.points[refsNum]
			appendLinkingText(p[0] + x[2], x[1])
			refsNum += 1
		}
	}
	
	storyDone = false
	if (!part[0]) {
		dyn.appendChild(separator())
		appendStaticText(meta.end)
		storyDone = true
	}
	
	if (visitedParts.length == 0) {
		button_back.disabled = 'disabled'
		button_reset.disabled = 'disabled'
	}
	else {
		button_back.disabled = ''
		button_reset.disabled = ''
	}
	
	visitedParts[visitedParts.length] = partName
	if (!cookieJustSat)
		autosave()
	else
		cookieJustSat = false
}

function setCookie(value, ms) {
	try {
		if (ms == undefined)
			var ms = 63936000000 // In 740 days (a little over 2 years)
		var date = new Date()
		date.setTime(date.getTime()+ms)
		date = date.toGMTString()
		document.cookie = "movact_auto_save="+value+"; expires="+date+"; path=/"
	} catch (e) {}
}

function clearCookie() {
	setCookie('', -1468800000) // Deleted 17 days ago
}

function getCookie() {
	try {
		var name = "movact_auto_save="
		var spl = document.cookie.split(';')
		for (var i = 0; i < spl.length; i++) {
			var current = spl[i]
			while (current.charAt(0) == ' ')
				current = current.substring(1)
			if (current.indexOf(name) == 0)
				return current.substring(name.length)
		}
		// Else:
		return false
	} catch (e) {
		return false
	}
}

function autoload() {
	var savedata = unescape(getCookie())
	if (savedata) {
		try {
			eval("var vp = " + savedata)
			var pn = vp[vp.length-1]
			if (main[pn] == undefined)
				return
			
			visitedParts = vp
			partName = pn
			popParts()
			return true
		}
		catch(e) {
			
		}
	}
	// Else:
	return false
}

function autosave() {
	// Transform visitedParts into a string that can be eval'd when loading it
	var arrStr, tStr
	arrStr = ''
	for (x in visitedParts) {
		tStr = visitedParts[x]
		tStr = tStr.replace(/\'/g, "\\\\'")
		arrStr += ",'" + tStr + "'"
	}
	arrStr = '[' + arrStr.substring(1) + ']'
	setCookie(escape(arrStr))
}

////////////////////////////////////////////////////////////////////////
// Initialize data and start function chain
window.onload = function() {
	loadMovact()
}
