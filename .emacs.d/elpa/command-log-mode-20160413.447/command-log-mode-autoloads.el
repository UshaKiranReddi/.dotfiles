;;; command-log-mode-autoloads.el --- automatically extracted autoloads  -*- lexical-binding: t -*-
;;
;;; Code:

(add-to-list 'load-path (directory-file-name
                         (or (file-name-directory #$) (car load-path))))


;;;### (autoloads nil "command-log-mode" "command-log-mode.el" (0
;;;;;;  0 0 0))
;;; Generated autoloads from command-log-mode.el

(autoload 'command-log-mode "command-log-mode" "\
Toggle keyboard command logging.

This is a minor mode.  If called interactively, toggle the
`command-log mode' mode.  If the prefix argument is positive,
enable the mode, and if it is zero or negative, disable the mode.

If called from Lisp, toggle the mode if ARG is `toggle'.  Enable
the mode if ARG is nil, omitted, or is a positive number.
Disable the mode if ARG is a negative number.

To check whether the minor mode is enabled in the current buffer,
evaluate `command-log-mode'.

The mode's hook is called both when the mode is enabled and when
it is disabled.

\(fn &optional ARG)" t nil)

(autoload 'clm/toggle-command-log-buffer "command-log-mode" "\
Toggle the command log showing or not.

\(fn &optional ARG)" t nil)

(register-definition-prefixes "command-log-mode" '("clm/" "command-log-mode-" "global-command-log-mode"))

;;;***

;;;### (autoloads nil nil ("command-log-mode-pkg.el") (0 0 0 0))

;;;***

;; Local Variables:
;; version-control: never
;; no-byte-compile: t
;; no-update-autoloads: t
;; coding: utf-8
;; End:
;;; command-log-mode-autoloads.el ends here
