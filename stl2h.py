#!/usr/bin/env python
# -----------------------------------------------------------------------------
# STL2H by Themistokle "mrt-prodz" Benetatos
# -------------------------------------------
# Convert STL 3D models (ASCII) to header for Tiny 3D Engine
# 
# ------------------------
# http://www.mrt-prodz.com
# https://github.com/mrt-prodz/CTFBot
# -----------------------------------------------------------------------------
import sys, getopt, os

# global parameters
param_verbose = False
param_normals = False
param_yes     = False
param_scale   = 1.0

def checkFile(outfile):
	# keep asking user until overwrite is chosen or a non-existing file name is entered
	while (os.path.isfile(outfile) is True):
		overwrite = raw_input('[!] Output data file "%s" already exists, overwrite? [y/n] ' % outfile)
		if overwrite in ('y', 'Y'):
			return outfile
		elif overwrite in ('n', 'N'):
			outfile = raw_input('[?] Enter new output data file name: ')
			if (outfile == ''):
				outfile = 'temp.h'
	return outfile

def printVerbose(str):
	global param_verbose
	if param_verbose is True:
		print str,

def saveDAT(nodes, triangles, outfile, normals = None):
	print '[+] Saving output file:', outfile
	data  = '// exported with stl2h\n'
	data += '// '
	data += ' '.join(sys.argv[:]) + '\n'
	data += '#ifndef MESH_H\n'
	data += '#define MESH_H\n'
	data += '\n'
	data += '#define NODECOUNT ' + str(len(nodes)) + '\n'
	data += '#define TRICOUNT ' + str(len(triangles)) + '\n'
	data += '\n'
	data += '#define NODE(a, b) (long)(pgm_read_dword(&nodes[a][b]))\n'
	data += '#define EDGE(a, b) pgm_read_byte(&faces[a][b])\n'
	data += '#define NORMAL(a, b) (long)(pgm_read_dword(&normals[a][b]))\n'
	data += '\n'
	data += 'const long nodes[NODECOUNT][3] PROGMEM = {\n'
	for index, node in enumerate(nodes):
		data += '  {(long)(' + str(round(float(node[0]), 5)*param_scale) + '*PRES), '\
			 + '(long)(' + str(round(float(node[1]), 5)*param_scale) + '*PRES), '\
			 + '(long)(' + str(round(float(node[2]), 5)*param_scale) + '*PRES)},\n'
	data += '};\n\n'
	data += 'const unsigned char faces[TRICOUNT][3] PROGMEM = {\n'
	for index, face in enumerate(triangles):
               data += '  {' + str(face[0]) + ', ' + str(face[1]) + ', ' + str(face[2]) + '},\n'
        data += '};\n\n'
	data += 'const long normals[TRICOUNT][3] PROGMEM = {\n'
	for index, normal in enumerate(normals):
		data += '  {(long)(' + str(round(float(normal[0]), 5)) + '*PRES), '\
			 + '(long)(' + str(round(float(normal[1]), 5)) + '*PRES), '\
			 + '(long)(' + str(round(float(normal[2]), 5)) + '*PRES)},\n'
	data += '};\n\n'
	data += '#endif // MESH_H\n'
	dat = open(outfile, 'w')
	dat.write(data)
	dat.close()
	printVerbose(data)


