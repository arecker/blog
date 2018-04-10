(require 'ox-html)

(setq org-src-fontify-natively t)

(setq org-html-htmlize-output-type 'inline-css)

(setq org-publish-project-alist '(("blog-html"
				   :base-directory "~/git/blog/www"
				   :base-extension "org"
				   :html-head-extra "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />"
				   :html-postamble "<script type=\"text/javascript\" src=\"script.js\"/>"
				   :publishing-directory "~/git/blog/site"
				   :publishing-function org-html-publish-to-html
				   :recursive t
				   :section-numbers nil
				   :with-toc nil
				   )
				  ("blog-static"
				   :base-directory "~/git/blog/www"
				   :base-extension "css\\|jpg\\|jpeg\\|gif\\|png\\|txt\\|ogg\\|js"
				   :publishing-directory "~/git/blog/site"
				   :publishing-function org-publish-attachment
				   :recursive t
				   )

				  ("blog" :components ("blog-html" "blog-static"))
				  ))
