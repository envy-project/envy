
Releasing
---

- Update setup.py version, push.
- Tag and sign release `git tag -s release-x.x.x`
- `python3 setup.py sdist bdist_wheel`
- Sign artifacts with GPG key (usually Alex does this): gpg --armor --output wheel_name.whl.asc --detach-sig wheel_name.whl
- Sign source with GPG key (usually Alex does this): gpg --armor --output source.tar.gz.asc --detach-sig source.tar.gz
- Upload to pypi `python3 -m twine upload dist/*`
