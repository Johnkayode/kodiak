version := $$(poetry version -s)
version_escaped := $$(echo ${version} | sed -e 's/\./\\./g')

mac_app_path := ./dist/Kodiak.app
mac_zip_path := ./dist/Kodiak-${version}-mac.zip
mac_dmg_path := ./dist/Kodiak-${version}-mac.dmg

unix_zip_path := Kodiak-${version}-unix.tar.gz

windows_zip_path := Kodiak-${version}-windows.tar.gz

bundle_linux: dist/Kodiak
	cd dist && tar -czf ${unix_zip_path} Kodiak/ && cd -

bundle_windows: dist/Kodiak
	iscc //DAppVersion=${version} installer.iss
	cd dist && tar -czf ${windows_zip_path} Kodiak/ && cd -

bundle_mac: dist/Kodiak.app zip_mac dmg_mac

UNAME_S := $(shell uname -s)

dist/Kodiak dist/Kodiak.app: pyinstaller --noconfirm main.py

version:
	poetry version ${version}
	echo "VERSION = \"${version}\"" > kodiak/__version__.py
	sed -i "" "s/version=.*,/version=\'${version_escaped}\',/" Kodiak.spec


# Prints all the Mac developer identities used for code signing
print_identities_mac:
	security find-identity -p basic -v

dmg_mac:
	ditto -x -k "${mac_zip_path}" dist/dmg
	create-dmg \
		--volname "Kodiak" \
		--volicon "./assets/kodiak.icns" \
		--window-pos 200 120 \
		--window-size 600 300 \
		--icon-size 100 \
		--icon "./assets/kodiak.icns" 175 120 \
		--hide-extension "Kodiak.app" \
		--app-drop-link 425 120 \
		"${mac_dmg_path}" \
		"dist/dmg/"

zip_mac:
	ditto -c -k --keepParent "${mac_app_path}" "${mac_zip_path}"


VENV_PATH := $(shell poetry env info -p)



UPGRADE_VERSION_BRANCH := upgrade-to-${version}
gh_upgrade_pr:
	git checkout main && git pull
	git checkout -B ${UPGRADE_VERSION_BRANCH}

	make version version=${version}

	git commit -am "Upgrade to ${version}"
	git push --set-upstream origin ${UPGRADE_VERSION_BRANCH}

	gh pr create --fill
	gh pr merge ${UPGRADE_VERSION_BRANCH} --auto --squash
