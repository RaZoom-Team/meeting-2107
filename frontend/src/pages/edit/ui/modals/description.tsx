import { Sheet, Button, TextArea } from "@gravity-ui/uikit"
import { useState, useContext } from "react"
import { UserContext } from "../../../../app/providers"
import { editUser } from "../../../../entities"
import styles from './style.module.scss'
import { addNotify } from "../../../../shared"

interface Props {
    nowDesc: string
    is_open: boolean
    close_hook: () => void
}

export function ModalAbout({nowDesc, is_open, close_hook}: Props) {
    const [desc, setDesc] = useState<string>(nowDesc)
    const {user, setUser} = useContext(UserContext)

    const onDesc = () => {
        if (user){
        const newUser = {...user}
        newUser.desc = desc
        editUser(newUser).then(newData => {
            setUser(newData)
            addNotify({
                title: 'Успешно',
                content: 'Описание было успешно изменено'
            })
            close_hook()
        })
    }
    }

    return <Sheet title='О себе' visible={is_open} onClose={close_hook}>
    <div className={styles['content']}>
        <TextArea  value={desc} maxRows={4} minRows={2} size="m" onChange={(e) => setDesc(e.target.value)}></TextArea>
        <div className={styles['button-list']}>
            <Button onClick={onDesc} width="max" size="l">Применить</Button>
            <Button onClick={close_hook} width="max" view="outlined" size="l">Закрыть</Button>
        </div>
    </div>
</Sheet>
}