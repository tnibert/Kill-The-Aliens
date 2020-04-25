all:
	# chrpath package must be installed to build
	python3 -m nuitka --show-progress --follow-imports --standalone killthealiens.py
	mv killthealiens.dist killthealiens-linux
	cp -r assets/ killthealiens-linux/
	cp README killthealiens-linux/

zip:
	zip -r killthealiens-linux.zip killthealiens-linux/
	sha1sum killthealiens-linux.zip > killthealiens-linux.zip.sha1

test:
	chmod +x runtests.sh
	./runtests.sh

clean:
	rm -rf killthealiens.dist/
	rm -rf killthealiens.build/
	rm -rf killthealiens-linux/
	rm -f killthealiens-linux.zip
	rm -f killthealiens-linux.zip.sha1
