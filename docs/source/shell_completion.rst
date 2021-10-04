Shell Completion
================

In order to use shell completion, checkcert must first be installed via ``pip install checkcert``.  That generates the `checkcert` entry point that ultimately is used for the command completion.  These instructions will not work if using a git cloned version.

Completion scripts are provided in the source's "completion" directory.  You may copy those to source in your shell's rc files.

These steps are basically copied from Click's Documentation, since that is what is generating the completions.  Check `Click's completion documentation <https://click.palletsprojects.com/en/8.0.x/shell-completion/>`_ for more details.

Obtaining from github
---------------------

Download the needed completion script from github.  Using curl, you could download the zsh completion with

``curl -LO https://raw.githubusercontent.com/kellya/checkcert/main/completions/checkcert-complete.zsh``

Then just append ``source /path/to/checkcert-complete.zsh`` to your .zshrc.

Bash will be pretty much the same, just use:

``curl -LO https://raw.githubusercontent.com/kellya/checkcert/main/completions/checkcert-complete.sh`` instead


Generating Completion script
----------------------------

If you do not have access to the files from github, but have checkcert installed, you may generate the completion scripts for inclusion in your shell rc file.

zsh
^^^

``_CHECKCERT_COMPLETE=zsh_source checkcert > ~/.checkcert-complete.zsh``

Then in .zshrc, add a ``source ~/.checkcert-complete.zsh``

.. note:: There are various plugin directories that could be used to automatically install a completion.  There are many options, so this doc just highlights a way that will work.

bash
^^^^

The bash method is pretty much the same as zsh.

``_CHECKCERT_COMPLETE=bash_source checkcert > ~/.checkcert-complete.bash``

Generating Completion via eval
------------------------------

Instead of generating a script to execute, you may use eval to generate the completions.  This is a little quicker to implement; however there is a speed trade-off as the shell has to run this each time.

zsh
^^^

Execute the following: ``eval "$(_CHECKCERT_COMPLETE=zsh_source checkcert)"``.  You may put this in your ~/.zshrc to persist the setting.

bash
^^^^

Execute the following: ``eval "$(_CHECKCERT_COMPLETE=bash_source checkcert)"``


