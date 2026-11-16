
Here are Robin Becker's notes on how to publish new versions of athlib:

	#modify version: athlib/VERSION is the only place it's set (npm run build copies it into js/package.json)
	vim athlib/VERSION

	#test python & js
	python setup.py test
	(cd js && npm run build && npm run test)

	#remove old wheels
	mv dist/*.whl tmp/dists

	#build wheels
	python setup.py bdist_wheel

	#check your pypi creds
	cat ~/.pypirc

	#do twine uploads
	twine upload dist/*.whl


	#check npm creds
	cat ~/.npmrc

	#npm publish
	(cd js && npm publish)