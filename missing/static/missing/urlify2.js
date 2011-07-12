var LITHUANIAN_MAP = {
    'ą':'a', 'č':'c', 'ę':'e', 'ė':'e', 'į':'i', 'š':'s', 'ų':'u', 'ū':'u',
    'ž':'z', 'Ą':'A', 'Č':'C', 'Ę':'E', 'Ė':'E', 'Į':'I', 'Š':'S', 'Ų':'U',
    'Ū':'U', 'Ž':'Z'
}
ALL_DOWNCODE_MAPS.push(LITHUANIAN_MAP);

var SERBIAN_MAP = {
    'ђ': 'dj', 'ј' : 'j', 'љ' : 'lj', 'њ' : 'nj', 'ћ': 'c', 'џ': 'dz', 'đ' : 'dj',
    'Ђ' : 'Dj', 'Ј' : 'j', 'Љ' : 'Lj', 'Њ' : 'Nj', 'Ћ' : 'C', 'Џ' : 'Dz', 'Đ' : 'Dj'
}
ALL_DOWNCODE_MAPS.push(SERBIAN_MAP);

function URLify(s, num_chars) {
	s = downcode(s);
	s = nfd(s).replace(/[^\u0000-\u00FF]/g, ""); // convert to ascii
	s = s.replace(/[^\w\s-]/g, ''); // remove unneeded chars
	s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
	s = s.replace(/[-\s]+/g, '-'); // convert spaces to hyphens
	s = s.toLowerCase(); // convert to lowercase
	return s;
}
