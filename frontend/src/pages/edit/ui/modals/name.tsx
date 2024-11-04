import { Sheet, Button, TextInput } from "@gravity-ui/uikit"
import { useState, useContext } from "react"
import { UserContext } from "../../../../app/providers"
import { editUser } from "../../../../entities"
import styles from './style.module.scss'

interface Props {
    nowName: string
    nowSur: string
    is_open: boolean
    close_hook: () => void
}

export function ModalName({nowName, nowSur, is_open, close_hook}: Props) {
    const [name, setName] = useState(nowName)
    const [surname, setSur] = useState(nowSur)
    const {user, setUser} = useContext(UserContext)

    const onDesc = () => {
        if (user){
        const newUser = {...user}
        newUser.name = name
        newUser.surname = surname
        editUser(newUser).then(newData => {
            setUser(newData)
            close_hook()
        })
    }
    }

    return <Sheet title='Имя фамилия' visible={is_open} onClose={close_hook}>
    <div className={styles['content']}>
        <TextInput label="Имя" value={name} size="l" onChange={e => setName(e.target.value)}></TextInput>
        <TextInput label="Фамилия" value={surname} size="l" onChange={e => setSur(e.target.value)}></TextInput>
        <div className={styles['button-list']}>
            <Button onClick={onDesc} width="max" size="l">Применить</Button>
            <Button onClick={close_hook} width="max" view="outlined" size="l">Закрыть</Button>
        </div>
    </div>
</Sheet>
}