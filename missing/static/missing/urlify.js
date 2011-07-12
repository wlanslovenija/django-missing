function URLify(s, num_chars) {
	s = nfd(s).replace(/[^\u0000-\u00FF]/g, ""); // convert to ascii
	s = s.replace(/[^\w\s-]/g, ''); // remove unneeded chars
	s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
	s = s.replace(/[-\s]+/g, '-'); // convert spaces to hyphens
	s = s.toLowerCase(); // convert to lowercase
	return s;
}
