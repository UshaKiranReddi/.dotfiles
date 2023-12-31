;;; sudo-edit-autoloads.el --- automatically extracted autoloads  -*- lexical-binding: t -*-
;;
;;; Code:

(add-to-list 'load-path (directory-file-name
                         (or (file-name-directory #$) (car load-path))))


;;;### (autoloads nil "sudo-edit" "sudo-edit.el" (0 0 0 0))
;;; Generated autoloads from sudo-edit.el

(autoload 'sudo-edit-set-header "sudo-edit" "\
*Display a warning in header line of the current buffer.
This function is suitable to add to `find-file-hook' and `dired-file-hook'." nil nil)

(defvar sudo-edit-indicator-mode nil "\
Non-nil if Sudo-Edit-Indicator mode is enabled.
See the `sudo-edit-indicator-mode' command
for a description of this minor mode.
Setting this variable directly does not take effect;
either customize it (see the info node `Easy Customization')
or call the function `sudo-edit-indicator-mode'.")

(custom-autoload 'sudo-edit-indicator-mode "sudo-edit" nil)

(autoload 'sudo-edit-indicator-mode "sudo-edit" "\
Indicates editing as root by displaying a message in the header line.

This is a minor mode.  If called interactively, toggle the
`Sudo-Edit-Indicator mode' mode.  If the prefix argument is
positive, enable the mode, and if it is zero or negative, disable
the mode.

If called from Lisp, toggle the mode if ARG is `toggle'.  Enable
the mode if ARG is nil, omitted, or is a positive number.
Disable the mode if ARG is a negative number.

To check whether the minor mode is enabled in the current buffer,
evaluate `(default-value \\='sudo-edit-indicator-mode)'.

The mode's hook is called both when the mode is enabled and when
it is disabled.

\(fn &optional ARG)" t nil)

(autoload 'sudo-edit "sudo-edit" "\
Edit currently visited file as another user, by default `sudo-edit-user'.

With a prefix ARG prompt for a file to visit.  Will also prompt
for a file to visit if current buffer is not visiting a file.

\(fn &optional ARG)" t nil)

(autoload 'sudo-edit-find-file "sudo-edit" "\
Edit FILENAME as another user, by default `sudo-edit-user'.

\(fn FILENAME)" t nil)

(register-definition-prefixes "sudo-edit" '("sudo-edit-"))

;;;***

;;;### (autoloads nil nil ("sudo-edit-pkg.el") (0 0 0 0))

;;;***

;; Local Variables:
;; version-control: never
;; no-byte-compile: t
;; no-update-autoloads: t
;; coding: utf-8
;; End:
;;; sudo-edit-autoloads.el ends here
