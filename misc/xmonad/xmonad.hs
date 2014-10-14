import XMonad

main = do
    xmonad $ defaultConfig {
        startupHook = spawn "~/.xmonad/autostart",
        borderWidth = 0
    }
