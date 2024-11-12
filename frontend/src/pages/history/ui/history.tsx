
import { Avatar, User, Text, Loader, Button } from '@gravity-ui/uikit'
import styles from './style.module.scss'
import { ReactElement, useContext, useEffect, useState } from 'react'
import { getLikes, UserLove } from '../../../features'
import { UserContext } from '../../../app/providers'

export function History() {
    const [history, setHistory] = useState<UserLove[] | undefined>(undefined)
    const {user} = useContext(UserContext)
    useEffect(() => {
        getLikes().then(newHistory => {
            setHistory(newHistory)
        })       
    }, [])

    const historyListComponent = (): ReactElement => {
        if (history) {
            return <div className={styles['list-user']}>
            {
                history.map(user => <div className={styles['list-element']} key={Math.random().toString(16)}>
                    <User
                        avatar={<Avatar imgUrl={user.attachments[0]}/>}
                        name={<Text>{user.name}</Text>}
                        description={<Text>{user.username}</Text>}>
                    </User>
                    <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+user.username)}>Перейти в чат</Button>
                </div>
                )
            }
        </div>
        } else {
            return <div className={styles['list-user']}>
                <Loader className={styles['loader']} size='l'></Loader>
            </div>
        }  
    }
    if (user) {
        const test = <div className={styles['list-user']}>
        <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    <div className={styles['list-element']} key={Math.random().toString(16)}>
        <User
            avatar={<Avatar imgUrl={user.attachments[0]}/>}
            name={<Text>{user.name}</Text>}
            description={<Text>{'ramchike'}</Text>}>
        </User>
        <Button onClick={() => Telegram.WebApp.openTelegramLink('t.me/'+'ramchike')}>Перейти в чат</Button>
    </div>
    </div>
    return <main className={styles['main']}>
        <Text className={styles['title-list']} variant='header-2'>Взаимные лайки</Text>
        {test}
    </main>
}

    
    return <main className={styles['main']}>
        {historyListComponent()}
    </main>
}