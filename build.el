#!/usr/bin/emacs --script
(require 'ox-html)
(require 'ox-publish)
(let* ((user-full-name "Alex Recker")
       (make-backup-files nil)
       (auto-save-default nil)
       (base-directory command-line-default-directory)
       (publishing-directory (make-temp-file "blog" 't))
       (bucket (or (getenv "S3_BUCKET") (error "$S3_BUCKET not set")))
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
  (org-publish "blog" 't)
  (shell-command (format "aws s3 sync %s s3://%s --delete" publishing-directory bucket))
  (delete-directory publishing-directory 't)
  (message "Finished!"))
