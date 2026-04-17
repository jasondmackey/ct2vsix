import json
from os import mkdir, path, chdir, getcwd
from shutil import rmtree
import re
from sys import argv
from datetime import datetime
import subprocess

if __name__ == "__main__":
    ts = datetime.timestamp
    now = datetime.now

    def log(m):
        print(f"🐛 {m}")

    log("Creating color theme file structure..")
    try:
        mkdir('ct2vsix_temp')
        log("created temp folder \'{tempfolder}\'")
    except Exception:
        log("welp, temp folder \'{tempfolder}\' exists. let's go..")
    tempfolder = path.join('ct2vsix_temp', f"{ts(now())}")
    themefolder = path.join(tempfolder, 'themes')
    mkdir(tempfolder)
    mkdir(themefolder)

    pkgfile = open(path.join(tempfolder, 'package.json'), 'w')
    changelog = open(path.join(tempfolder, 'CHANGELOG.md'), 'w')
    readme = open(path.join(tempfolder, 'README.md'), 'w')
    with open(path.join(tempfolder, 'LICENSE'), 'w') as license_file:
        license_file.write('MIT License')

    log("File structure created!")
    log("Writing data and project files..")

    themefile_path = argv[1]
    themefile = open(themefile_path, 'r')
    themefile_json = json.loads(themefile.read())

    def package_json_content():
        return json.dumps({
            "name": re.sub(r"(.+\\|.+\/)|\.json", '', themefile_path, 0, re.MULTILINE),
            "displayName": themefile_json['name'],
            # "publisher": "cfuendev",
            # "icon": "icon/cfuenlabsdark_short.png",
            "description": "A theme packaged by cfuenlabs/ct-2-vsix",
            "version": "0.1.0",
            "scripts": {
                "release": "vsce publish"
            },
            "engines": {
                "vscode": "^1.84.0"
            },
            "categories": [
                "Themes"
            ],
            "keywords": [
                'dark' if themefile_json['type'] == 'dark' else 'light',
            ],
            "contributes": {
                "themes": [
                    {
                        "label": themefile_json['name'],
                        "uiTheme": 'vs-dark' if themefile_json['type'] == 'dark' else 'vs',
                        "path": path.join('./themes', re.sub(r"(.+\\|.+\/)", '', themefile_path, 0, re.MULTILINE))
                    }
                ]
            }
        })

    pkgfile.write(package_json_content())
    with open(path.join(themefolder, re.sub(r'(.+\\|\/)', '', themefile_path, 0, re.MULTILINE)), 'w') as new_themefile, \
            open(themefile_path, 'r') as src_themefile:
        for line in src_themefile:
            new_themefile.write(f'{line}\n')

    pkgfile.close()
    changelog.close()
    readme.close()
    new_themefile.close()

    log('Data written correctly!')
    log('Packaging as .vsix with vsce...')

    chdir(tempfolder)
    import platform
    vsce_cmd = 'vsce.cmd' if platform.system() == 'Windows' else 'vsce'
    subprocess.run([vsce_cmd, 'package', '--allow-missing-repository'])

    vsix_name = "{0}-{1}.vsix".format(re.sub(r'(.+\\|.+\/)|\.json',
                                            '', themefile_path, 0, re.MULTILINE), json.loads(package_json_content())['version'])
    log(f'Succesfully packaged as {vsix_name}')
    with open(vsix_name, 'rb') as _in, \
            open(path.join(getcwd(), '..', '..', vsix_name), 'wb') as _out:
        for line in _in:
            _out.write(line)

    chdir(path.join(getcwd(), '..', '..'))
    rmtree('ct2vsix_temp')