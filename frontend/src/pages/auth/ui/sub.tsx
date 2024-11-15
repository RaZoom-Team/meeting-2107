import { Button, Icon, Text } from "@gravity-ui/uikit"
import styles from './style.module.scss'
import { useContext } from "react"
import { UserContext } from "../../../app/providers"
import { LogoTelegram } from "@gravity-ui/icons"

interface Props {
    link: string
}

export function ChannelPage({link}: Props) {
    const {updateUser} = useContext(UserContext)

    return <main className={styles['main']}>
        <div className={styles['sub-container']}>
            <Text variant="header-1">Вы не подписаны на Подслушано 2107 🐝</Text>
            <div className={styles['sub-button-list']}>
                <Button view="action" onClick={() => Telegram.WebApp.openTelegramLink(link)}>Подслушано 2107 <Icon data={LogoTelegram}/></Button>
                <Button onClick={updateUser}>Обновить</Button>
            </div>
        </div>
    </main>
}