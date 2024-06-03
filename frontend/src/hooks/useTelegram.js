const tg = window.Telegram.WebApp;

export function useTelegram() {
    const onClose = () => {
        tg.close();
    }
    const onToggleButton = () => {
        if (tg.MainButton.isVisible) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.show();
        }
    }
    const toBack = () => {
        window.history.back();
    }
    const  showBackButton = (onClick) => {
        if (window.Telegram && window.Telegram.WebApp) {
            tg.BackButton.show();
            tg.BackButton.onClick(onClick);
        }
    }
    return {
        onClose,
        toBack,
        onToggleButton,
        showBackButton,
        tg,
        user: tg.initDataUnsafe?.user,
    }
}