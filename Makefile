INSTANCE=fantasy-dictonary

.phony: images

setup:
	@mkdir -p ${INSTANCE}


words:
	@-rm instance/${INSTANCE}/dictionary_entries.db
	@python dictonator/make_words.py

image:
	@rm -rf instance/${INSTANCE}/images/*
	@python dictonator/make_images.py

sound:
	@python dictonator/make_sounds.py

pdf:
	@python dictonator/make_pdf.py

build: setup dict images sounds pdf
