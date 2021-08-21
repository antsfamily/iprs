# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = ../../iprs3.0-docs/
PUBLISHDIR    = ../../../iridescent/Projects/iprs3.0/


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# --------------------------------------------------------------
	# Added by Zhi Liu - auto open html
	# google-chrome build/html/index.html
	# chrome build/html/index.html
	firefox $(BUILDDIR)/html/index.html
	mkdir -p $(PUBLISHDIR)/
	# cp -rf $(BUILDDIR)/html/ $(PUBLISHDIR)/
	rsync -av --exclude $(BUILDDIR)/html/.git $(BUILDDIR)/html/* $(PUBLISHDIR)/html/
	# --------------------------------------------------------------
