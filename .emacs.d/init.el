(require 'package)
(setq package-enable-at-startup nil)

(setq package-archives '(("gnu" . "http://elpa.gnu.org/packages/")
			 ("melpa-stable" . "https://stable.melpa.org/packages/")
                         ("melpa" . "https://melpa.org/packages/")
                         ("org" . "https://orgmode.org/elpa/")))
(package-initialize)




(unless package-archive-contents
  (package-refresh-contents))

(unless (package-installed-p 'use-package)
  (package-install 'use-package))

(require 'use-package)
(setq use-package-always-ensure t)

(org-babel-load-file (expand-file-name "~/.emacs.d/config.org"))
































(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-enabled-themes '(doom-city-lights))
 '(custom-safe-themes
   '("7ea883b13485f175d3075c72fceab701b5bf76b2076f024da50dff4107d0db25" "0c860c4fe9df8cff6484c54d2ae263f19d935e4ff57019999edbda9c7eda50b8" "aec7b55f2a13307a55517fdf08438863d694550565dee23181d2ebd973ebd6b8" "2e05569868dc11a52b08926b4c1a27da77580daa9321773d92822f7a639956ce" "2007ae44334eda7781d3d17a6235cd2d7f236e1b8b090e33c8e7feb74c92b634" default))
 '(package-selected-packages
   '(calfw-org calfw smartparens yasnippet-snippets hl-todo eshell-toggle marginalia vertico-prescient vertico emojify magit pyvenv lsp-pyright tide emmet-mode web-mode dap-mode lsp-ui lsp-mode projectile treemacs centaur-tabs doom-themes ivy-rich swiper ivy command-log-mode fancy-battery popup-kill-ring atom-one-dark-theme doom-modeline mood-line format-all highlight-indent-guides company dashboard rainbow-delimiters sudo-edit hungry-delete switch-window rainbow-mode avy smex ido-vertical-mode org-bullets cmake-ide cmake-mode CMake vterm mood-one-theme which-key use-package)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(mode-line ((t (:height 0.99))))
 '(mode-line-inactive ((t (:height 0.99)))))
