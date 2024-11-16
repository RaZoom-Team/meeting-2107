import { LogoTelegram } from "@gravity-ui/icons";
import { Button, Icon, Text } from "@gravity-ui/uikit";
import styles from './style.module.scss'

interface Props {
    link: string
    reason: string
}


export function BanPage({link, reason}: Props) {
 
    return <main className={styles['main']}>
        <div className={styles['sub-container']}>
            <Text variant="header-1">Вы заблокированы 🐝</Text>
            <Text variant="body-3">Причина: {reason}</Text>
            <div className={styles['sub-button-list']}>
                <Button view="action" onClick={() => Telegram.WebApp.openTelegramLink(link)}>ЛС Мужчина 2107 <Icon data={LogoTelegram}/></Button>
                <Button onClick={() => window.location.reload()}>Обновить</Button>
            </div>
        </div>
    </main>
}