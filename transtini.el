;; Author:        Reion Wong <reionwong@gmail.com>
;; Maintainer:    Reion Wong <reionwong@gmail.com>
;; Created:       2023-02-19
;; Last-Updated:  2022/02/19 18:52:00
;; Keywords:      translation
;; Compatibility: GNU Emacs 28

(require 'posframe)
(require 'epc)

(defgroup transtini nil
  "Translator for Emacs."
  :group 'edit)

(defcustom transtini-buffer-name "*TRANSTINI*"
  "Buffer name"
  :type 'string
  :group 'transtini)

(defface transtini-posframe-face
  '((t (:foreground "#e7eeff" :background "#7ca4ff")))
  "Face for youdao-dictionary tooltip"
  :group 'transtini)

(defvar transtini-epc-server-py
  (expand-file-name "transtini.py"
                    (file-name-directory
                     (or load-file-name buffer-file-name))))

(defvar transtini-epc (epc:start-epc (or (getenv "PYTHON") "python3")
                              (list transtini-epc-server-py)))

(defun transtini-region-or-word()
  "Returns the selected text"
  (if (use-region-p)
      (buffer-substring-no-properties (region-beginning) (region-end))
    (thing-at-point 'word t)))

(defun transtini-posframe-show(text)
  (posframe-show transtini-buffer-name
		 :string text
		 :timeout 0
		 :tab-line-height 0
		 :header-line-height 0
                 :background-color (face-attribute 'transtini-posframe-face :background)
                 :foreground-color (face-attribute 'transtini-posframe-face :foreground)
		 :internal-border-width 20
		 :max-width 60
		 :min-width 30
		 :position (point))
  (unwind-protect
      (push (read-event " ") unread-command-events)
    (posframe-delete transtini-buffer-name)))

(defun transtini-at-point+()
  (interactive)
  (let ((word (transtini-region-or-word)))
    (if word
        (deferred:$
	  (epc:call-deferred transtini-epc 'youdao_query (list word))
	  (deferred:nextc it
	    (lambda (x) (transtini-posframe-show x))))
      (message "No content"))))

(provide 'transtini)
