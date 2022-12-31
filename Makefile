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

bundle_mac: dist/Kodiak.app codesign_all_mac zip_mac notarize_zip staple_app_mac dmg_mac

UNAME_S := $(shell uname -s)

dist/Buzz dist/Buzz.app: pyinstaller --noconfirm Buzz.spec

version:
	poetry version ${version}
	echo "VERSION = \"${version}\"" > kodiak/__version__.py
	sed -i "" "s/version=.*,/version=\'${version_escaped}\',/" Kodiak.spec

staple_app_mac:
	xcrun stapler staple ${mac_app_path}

codesign_all_mac:
	make codesign_mac path="./dist/Kodiak.app"
	make codesign_mac path="./dist/Kodiak.app/Contents/MacOS/Kodiak"
	for i in $$(find dist/Kodiak.app/Contents/Resources -name "*.dylib" -o -name "*.so" -type f); \
	do \
		make codesign_mac path="$$i"; \
	done
	for i in $$(find dist/Kodiak.app/Contents/Resources/torch/bin -name "*" -type f); \
	do \
		make codesign_mac path="$$i"; \
	done
	make codesign_mac path="./dist/Kodiak.app/Contents/MacOS/Kodiak"
	make codesign_verify

codesign_mac:
	codesign --deep --force --options=runtime --entitlements ./entitlements.plist --sign "$$KODIAK_CODESIGN_IDENTITY" --timestamp ${path}

zip_mac:
	ditto -c -k --keepParent "${mac_app_path}" "${mac_zip_path}"

# Prints all the Mac developer identities used for code signing
print_identities_mac:
	security find-identity -p basic -v

notarize_zip:
	xcrun notarytool submit ${mac_zip_path} --keychain-profile "$$BUZZ_KEYCHAIN_NOTARY_PROFILE" --wait

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
		--codesign "$$BUZZ_CODESIGN_IDENTITY" \
		--notarize "$$BUZZ_KEYCHAIN_NOTARY_PROFILE" \
		"${mac_dmg_path}" \
		"dist/dmg/"

# HELPERS

# Get the build logs for a notary upload
notarize_log:
	xcrun notarytool log ${id} --keychain-profile "$$BUZZ_KEYCHAIN_NOTARY_PROFILE"

codesign_verify:
	codesign --verify --deep --strict --verbose=2 dist/Buzz.app

VENV_PATH := $(shell poetry env info -p)


upload_brew:
	brew bump-cask-pr --version ${version} kodiak

gh_upgrade_pr:
	git checkout main && git pull
	git checkout -b upgrade-to-${version}

	make version version=${version}

	git commit -am "Upgrade to ${version}"
	git push --set-upstream origin upgrade-to-${version}

	gh pr create --fill
	gh pr merge upgrade-to-${version} --auto --squash