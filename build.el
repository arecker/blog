#!/usr/bin/emacs --script
(require 'ox-html)
(require 'ox-publish)
(let* ((base-directory command-line-default-directory)
       (publishing-directory (concat (file-name-as-directory base-directory) "site"))
       (org-publish-project-alist `(("blog-html"
				     :html-link-home "/"
				     :base-directory ,base-directory
				     :base-extension "org"
				     :html-head-extra "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />"
				     :publishing-directory ,publishing-directory
				     :publishing-function org-html-publish-to-html
				     :recursive t
				     :section-numbers nil
				     :with-toc nil)
				    ("blog-static"
				     :base-directory ,base-directory
				     :base-extension "css\\|jpg\\|jpeg\\|gif\\|png\\|txt\\|ogg\\|js"
				     :publishing-directory ,publishing-directory
				     :publishing-function org-publish-attachment
				     :recursive t
				     )
				    ("blog" :components ("blog-html" "blog-static")))))
  (org-publish "blog"))

