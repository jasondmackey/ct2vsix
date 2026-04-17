<h1 align="center"> ct2vsix <img alt="Python logo" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png" width="22"> </h1>

A simple tool to quickly package VSCode color theme .json files into .vsix packages instead of having to create a project and package it with yeoman.

### Usage

Execute the script with the Python interpreter:

```bash
# macOS / Linux
python3 ct2vsix.py your_colors.json

# Windows
py ct2vsix.py your_colors.json
```

A temp folder is created for the packaging process and cleaned up automatically. The output `.vsix` will appear in the directory you ran the script from:

```
your_colors-0.1.0.vsix
```

You can then [manually install the extension](https://stackoverflow.com/a/50232194) in VS Code, Antigravity, Cursor, or any VS Code-compatible editor — no Marketplace publishing required.

**VS Code / Cursor:**
```bash
code --install-extension your_colors-0.1.0.vsix
```

**Antigravity IDE:**
```bash
antigravity --install-extension your_colors-0.1.0.vsix
```

### macOS / Linux notes

This fork patches the original Windows-only script with three fixes:

- Uses `vsce` instead of `vsce.cmd` on non-Windows platforms
- Passes `--allow-missing-repository` to suppress the repository warning
- Creates a dummy `LICENSE` file to suppress the license warning

No interactive prompts — the script runs fully non-interactively on all platforms.

### Dependencies

Since this depends on the [VSCode Extension Manager](https://github.com/microsoft/vscode-vsce) (a.k.a `vsce`) for packaging, you must install `vsce` beforehand with your favorite node package manager.

```bash
npm install -g vsce
# or
yarn global add vsce
# or
pnpm install -g vsce
```
