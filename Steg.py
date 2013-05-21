import Image

def write_image(in_path,s,out_path='mystery'):
	"""
	Writes a binary string into a .png image.

	Args:
	in_path - string containing the path of the input image.
	s - the binary string to be written.
	out_path (default='mystery') - string containing the name of the output image


	"""

	try:
		image=Image.open(in_path)
	except IOError as e :
		print "<Steg> " + e.strerror
		return

	width,height = image.size

	if len(s) <= width * height * 3 :
		i = 0
		s = s + '0'*((3-len(s)%3)%3)
		
		while i < len(s) :
			x,y = ((i/3)%width,(i/3)/width)
			r,g,b = image.getpixel( (x,y) )
			r = int(bin(r)[:-1]+s[i],2)
			g = int(bin(g)[:-1]+s[i+1],2)
			b = int(bin(b)[:-1]+s[i+2],2)
			image.putpixel((x,y),(r,g,b))
			i += 3
				
	else : print "<Steg> Image too small / Message too long"

	image.save(out_path + '.png')


def read_image(in_path) :
	"""
	Reads the 'message' written into the less significant bits of the pixels RGB channels of a png image. 
	Takes a string containing the path of the image, returns a binary string.

	Args:
	in_path - the string containing the path of the image.


	"""
	try:
		image=Image.open(in_path)
	except IOError as e :
		print "<Steg> " + e.strerror
		return

	width,height = image.size
	out = ""

	for y in range(height) :
		for x in range(width) :
			r,g,b = image.getpixel( (x,y) )
			out = out + bin(r)[-1] + bin(g)[-1] + bin(b)[-1]


	return out

def encode(s) :
	"""
	Encodes a binary string, prefixing the bit-stuffed size and a delimiter.

	Args:
	s - the input binary string.


	"""
	bin_length = bin(len(s))[2:]
	return stuff(bin_length)+'10000'+s

def decode(s) :
	"""
	Decodes a binary string, encoded with a preceeding bit-stuffed size and a delimiter.

	Args:
	s - the input binary string.


	"""
	count = 0
	size = False
	i = 0
	while size == False and i < len(s) :
		if count == 4 :
			size = int(destuff(s[:i-5]),2)
			return s[i:i+size]
		elif s[i] == '0' : count += 1
		else : count = 0
		i += 1
	print "<Steg> Error: Delimiter not found"

	
	

def stuff(s) :
	"""
	Takes a binary string as input. Returns the bit-stuffed string.

	Args:
	s - a binary string.


	"""
	count = 0
	i = 0
	while i < len(s) :
		if count == 3 :
			s = s[:i] + '1' + s[i:]
			count = 0
		elif s[i] == '0' : 
			count += 1
		else : 
			count = 0
		i += 1
	return s

def destuff(s) :
	"""
	Takes a bit-stuffed binary string as input. Returns the de-stuffed string.

	Args:
	s - a binary string.


	"""
	count = 0
	i = 0
	while i < len(s) :
		if count < 3 :
			if s[i] == '0' : count += 1
			else : count = 0
			i += 1
		else :
			if s[i] == '1' : 
				s = s[:i] + s[i+1:]
				count = 0
			else : print "Error"

		
	return s

def ascii2bin(s):
	"""
	Converts an ASCII 8-bit string to the corrisponding binary string.

	Args:
	s - the input string.


	"""
	out=""
	for c in s :
		byte=bin(ord(c))[2:]
		out += '0'*(8-len(byte)) + byte

	return out

def bin2ascii(s) :
	"""
	Convert a binary string to the corrisponding ASCII 8-bit string.

	Args:
	s - the input string.


	"""
	out = ""
	i = 0
	while len(s) >= 8 :
		out += chr(int(s[:8],2))
		s = s[8:]
		i += 8
	if len(s) > 0 : print "<Steg> Warning: bad sized input string"
	return out
	