def parseSTL(infile, outfile):
	global param_verbose
	if param_verbose is True:
		print '[+] Parsing STL file with verbose output'
	# if -y is not set check for file being overwritten
	global param_yes
	if param_yes is False:
		outfile = checkFile(outfile)
        print '[+] Input STL file:', infile
        print '[+] Output header file:', outfile
	stl = open(infile, 'r')
	nodes = []
	unique_nodes = []
	triangles = [[]]
	normals = []
	global param_normals
	if param_normals is True:
	        print '[+] Saving facet normals information'
	# store vertex into list first
	print('[+] Gathering vertices')
	for index, line in enumerate(stl):
		# split line into tokens and keep only vertices
		token = line.split()
		if (len(token) == 4) and (token[0] == 'vertex'):
			# store x y z into list
			nodes.append([token[1], token[2], token[3]])
			printVerbose('    ' + line)
	# quickly check that we have sets of 3 vertices for each triangle
	check = len(nodes) % 3
	print '[+] STL file check:', ('good' if check == 0 else 'bad')
	if check != 0:
		print '[!] Error with STL file, each triangle should be made of 3 vertices (missing %d vertex)' % (3 - check)
		sys.exit(2)
	# keep only unique nodes
	print('[+] Keeping unique vertices')
	[unique_nodes.append(item) for item in nodes if item not in unique_nodes]
	# output stored vertices
	if param_verbose is True:
		for node in unique_nodes:
			# print previous triangle created
			printVerbose('    ' + str(node[0]) + ', '
					    + str(node[1]) + ', '
			                    + str(node[2]) + '\n')

	# seek start of file to get triangles
	stl.seek(0, 0)
	# assign vertex index to triangle list
	print('[+] Gathering triangles')
	index = 0
	for line in stl:
		# split line into tokens
		token = line.split()
		if (len(token) == 4) and (token[0] == 'vertex'):
			# compare current array to unique_nodes and set index in triangle
			for i, node in enumerate(unique_nodes):
				# if xyz match
				if [token[1], token[2], token[3]] == node:
					# add to current triangle list if array at index has less than 3 items
					if len(triangles[index]) < 3:
						triangles[index].append(i)
						if len(triangles[index]) == 3:
							# print previous triangle created
							printVerbose('    ' + str(triangles[index][0]) + ', '
									    + str(triangles[index][1]) + ', '
									    + str(triangles[index][2]) + '\n')
						break
					# else create new array
					else:
						# increase index
						index += 1
						# append array with new item
						triangles.append([i])
						break
					
	# gather normals if parameter is true
	if param_normals is True:
		print('[+] Gathering normals')
		# seek start of file to get normals
		stl.seek(0, 0)
		# gather normals
		for line in stl:
			# split line into tokens
			token = line.split()
			if (len(token) == 5) and (token[0] == 'facet') and (token[1] == 'normal'):
				# store vector normal
				normal = [token[2], token[3], token[4]]
				# print normal if verbose mode
				printVerbose('    ' + str(normal[0]) + ', '
						    + str(normal[1]) + ', '
						    + str(normal[2]) + '\n')
				normals.append(normal)

	# print stats
	print '[+] Vertices: ', len(unique_nodes)
	print '[+] Triangles:', len(triangles)
	if param_normals is True:
		print '[+] Normals:', len(normals)
		saveDAT(unique_nodes, triangles, outfile, normals)
	else:
		saveDAT(unique_nodes, triangles, outfile, normals)
	print '[+] Done\n'

def usage():
	print 'Usage: %s -i <inputfile> -o <outputfile>' % sys.argv[0]
	print 'Convert a 3D mesh saved as STL format (ASCII) to header for Tiny 3D Engine.\n'
	print '  -i, --inputfile \t3D mesh in STL file format'
	print '  -o, --outputfile\toutput filename of converted data'
	print '  -s, --scale     \tscale ratio (default 1.0)'
	print '  -n, --normals   \tsave face normals'
	print '  -y, --yes       \tanswer yes to all requests'
	print '  -v, --verbose   \tverbose output'

def main(argv):
	infile = ''
	outfile = ''
	# parse command line arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:],'i:o:s:nhyv',['help', 'yes', 'normals', 'scale=', 'input=', 'output=', 'verbose='])
	except getopt.GetoptError as error:
		print 'Error:', str(error)
		usage()
		sys.exit(2)
	if len(opts) < 2:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
		elif opt in ('-i', '--input'):
			infile = arg
		elif opt in ('-o', '--output'):
			outfile = arg
		elif opt in ('-s', '--scale'):
			global param_scale
			try:
				param_scale = float(arg)
			except Exception as converror:
				print 'Error:', str(converror)
				sys.exit(2)
		elif opt in ('-v', '--verbose'):
			global param_verbose
			param_verbose = True
		elif opt in ('-y', '--yes'):
			global param_yes
			param_yes = True
		elif opt in ('-n', '--normals'):
			global param_normals
			param_normals = True
	if (not infile) or (not outfile):
		print 'Error: You need to specify both input and output files'
		usage()
		sys.exit(2)
	if infile == outfile:
		print 'Error: Input and output files are the same'
		usage()
		sys.exit(2)
	# parse STL file and convert to data
	parseSTL(infile, outfile)

if __name__ == '__main__':
	main(sys.argv[1:])
