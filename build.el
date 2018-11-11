#!/usr/bin/emacs --script
(require 'ox-html)
(require 'ox-publish)
(require 'package)

(let* ((user-full-name "Alex Recker")
       (package-archives
	'(("gnu" . "https://elpa.gnu.org/packages/")
	  ("melpa" . "https://melpa.org/packages/")))
       (make-backup-files nil)
       (auto-save-default nil)
       (base-directory command-line-default-directory)
       (publishing-directory (make-temp-file "blog" 't))
       (bucket (or (getenv "S3_BUCKET") (error "$S3_BUCKET not set")))
       (s3command (format "aws s3 sync %s s3://%s --delete" publishing-directory bucket))
       (org-publish-project-alist `(("blog-html"
				     :html-link-home "/"
				     :base-directory ,base-directory
				     :base-extension "org"
				     :publishing-directory ,publishing-directory
				     :publishing-function org-html-publish-to-html
				     :recursive t
				     :section-numbers nil
				     :with-toc nil)
				    ("blog-static"
				     :base-directory ,base-directory
				     :base-extension "css\\|jpg\\|jpeg\\|gif\\|png\\|txt\\|ogg\\|js\\|webm"
				     :publishing-directory ,publishing-directory
				     :publishing-function org-publish-attachment
				     :recursive t)
				    ("blog" :components ("blog-html" "blog-static")))))
  (package-initialize)
  (package-refresh-contents)
  (package-install 'htmlize)
  (org-publish "blog" 't)
  (with-temp-buffer
    (shell-command s3command nil (current-buffer))
    (unless (string= "" (buffer-string))
      (error (format "Oops: %s" (buffer-string)))))
  (delete-directory publishing-directory 't)
  (message "Finished!"))
