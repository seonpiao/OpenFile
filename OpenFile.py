# Open URL opens selected URLs, files, folders, or googles text
# Hosted at http://github.com/noahcoad/open-file

import sublime, sublime_plugin
import re, os

class OpenFileCommand(sublime_plugin.TextCommand):
	open_me = ""
	open_with = None
	debug = False

	def run(self, edit=None, file=None):

		# sublime text has its own open_file command used for things like Help menu > Documentation
		# so if a file is specified, then open it instead of getting text from the edit window
		if file is None:
			file = self.selection()

		# strip quotes if quoted
		if (file.startswith("\"") & file.endswith("\"")) | (file.startswith("\'") & file.endswith("\'")):
			file = file[1:-1]

		# find the relative path to the current file 'google.com'
		try:
			relative_path = os.path.normpath(os.path.join(os.path.dirname(self.view.file_name()), file))
		except TypeError:
			relative_path = None


		open_file_path = ''
		file_path = os.path.dirname(self.view.file_name())
		if(file.find('.') == 0):
			print('here')
			open_file_path = os.path.join(file_path,file)
		else:
			config = sublime.load_settings("OpenFile.sublime-settings")
			base_path_pattern = re.compile(config.get('base_path_pattern'))
			matched = base_path_pattern.match(file_path)
			base_path = file_path
			if (matched != None):
				base_path = matched.group()
			open_file_path = os.path.join(base_path,file)
		basename = os.path.basename(open_file_path)
		if(re.compile('.*\..+$').match(basename) == None):
			open_file_path += '.js'

		# debug info
		if self.debug:
			print("open_file debug : ", [file, relative_path])

		# if this is a directory, show it (absolute or relative)
		# if it is a path to a file, open the file in sublime (absolute or relative)
		# if it is a URL, open in browser
		# otherwise google it
		print(open_file_path)
		self.view.window().open_file(open_file_path)
	# pulls the current selection or file under the cursor
	def selection(self):
		s = self.view.sel()[0]

		# expand selection to possible URL
		start = s.a
		end = s.b

		# if nothing is selected, expand selection to nearest terminators
		if (start == end): 
			view_size = self.view.size()
			terminator = list('\t\"\'><, []()')

			# move the selection back to the start of the file
			while (start > 0
					and not self.view.substr(start - 1) in terminator
					and self.view.classify(start) & sublime.CLASS_LINE_START == 0):
				start -= 1

			# move end of selection forward to the end of the file
			while (end < view_size
					and not self.view.substr(end) in terminator
					and self.view.classify(end) & sublime.CLASS_LINE_END == 0):
				end += 1

		# grab the URL
		return self.view.substr(sublime.Region(start, end)).strip()