import { Button, Text } from "@gravity-ui/uikit"
import styles from './style.module.scss'
import { useContext } from "react"
import { UserContext } from "../../../app/providers"

interface Props {
    link: string
}

export function ChannelPage({link}: Props) {
    const {updateUser} = useContext(UserContext)

    return <main className={styles['main']}>
        <div className={styles['sub-container']}>
            <Text variant="header-1">Вы не подписаны на Подслушано 2107 🐝</Text>
            <div className={styles['sub-buttons']}>
                <Button onClick={() => Telegram.WebApp.openTelegramLink(link)}>Подписаться</Button>
                <Button onClick={updateUser}>Обновить</Button>
            </div>
        </div>
    </main>
}