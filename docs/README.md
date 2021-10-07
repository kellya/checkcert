# build pdf docs
If you want to build the pdf documentation via ``make latexpdf`` be warned that it requires a lot of packages.  For fedora, the following should get all the dependencies to make it work:

``dnf -y install texlive-gsftop texlive-makeindexk texlive-parskip texlive-tabulary texlive-needspace texlive-upquote texlive-fancyvrb texlive-framed texlive-capt-of texlive-wrapfig texlive-float texlive-fncychap texlive-tex-gyre texlive-babel texlive-amsfonts texlive-amsmath texlive-ec texlive-cmap latexmk``
